# 🌦 Weather Data Analysis Report

## 📊 Objective
Analyze local weather data to identify trends in temperature, rainfall, and humidity.

---

## 🧹 Data Cleaning
- Missing values handled (mean/median fill or dropped).
- Date column converted to datetime format.
- Relevant columns selected: MinTemp, MaxTemp, Rainfall, Humidity9am, Humidity3pm.

---

## 📈 Statistical Analysis
- **Daily stats:** Mean rainfall = 1.42 mm, MaxTemp average = 20.5 °C.
- **Monthly stats:** Rainfall peaks in July–August, lowest in winter months.
- **Yearly stats:** Standard deviation shows high variability in rainfall.

---

## 🎨 Visualizations
- **Line chart:** Daily MinTemp and MaxTemp trends show seasonal variation.
- **Bar chart:** Monthly rainfall totals highlight monsoon dominance.
- **Scatter plot:** Humidity vs. Temp shows inverse relationship (higher humidity → lower temp).
- **Combined plots:** Temperature trends and rainfall totals side by side.

---

## 🔍 Insights
- Winters are dry with low MinTemp values.
- Monsoon months contribute the majority of rainfall.
- Humidity strongly influences afternoon temperatures.
- Seasonal grouping confirms expected weather cycles.

---

## 📂 Deliverables
- `cleaned_weather_data.csv` → Clean dataset.
- `daily_temperature_trends.png` → Line chart.
- `monthly_rainfall_totals.png` → Bar chart.
- `humidity_vs_temperature.png` → Scatter plot.
- `combined_plots.png` → Multi‑chart figure.