import pandas as pd
import matplotlib.pyplot as plt
from utils.api import get_match_history
import os

def save_matches_to_csv(api_data, filename="data/matches.csv"):
    """
    Extract and save match summary data from Tracker API response.
    """
    matches = api_data.get("data", {}).get("matches", [])
    rows = []

    for match in matches:
        metadata = match.get("metadata", {})
        stats = match.get("stats", {})
        player_stats = stats.get("kills", 0), stats.get("deaths", 0), stats.get("assists", 0), stats.get("score", 0)

        row = {
            "match_id": match.get("id"),
            "date": metadata.get("date", "unknown"),
            "map": metadata.get("mapName", "unknown"),
            "agent": metadata.get("agentName", "unknown"),
            "kills": stats.get("kills", 0),
            "deaths": stats.get("deaths", 1),
            "assists": stats.get("assists", 0),
            "score": stats.get("score", 0),
        }

        # Derived metrics (optional: fake round count = 24 for now)
        row["rounds"] = 24  

        rows.append(row)

    df = pd.DataFrame(rows)
    os.makedirs("data", exist_ok=True)
    df.to_csv(filename, index=False)
    print(f"Saved {len(rows)} matches to {filename}")

def analyze_and_visualize(filename="data/matches.csv"):
    df = pd.read_csv(filename)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Calculate KDA
    df["KDA"] = (df["kills"] + df["assists"]) / df["deaths"]

    # Sort chronologically
    df = df.sort_values("date")

    # Display summary
    print(df[["date", "agent", "map", "KDA", "ADR", "ACS"]])

    # Visualization: 3 subplots (ACS, ADR, KDA)
    plt.figure(figsize=(12, 10))

    # ACS
    plt.subplot(3, 1, 1)
    plt.plot(df["date"], df["ACS"], marker="o", color="royalblue")
    plt.title("ACS Over Time")
    plt.ylabel("ACS")
    plt.grid(True)

    # ADR
    plt.subplot(3, 1, 2)
    plt.plot(df["date"], df["ADR"], marker="s", color="orange")
    plt.title("ADR Over Time")
    plt.ylabel("ADR")
    plt.grid(True)

    # KDA
    plt.subplot(3, 1, 3)
    plt.plot(df["date"], df["KDA"], marker="^", color="green")
    plt.title("KDA Over Time")
    plt.xlabel("Date")
    plt.ylabel("KDA")
    plt.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
 #   player_name = "AnhMeo"  # Your Riot ID name
 #   player_tag = "iuMai"    # Your Riot ID tagline (without #)

 #   data = get_match_history(player_name, player_tag)
 #   if data:
 #       save_matches_to_csv(data)
        analyze_and_visualize()
 #   else:
 #       print("Failed to retrieve data.")
