import sys
import os

# Ensure we can import sibling folders like utils/ and visualizations/
sys.path.append(os.path.dirname(__file__))

import pandas as pd
from utils.api import get_match_history
from visualizations.charts import plot_analytics


def print_summary_stats(df):
    # Print out some high-level stats for quick insights
    print("\n--- Summary Statistics ---")
    print("Average ACS:", round(df["ACS"].mean(), 2))
    print("Average ADR:", round(df["ADR"].mean(), 2))
    print("Average KDA:", round(df["KDA"].mean(), 2))
    print("Best map by ACS:", df.groupby("map")["ACS"].mean().idxmax())


def analyze_and_visualize(filename=None):
    if filename is None:
        filename = os.path.join(os.path.dirname(__file__), "data", "matches.csv")
    
    # Load data and clean up the date column
    df = pd.read_csv(filename)
    
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Calculate KDA (kills + assists) / deaths
    df["KDA"] = (df["kills"] + df["assists"]) / df["deaths"]
    # Make sure everything is in chronological order before plotting
    df = df.sort_values("date")


    print(df[["date", "agent", "map", "KDA", "ADR", "ACS"]])
    # Show overall trends and averages
    print_summary_stats(df)
    plot_analytics(df)


if __name__ == "__main__":
    # Commented out for now. Waiting for when API key is approved:
    # player_name = "AnhMeo"
    # player_tag = "iuMai"
    # data = get_match_history(player_name, player_tag)

    # if data:
    #     save_matches_to_csv(data)
    # else:
    #     print("Failed to retrieve data.")

    analyze_and_visualize()