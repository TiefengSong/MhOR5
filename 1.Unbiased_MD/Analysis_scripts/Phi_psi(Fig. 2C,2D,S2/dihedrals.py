import pandas as pd
from math import pi
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde

filepath = ["COLVAR_DEET_torsion", "COLVAR_EOL_torsion", "COLVAR_apo_torsion"]

with open("COLVAR_DEET_torsion") as f:
    for line in f:
        if line.startswith("#") and 'FIELDS' in line:
            header = line.strip().split()[2:]

for i in filepath:
    globals()[f"data_{i.split("_")[1]}"] = pd.read_csv(i, sep=r"\s+", comment="#", header=None)

data = [data_DEET, data_EOL, data_apo]
name = ["DEET", "EOL", "apo"]

# ===== CHANGE THE ANGLE TO DEGREE =====
for i in data:
    i.columns = header
    for col in i.columns:
        i[col] = i[col]*180/pi

# ===== COMBINE DATA =====
combine_chain = {}
cols = []

for dat, name in zip(data, ["DEET", "EOL", "apo"]):
    head = []
    for i in range(203,222):
        # --- phi
        phi = str(i)+"_phi"
        cols.append(phi)
        values = []
        for col in dat.columns:
            if phi in col:
                values.append(dat[col])
        combine_chain[phi] = pd.concat(values, ignore_index=True)
        head.append(phi)
        # --- psi
        psi = str(i)+"_psi"
        cols.append(psi)
        values = []
        for col in dat.columns:
            if psi in col:
                values.append(dat[col])
        combine_chain[psi] = pd.concat(values, ignore_index=True)
        head.append(psi)
    globals()[f"df_{name}"] = pd.DataFrame.from_dict(combine_chain, orient="columns")
    globals()[f"df_{name}"].columns = head

df = [df_DEET, df_EOL, df_apo]

#%%
# ===== DEET VS EOL VS APO
for col in ["209_phi"]:#["208_phi", "208_psi", "209_phi", "209_psi", "212_phi", "212_psi", "213_phi", "213_psi"]:
    plt.figure(figsize=(8,5), dpi=300)
    for dat, color, name in zip(df, ["#ff7F0e", "#1f77b4", "#2ca02c"], ["DEET", "EOL", "apo"]):
        values = dat[col].values
        kde = gaussian_kde(values, bw_method=0.2)
        x = np.linspace(np.min(values), np.max(values), 200)
        plt.plot(x, kde(x), color=color)
        plt.fill_between(x, kde(x), color=color, alpha=0.3)
    plt.xlabel("Torsion (Degree)")
    plt.ylabel("Probability Density")
    y_max = max([max(gaussian_kde(dat[col].values, bw_method=0.2)(np.linspace(np.min(dat[col].values), np.max(dat[col].values), 200))) for dat in df])
    plt.yticks(np.arange(0, y_max, 0.01))
    ax = plt.subplot()
    ax.spines[['right', 'top']].set_visible(False)
    ax.annotate("", xy=(1.01, 0), xycoords=("axes fraction", "data"),
                xytext=(0.999, 0), textcoords=("axes fraction", "data"),
                arrowprops=dict(arrowstyle="-|>", linewidth=1, color="black"))
    if "phi" in col:
        ax.annotate("", xy=(-125, 1.01), xycoords=("data", "axes fraction"),
                    xytext=(-125, 0.99), textcoords=("data", "axes fraction"),
                    arrowprops=dict(arrowstyle="-|>", linewidth=1, color="black"))
        plt.xticks(np.arange(-125,0,25))
        plt.xlim(-125, -20)
        plt.yticks(np.arange(0, 0.05, 0.01))
        plt.ylim(0, 0.05)
    if "psi" in col:
        ax.annotate("", xy=(-75, 1.01), xycoords=("data", "axes fraction"),
                    xytext=(-75, 0.99), textcoords=("data", "axes fraction"),
                    arrowprops=dict(arrowstyle="-|>", linewidth=1, color="black"))
        plt.xticks(np.arange(-75, 50, 25))
        plt.xlim(-75, 40)
        plt.yticks(np.arange(0, 0.05, 0.01))
        plt.ylim(0, 0.05)
    plt.tight_layout()
    plt.savefig(f"{col}.pdf", dpi=300)
    plt.show()
