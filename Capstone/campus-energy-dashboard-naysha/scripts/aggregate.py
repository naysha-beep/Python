
def calculate_daily_totals(df):
    return df.resample("D", on="timestamp")["kwh"].sum()

def calculate_weekly_aggregates(df):
    return df.resample("W", on="timestamp")["kwh"].sum()

def building_wise_summary(df):
    return df.groupby("building")["kwh"].agg(["mean", "min", "max", "sum"])
