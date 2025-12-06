
from dataclasses import dataclass, field
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
from datetime import datetime
import os
import sys

# ------------------------- Setup logging -------------------------
LOG_PATH = Path('output') / 'processing.log'
Path('output').mkdir(exist_ok=True)
logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# ------------------------- Task 0: Helpers / Sample Data -------------------------

def generate_sample_csvs(data_dir: Path, n_buildings: int = 4, days: int = 30):
    """Generate sample hourly CSV files for example buildings if none exist.
    Each file will contain two columns: timestamp,kwh (no building metadata to test auto metadata addition).
    """
    data_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(42)
    base_date = pd.Timestamp.today().normalize() - pd.Timedelta(days=days)

    for i in range(1, n_buildings + 1):
        timestamps = pd.date_range(start=base_date, periods=days * 24, freq='h')
        # daily pattern + random noise
        daily_cycle = (np.sin((timestamps.hour / 24) * 2 * np.pi) + 1) * 5  # base shape
        building_factor = 1 + rng.normal(0.0, 0.1) + (i - 1) * 0.2
        kwh = np.maximum(0.1, daily_cycle * building_factor + rng.normal(0, 1, len(timestamps)))

        df = pd.DataFrame({'timestamp': timestamps, 'kwh': kwh.round(3)})
        filename = data_dir / f'building_{i}_monthly.csv'
        df.to_csv(filename, index=False)
        logging.info(f'Generated sample file: {filename}')


# ------------------------- Task 1: Data Ingestion and Validation -------------------------

def ingest_csv_folder(data_dir: Path) -> pd.DataFrame:
    """Read all CSV files in data_dir and return combined DataFrame.

    Handles missing folder/files and corrupt rows.
    Adds metadata columns 'building' and 'month' when missing.
    Logs missing/corrupt files.
    """
    if not data_dir.exists():
        logging.warning(f'Data directory {data_dir} does not exist. Creating sample data...')
        generate_sample_csvs(data_dir)

    csv_files = list(data_dir.glob('*.csv'))
    if not csv_files:
        logging.warning('No CSV files found in data directory. Generating sample data...')
        generate_sample_csvs(data_dir)
        csv_files = list(data_dir.glob('*.csv'))

    master_frames = []

##    for file in csv_files:
##        try:
##            # robust read: parse timestamp, skip bad lines
##            df = pd.read_csv(
##                file,
##                parse_dates=['timestamp'],
##                infer_datetime_format=True,
##                on_bad_lines='skip',  # pandas >=1.3
##            )
##        except FileNotFoundError as e:
##            logging.error(f'File not found: {file} -- {e}')
##            continue
##        except Exception as e:
##            logging.error(f'Error reading {file}: {e}. Attempting to read with loose parsing...')
##            try:
##                df = pd.read_csv(file, on_bad_lines='skip')
##            except Exception as e2:
##                logging.error(f'Failed to read {file}: {e2}. Skipping file.')
##                continue

        # ensure expected columns exist
    if 'timestamp' not in df.columns:
            logging.warning(f'File {file.name} missing "timestamp" column. Trying to infer from first column.')
            df.rename(columns={df.columns[0]: 'timestamp'}, inplace=True)
            try:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            except Exception:
                logging.error(f'Unable to parse timestamps in {file.name}. Skipping file.')
                continue

        if 'kwh' not in df.columns:
            # try heuristics: any numeric column other than timestamp
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                df.rename(columns={numeric_cols[0]: 'kwh'}, inplace=True)
                logging.info(f'Inferred kwh column as {numeric_cols[0]} in {file.name}')
            else:
                logging.error(f'File {file.name} has no numeric consumption column. Skipping file.')
                continue

        # Add metadata if missing
        if 'building' not in df.columns:
            # infer from filename
            building_name = file.stem
            df['building'] = building_name
        if 'month' not in df.columns:
            try:
                df['month'] = df['timestamp'].dt.to_period('M').astype(str)
            except Exception:
                df['month'] = ''

        # Clean basic types
        df = df[['timestamp', 'kwh', 'building', 'month']]
        # coerce kwh to numeric
        df['kwh'] = pd.to_numeric(df['kwh'], errors='coerce')
        # drop rows with nan timestamp or kwh
        n_before = len(df)
        df = df.dropna(subset=['timestamp', 'kwh'])
        dropped = n_before - len(df)
        if dropped:
            logging.info(f'Dropped {dropped} rows with invalid timestamp/kwh from {file.name}')

        master_frames.append(df)

    if not master_frames:
        logging.error('No valid data frames were ingested. Exiting with empty DataFrame.')
        return pd.DataFrame(columns=['timestamp', 'kwh', 'building', 'month'])

    df_combined = pd.concat(master_frames, ignore_index=True)
    # enforce types
    df_combined['timestamp'] = pd.to_datetime(df_combined['timestamp'])
    df_combined['kwh'] = pd.to_numeric(df_combined['kwh'])

    # sort
    df_combined = df_combined.sort_values('timestamp').reset_index(drop=True)
    logging.info(f'Combined dataframe created with {len(df_combined)} rows from {len(master_frames)} files.')
    return df_combined


# ------------------------- Task 2: Core Aggregation Logic -------------------------

def calculate_daily_totals(df: pd.DataFrame) -> pd.DataFrame:
    """Return daily kwh totals per building as a DataFrame with DatetimeIndex.
    Columns = building names, index = date (daily).
    """
    df2 = df.copy()
    df2.set_index('timestamp', inplace=True)
    # ensure timezone-naive
    df2.index = pd.to_datetime(df2.index)
    daily = df2.groupby('building').resample('D').kwh.sum().unstack(level=0).fillna(0)
    daily.index = pd.to_datetime(daily.index.date)
    return daily


def calculate_weekly_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    df2 = df.copy()
    df2.set_index('timestamp', inplace=True)
    df2.index = pd.to_datetime(df2.index)
    weekly = df2.groupby('building').resample('W-MON').kwh.sum().unstack(level=0).fillna(0)
    return weekly


def building_wise_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return summary per building: mean, min, max, total (on hourly basis as in raw data).
    """
    summary = df.groupby('building').kwh.agg(['mean', 'min', 'max', 'sum']).rename(
        columns={'sum': 'total'}
    )
    # add daily average (approx)
    summary['daily_average'] = df.groupby('building').apply(
        lambda x: x.set_index('timestamp').resample('D').kwh.sum().mean()
    )
    return summary


# ------------------------- Task 3: Object-Oriented Modeling -------------------------

@dataclass
class MeterReading:
    timestamp: pd.Timestamp
    kwh: float


@dataclass
class Building:
    name: str
    meter_readings: list = field(default_factory=list)

    def add_reading(self, reading: MeterReading):
        self.meter_readings.append(reading)

    def calculate_total_consumption(self) -> float:
        return float(sum(r.kwh for r in self.meter_readings))

    def generate_report(self) -> dict:
        if not self.meter_readings:
            return {'name': self.name, 'total': 0}
        df = pd.DataFrame([{'timestamp': r.timestamp, 'kwh': r.kwh} for r in self.meter_readings])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        total = df.kwh.sum()
        mean = df.kwh.mean()
        peak = df.kwh.max()
        peak_time = df.kwh.idxmax()
        return {
            'name': self.name,
            'total': float(total),
            'mean': float(mean),
            'peak': float(peak),
            'peak_time': str(peak_time),
        }


class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def load_from_dataframe(self, df: pd.DataFrame):
        for _, row in df.iterrows():
            bname = row['building']
            if bname not in self.buildings:
                self.buildings[bname] = Building(name=bname)
            reading = MeterReading(timestamp=row['timestamp'], kwh=float(row['kwh']))
            self.buildings[bname].add_reading(reading)

    def generate_all_reports(self) -> dict:
        return {name: b.generate_report() for name, b in self.buildings.items()}


# ------------------------- Task 4: Visual Output with Matplotlib -------------------------

def create_dashboard(daily_df: pd.DataFrame, weekly_df: pd.DataFrame, df_raw: pd.DataFrame, outpath: Path):
    plt.close('all')
    fig, axes = plt.subplots(3, 1, figsize=(12, 14), constrained_layout=True)

    # 1) Trend Line – daily consumption over time for all buildings
    ax = axes[0]
    for col in daily_df.columns:
        ax.plot(daily_df.index, daily_df[col], label=col)
    ax.set_title('Daily Electricity Consumption per Building')
    ax.set_ylabel('kWh')
    ax.legend(loc='upper right', fontsize='small')

    # 2) Bar Chart – compare average weekly usage across buildings
    ax = axes[1]
    weekly_mean = weekly_df.mean()
    weekly_mean.sort_values(ascending=False).plot(kind='bar', ax=ax)
    ax.set_title('Average Weekly Usage per Building')
    ax.set_ylabel('kWh per week')

    # 3) Scatter Plot – peak-hour consumption vs. time/building
    ax = axes[2]
    # find peak hours across buildings
    peaks = df_raw.groupby('building').apply(lambda g: g.loc[g.kwh.idxmax()])
    # peaks is a DataFrame or Series depending; normalize
    if isinstance(peaks, pd.Series):
        peaks = peaks.to_frame().T
    peaks = peaks.reset_index(drop=True)
    sc = ax.scatter(pd.to_datetime(peaks['timestamp']), peaks['kwh'], s=80)
    # annotate points with building names
    for i, row in peaks.iterrows():
        ax.annotate(row['building'], (pd.to_datetime(row['timestamp']), row['kwh']), textcoords="offset points", xytext=(5,5))
    ax.set_title('Peak-Hour Consumption by Building')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('kWh')

    # Save
    outfile = outpath / 'dashboard.png'
    fig.savefig(outfile, dpi=150)
    logging.info(f'Dashboard saved to {outfile}')
    plt.close(fig)


# ------------------------- Task 5: Persistence and Executive Summary -------------------------

def persist_outputs(df_combined: pd.DataFrame, summary_df: pd.DataFrame, reports: dict, outpath: Path):
    outpath.mkdir(parents=True, exist_ok=True)
    cleaned_path = outpath / 'cleaned_energy_data.csv'
    summary_path = outpath / 'building_summary.csv'
    txt_path = outpath / 'summary.txt'

    df_combined.to_csv(cleaned_path, index=False)
    logging.info(f'Cleaned data exported to {cleaned_path}')

    summary_df.to_csv(summary_path)
    logging.info(f'Building summary exported to {summary_path}')

    # generate textual summary
    total_campus = df_combined.kwh.sum()
    # highest-consuming building by total
    building_totals = df_combined.groupby('building').kwh.sum()
    highest_building = building_totals.idxmax()
    highest_value = building_totals.max()
    # peak load time overall
    idx_peak_overall = df_combined.kwh.idxmax()
    if pd.isna(idx_peak_overall):
        peak_time = 'N/A'
    else:
        peak_time = str(df_combined.loc[idx_peak_overall, 'timestamp'])

    # weekly/daily trends summary - recent week vs previous
    try:
        df_temp = df_combined.copy()
        df_temp['timestamp'] = pd.to_datetime(df_temp['timestamp'])
        df_temp.set_index('timestamp', inplace=True)
        last_week = df_temp.last('7D').kwh.sum()
        prev_week = df_temp.last('14D').head(df_temp.last('14D').shape[0] - df_temp.last('7D').shape[0]).kwh.sum() if df_temp.last('14D').shape[0] > df_temp.last('7D').shape[0] else np.nan
    except Exception:
        last_week = np.nan
        prev_week = np.nan

    with open(txt_path, 'w') as f:
        f.write('Campus Energy Executive Summary\n')
        f.write('Generated: ' + datetime.now().isoformat() + '\n\n')
        f.write(f'Total campus consumption (kWh): {total_campus:.2f}\n')
        f.write(f'Highest-consuming building: {highest_building} ({highest_value:.2f} kWh)\n')
        f.write(f'Peak load time (overall): {peak_time}\n')
        f.write('\nWeekly/Daily Trends:\n')
        f.write(f'Last week consumption (kWh): {last_week:.2f}\n')
        if not np.isnan(prev_week):
            delta = last_week - prev_week
            f.write(f'Change vs previous week (kWh): {delta:.2f}\n')
        f.write('\nPer-building quick reports:\n')
        for name, rep in reports.items():
            f.write(f"- {name}: total={rep.get('total',0):.2f}, mean={rep.get('mean',0):.2f}, peak={rep.get('peak',0):.2f} at {rep.get('peak_time','')}.\n")

    logging.info(f'Executive summary written to {txt_path}')


# ------------------------- Main Orchestration -------------------------

def main(data_folder: str = 'data', output_folder: str = 'output'):
    data_dir = Path(data_folder)
    out_dir = Path(output_folder)

    # Task 1: ingest
    df_combined = ingest_csv_folder(data_dir)
    if df_combined.empty:
        logging.error('No data to process. Exiting.')
        sys.exit(1)

    # Task 2: aggregations
    daily = calculate_daily_totals(df_combined)
    weekly = calculate_weekly_aggregates(df_combined)
    building_summary_df = building_wise_summary(df_combined)

    # Task 3: OOP
    manager = BuildingManager()
    manager.load_from_dataframe(df_combined)
    reports = manager.generate_all_reports()

    # Task 4: visualization
    create_dashboard(daily, weekly, df_combined, out_dir)

    # Task 5: persistence and executive summary
    persist_outputs(df_combined, building_summary_df, reports, out_dir)

    logging.info('All tasks completed successfully. Check the output folder for results.')


if __name__ == '__main__':
    # allow optional CLI args for data and output folder
    import argparse

    parser = argparse.ArgumentParser(description='Campus Energy Dashboard generator')
    parser.add_argument('--data', default='data', help='Path to data folder containing CSVs')
    parser.add_argument('--output', default='output', help='Output folder to write results')
    args = parser.parse_args()

    main(data_folder=args.data, output_folder=args.output)
