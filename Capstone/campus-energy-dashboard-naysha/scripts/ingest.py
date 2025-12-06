
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(filename="output/ingestion.log", level=logging.INFO)

def ingest_data(data_dir=r"C:\Users\Naysha\Downloads\Assignments sem 1\Python\campus-energy-dashboard-naysha\data"):
    df_list = []
    for file in Path(data_dir).glob("*.csv"):
        try:
            df = pd.read_csv(file, on_bad_lines="skip")
            # Add metadata if missing
            if "building" not in df.columns:
                df["building"] = file.stem.split("_")[0]  # e.g., buildingA_2025-01.csv
            if "month" not in df.columns:
                df["month"] = file.stem.split("_")[1]
            df_list.append(df)
        except FileNotFoundError:
            logging.error(f"Missing file: {file}")
        except Exception as e:
            logging.error(f"Error reading {file}: {e}")
    df_combined = pd.concat(df_list, ignore_index=True)
    return df_combined
