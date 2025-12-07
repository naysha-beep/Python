#task1
import zipfile

# Path to your zip file
zip_path = "archive.zip"

# Extract all contents into a folder
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall("weather_data")
import pandas as pd

# Load the CSV file
df = pd.read_csv("weather_data/weather.csv")

# Inspect the first few rows
print(df.head())
# General info: column names, data types, non-null counts
print(df.info())

# Summary statistics for numerical columns
print(df.describe())

# First 10 rows for a quick look
print(df.head(10))


#Task 2
# Drop rows with any NaN values
df_clean = df.dropna()

# OR fill missing values
df_clean = df.fillna({
    "Sunshine": df["Sunshine"].mean(),
    "WindGustDir": "Unknown",
    "WindDir9am": "Unknown",
    "WindGustSpeed": df["WindGustSpeed"].median()
})

df["Date"] = pd.date_range(start="2020-01-01", periods=len(df), freq="D")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df_filtered = df[["Date", "MinTemp", "MaxTemp", "Rainfall", "Humidity9am", "Humidity3pm"]]

print(df_filtered.head())
print(df_filtered.info())
print(df_filtered.describe())


#Task 3
import numpy as np
# Example: daily rainfall stats
daily_mean = np.mean(df["Rainfall"])
daily_min = np.min(df["Rainfall"])
daily_max = np.max(df["Rainfall"])
daily_std = np.std(df["Rainfall"])

print("Daily Rainfall Stats:")
print("Mean:", daily_mean, "Min:", daily_min, "Max:", daily_max, "Std:", daily_std)



# Ensure Date column exists
df["Date"] = pd.date_range(start="2020-01-01", periods=len(df), freq="D")
df["Month"] = df["Date"].dt.month

# Monthly statistics for Rainfall
monthly_stats = df.groupby("Month")["Rainfall"].agg(["mean", "min", "max", "std"])
print(monthly_stats)



df["Year"] = df["Date"].dt.year

yearly_stats = df.groupby("Year")["Rainfall"].agg(["mean", "min", "max", "std"])
print(yearly_stats)





columns_to_analyze = ["MinTemp", "MaxTemp", "Rainfall", "Humidity9am", "Humidity3pm"]

monthly_stats_all = df.groupby("Month")[columns_to_analyze].agg(
    ["mean", "min", "max", "std"]
)

print(monthly_stats_all)


#Task4
import matplotlib.pyplot as plt

#Line chart for Daily Temperature Trends
plt.figure(figsize=(10,5))
plt.plot(df["Date"], df["MinTemp"], label="Min Temp", color="blue")
plt.plot(df["Date"], df["MaxTemp"], label="Max Temp", color="red")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.title("Daily Temperature Trends")
plt.legend()
plt.show()

#Bar Chart for Monthly Rainfall Totals

monthly_rainfall = df.groupby(df["Date"].dt.month)["Rainfall"].sum()

plt.figure(figsize=(8,5))
monthly_rainfall.plot(kind="bar", color="skyblue")
plt.xlabel("Month")
plt.ylabel("Total Rainfall (mm)")
plt.title("Monthly Rainfall Totals")
plt.show()

#Scatter Plot for Humidity vs. Temperature
plt.figure(figsize=(8,5))
plt.scatter(df["Humidity3pm"], df["Temp3pm"], alpha=0.6, color="green")
plt.xlabel("Humidity at 3pm (%)")
plt.ylabel("Temperature at 3pm (°C)")
plt.title("Humidity vs Temperature (3pm)")
plt.show()


#Combine Two Plots in One Figure


fig, axes = plt.subplots(1, 2, figsize=(14,5))

# Line chart
axes[0].plot(df["Date"], df["MinTemp"], label="Min Temp", color="blue")
axes[0].plot(df["Date"], df["MaxTemp"], label="Max Temp", color="red")
axes[0].set_title("Daily Temperature Trends")
axes[0].set_xlabel("Date")
axes[0].set_ylabel("Temperature (°C)")
axes[0].legend()

# Bar chart
monthly_rainfall.plot(kind="bar", ax=axes[1], color="skyblue")
axes[1].set_title("Monthly Rainfall Totals")
axes[1].set_xlabel("Month")
axes[1].set_ylabel("Total Rainfall (mm)")

plt.tight_layout()
plt.show()


#Task 5
#grouping by date
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
#grouping by month
columns_to_analyze = ["MinTemp", "MaxTemp", "Rainfall", "Humidity9am", "Humidity3pm"]

monthly_stats_all = df.groupby("Month")[columns_to_analyze].agg(["mean", "min", "max", "std"])
print(monthly_stats_all)
#grouping by season
def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    else:
        return "Post-Monsoon"

df["Season"] = df["Month"].apply(get_season)

seasonal_stats = df.groupby("Season")[columns_to_analyze].agg(["mean", "min", "max", "std"])
print(seasonal_stats)



df = df.set_index("Date")

# Monthly resample
monthly_resample = df.resample("ME")[columns_to_analyze].agg(["mean", "min", "max", "std"])
print(monthly_resample)

# Yearly resample
yearly_resample = df.resample("YE")[columns_to_analyze].agg(["mean", "min", "max", "std"])
print(yearly_resample)



