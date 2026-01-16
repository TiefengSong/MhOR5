import pandas as pd
import MDAnalysis as mda
from MDAnalysis.analysis.hydrogenbonds.hbond_analysis import HydrogenBondAnalysis as HBA
import matplotlib.pyplot as plt
import numpy as np

#%% ======= CALCULATE HYDROGNE BONDS ========
hbond = False
if hbond is True:
    for input in ["DEET", "EOL", "apo"]:
        print(f"Calculating hbond for {input}")
        u = mda.Universe(f"Stockmedia/S4/{input}.tpr", f"Stockmedia/S4/{input}_3us.xtc")
        hbonds = HBA(universe=u)
        hbonds.hydrogens_sel = "protein and resid 184-211 and name HN" #199-226 minus 15
        hbonds.acceptors_sel = "protein and resid 184-211 and name O" #199-226 minus 15
        hbonds.run()
        data = hbonds.results.hbonds
        globals()[f"df_{input}"] = pd.DataFrame(data, columns=["frame", "donor_idx", "hydrogen_idx", "acceptor_idx", "distance", "angle"])
        print("Done")
    for df, name in zip([df_DEET, df_EOL, df_apo], ["DEET", "EOL", "apo"]):
        print(f"Saving hbond for {name}")
        df["donor_resid"] = df["donor_idx"].apply(lambda i: u.atoms[int(i)].resid)
        df["donor_atom"] = df["donor_idx"].apply(lambda i: u.atoms[int(i)].name)
        df["hydrogen_resid"] = df["hydrogen_idx"].apply(lambda i: u.atoms[int(i)].resid)
        df["hydrogen_atom"] = df["hydrogen_idx"].apply(lambda i: u.atoms[int(i)].name)
        df["acceptor_resid"] = df["acceptor_idx"].apply(lambda i: u.atoms[int(i)].resid)
        df["acceptor_atom"] = df["acceptor_idx"].apply(lambda i: u.atoms[int(i)].name)
        df.to_csv(f"Stockmedia/S4/hbond/{name}_hbond.csv", index=False)
        print("Done")

#%% ======= READ DATA (SAVED DATA AT PREVIOUS STEP) ==========
database = "Stockmedia/S4/hbond/"
dataname = ["DEET_hbond", "EOL_hbond", "apo_hbond"]
datasets = []
for data in dataname:
    datasets.append(f"{database}{data}")
for data, name in zip(datasets, ["DEET", "EOL", "apo"]):
    globals()[f"df_{name}"] = pd.read_csv(f"{data}.csv", sep=",")

#%% ----- calculate hbond connection frequency -----
for name in ["DEET", "EOL", "apo"]:
    df = globals()[f"df_{name}"]
    df_filtered = df[(df["acceptor_resid"].between(184, 211)) &
                     (df["hydrogen_resid"] == df["acceptor_resid"] + 4)] #199-226 minus 15
    freq = df_filtered.groupby(["hydrogen_resid", "acceptor_resid"]).size().reset_index(name="frequency")
    n_frames = df["frame"].nunique()
    freq["probability"] = freq["frequency"] / n_frames
    globals()[f"hbond_freq_{name}"] = freq

#%% ============ data ============ #
rows = []
for name in ["DEET", "EOL", "apo"]:
    df = globals()[f"hbond_freq_{name}"].copy()
    df["acceptor_resid"] = df["acceptor_resid"] + 15 -4
    df["hydrogen_resid"] = df["hydrogen_resid"] + 15 -4
    rows.append(df["probability"].values)
heatmap_data = pd.DataFrame(rows,columns=df["acceptor_resid"].values, index=["DEET","EOL","apo"])
#%%
# ======= bar type =========== #
plt.figure(figsize=(11, 4))
x = np.arange(len(heatmap_data.columns))
width = 0.25
for (i, name), color in zip(enumerate(heatmap_data.index),["#ff7F0e", "#1f77b4", "#2ca02c"]):
    plt.bar(
        x + (i - 1) * width,
        heatmap_data.loc[name].values,
        width=width,
        label=name,
        color=color,
        alpha=0.5,
    )
plt.xticks(x, heatmap_data.columns, rotation=90)
plt.xlabel("Acceptor residue (i)")
plt.ylabel("H-bond probability")
plt.title("i → i+4 Hydrogen Bond Probability")
plt.legend(frameon=False)
plt.tight_layout()
plt.show()