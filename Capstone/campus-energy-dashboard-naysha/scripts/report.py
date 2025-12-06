
def export_results(df_clean, df_summary):
    df_clean.to_csv("output/cleaned_energy_data.csv", index=False)
    df_summary.to_csv("output/building_summary.csv")

    total_consumption = df_summary["sum"].sum()
    highest_building = df_summary["sum"].idxmax()
    peak_load_time = df_clean.loc[df_clean["kwh"].idxmax(), "timestamp"]

    with open("output/summary.txt", "w") as f:
        f.write(f"Total Campus Consumption: {total_consumption}\n")
        f.write(f"Highest Consuming Building: {highest_building}\n")
        f.write(f"Peak Load Time: {peak_load_time}\n")
        f.write("Weekly/Daily trends saved in dashboard.png\n")
