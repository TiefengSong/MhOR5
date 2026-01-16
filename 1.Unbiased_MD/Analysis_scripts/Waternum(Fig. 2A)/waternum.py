# gmx select -f DEET_3us.xtc -s DEET.tpr -select 'group 17 and within 0.3 of group 13' -n DEET.ndx -os DEET_water_lig.xvg

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

filepath = ["DEET_water_lig.xvg", "EOL_water_lig.xvg"]

def plot_waternum (filepath, title, labels, colors):
    data = []
    for file in filepath:
        df = pd.read_csv(file, sep=r"\s+", comment="#", header=None, skiprows=24)
        df.columns = ["time", "num"]
        df["time"] = df["time"]/4
        df["num"] = df["num"]/4
        data.append(df)
    plt.figure(figsize=(8,5), dpi=300)
    for df, label, color in zip(data, labels, colors):
        values = df["num"].values
        kde = gaussian_kde(values, bw_method=0.4)
        x = np.linspace(np.min(values), np.max(values), 200)
        plt.plot(x, kde(x), color=color, label=f"{label}")
        plt.fill_between(x, kde(x), color=color, alpha=0.3, linewidth=0, label=f"{label}")
    ax = plt.subplot()
    ax.spines[['right', 'top']].set_visible(False)
    ax.annotate("", xy=(1.01, 0), xycoords=("axes fraction", "data"),
                xytext=(0.999, 0), textcoords=("axes fraction", "data"),
                arrowprops=dict(arrowstyle="-|>", linewidth=1, color="black"))
    ax.annotate("", xy=(0, 1.01), xycoords=("data", "axes fraction"),
                xytext=(0, 0.99), textcoords=("data", "axes fraction"),
                arrowprops=dict(arrowstyle="-|>", linewidth=1, color="black"))
    plt.xticks(np.arange(0,10,2))
    plt.xlim(0,10)
    plt.yticks(np.arange(0,0.5,0.1))
    plt.ylim(0,0.5)
    plt.xlabel("Water Number")
    plt.ylabel("Probability Density")
    plt.tight_layout()
    plt.savefig(f"waternum.pdf", dpi=300, transparent=True)
    plt.show()

plot_waternum(filepath, "Water Number (lig)", ["DEET", "EOL"], ["#ff7F0e", "#1f77b4"])
