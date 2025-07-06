import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Force GUI-based backend

from utils.api import get_match_history

def analyze_and_visualize(filename=None):
    if filename is None:
        filename = os.path.join(os.path.dirname(__file__), "data", "matches.csv")

    df = pd.read_csv(filename)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["KDA"] = (df["kills"] + df["assists"]) / df["deaths"]
    df = df.sort_values("date")

    print(df[["date", "agent", "map", "KDA", "ADR", "ACS"]])

    plt.figure(figsize=(12, 10))

    plt.subplot(3, 1, 1)
    plt.plot(df["date"], df["ACS"], marker="o", color="royalblue")
    plt.title("ACS Over Time")
    plt.ylabel("ACS")
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(df["date"], df["ADR"], marker="s", color="orange")
    plt.title("ADR Over Time")
    plt.ylabel("ADR")
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(df["date"], df["KDA"], marker="^", color="green")
    plt.title("KDA Over Time")
    plt.xlabel("Date")
    plt.ylabel("KDA")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    analyze_and_visualize()
