
import matplotlib.pyplot as plt

def create_dashboard(df_daily, df_weekly, df_summary):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Trend Line
    df_daily.plot(ax=axes[0], title="Daily Consumption Trend")

    # Bar Chart
    df_weekly.groupby("building").mean().plot.bar(ax=axes[1], title="Weekly Avg Usage")

    # Scatter Plot
    axes[2].scatter(df_summary["max"], df_summary["sum"])
    axes[2].set_title("Peak vs Total Consumption")
    axes[2].set_xlabel("Peak Load")
    axes[2].set_ylabel("Total Consumption")

    plt.tight_layout()
    plt.savefig("output/dashboard.png")
