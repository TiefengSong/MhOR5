import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
from scipy.stats import gaussian_kde

filepath = ["COLVAR_DEET", "COLVAR_EOL", "COLVAR_apo"] 

for file in filepath:
    globals()[f"data_{file.split("_")[1]}"] = pd.read_csv(file, sep=r"\s+", comment="#", header=None)
    globals()[f"data_{file.split("_")[1]}"].columns = header

expanded_frames = {}
cols = []
header = ["ANGLE_S4a", "ANGLE_S4b"]

# ===== COMBINE DATA OF CHAIN A-D =====
for j, name in zip([data_DEET, data_EOL, data_apo], ["DEET", "EOL", "apo"]):
    for i in ["ANGLE_S4a", "ANGLE_S4b"]:
        cols.append(i)
        values = []
        for col in j.columns:
            if col.startswith(i):
                values.append(j[col])
        expanded_frames[i] = pd.concat(values, ignore_index=True)
    globals()[f"df_{name}"] = pd.DataFrame.from_dict(expanded_frames, orient="columns")
    globals()[f"df_{name}"].columns = header

# ===== CHANGE THE ANGLE TO DEGREE =====
for data in df_DEET, df_EOL, df_apo:
    for col in data.columns:
        if 'ANGLE' in col:
            data[col] = data[col]*180/pi

# ===== COMPARE DEET VS EOL VS APO=====
for col in ["ANGLE_S4a", "ANGLE_S4b"]:
    plt.figure(figsize=(8,5), dpi=300)
    for data, color, name in zip([df_DEET, df_EOL, df_apo], ["#ff7F0e", "#1f77b4", "#2ca02c"], ["DEET", "EOL", "apo"]):
        values = data[col].values
        kde = gaussian_kde(values, bw_method=0.4)
        x = np.linspace(np.min(values), np.max(values), 200)
        plt.plot(x, kde(x), color=color, label=f"{name}")
        plt.fill_between(x, kde(x), color=color, alpha=0.3, linewidth=0, label=f"{name} KDE")
    ax = plt.subplot()
    ax.spines[['right', 'top']].set_visible(False)
    ax.annotate("", xy=(1.012, 0), xycoords=("axes fraction", "data"),
                xytext=(0.999, 0), textcoords=("axes fraction", "data"),
                arrowprops=dict(arrowstyle="-|>", linewidth=1, color="black"))
    if col == "ANGLE_S4a":
        ax.annotate("", xy=(6, 0.091), xycoords=("data", "data"),
                    xytext=(6, 0.089), textcoords=("data", "data"),
                    arrowprops=dict(arrowstyle="-|>", linewidth=1, color="black"))
        plt.xticks(np.arange(5, 60, 10))
        plt.xlim(6, 60)
        plt.yticks(np.arange(0, 0.1, 0.02))
        plt.ylim(0, 0.09)
    if col == "ANGLE_S4b":
        ax.annotate("", xy=(10, 0.183), xycoords=("data", "data"),
                    xytext=(10, 0.181), textcoords=("data", "data"),
                    arrowprops=dict(arrowstyle="-|>", linewidth=1, color="black"))
        plt.xticks(np.arange(10, 40, 5))
        plt.xlim(10, 40)
        plt.yticks(np.arange(0,0.18,0.04))
        plt.ylim(0, 0.18)
    plt.xlabel("Angle Value (deg)")
    plt.ylabel("Probability Density")
    plt.savefig(f"{col}.pdf", dpi=300)
    plt.show()
