import matplotlib.pyplot as plt

def plot_analytics(df):
    plt.figure(figsize=(12, 10))

    # ACS Plot
    plt.subplot(3, 1, 1)
    plt.plot(df["date"], df["ACS"], marker="o", color="royalblue")
    plt.title("ACS Over Time")
    plt.ylabel("ACS")
    plt.grid(True)

    # ADR Plot
    plt.subplot(3, 1, 2)
    plt.plot(df["date"], df["ADR"], marker="s", color="orange")
    plt.title("ADR Over Time")
    plt.ylabel("ADR")
    plt.grid(True)

    # KDA Plot
    plt.subplot(3, 1, 3)
    plt.plot(df["date"], df["KDA"], marker="^", color="green")
    plt.title("KDA Over Time")
    plt.xlabel("Date")
    plt.ylabel("KDA")
    plt.grid(True)

    plt.tight_layout()
    plt.show()