import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import seaborn as sns

TABLES_DIR = Path("data/output/tables")
TABLES_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR = Path("data/output/figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(
    TABLES_DIR / "transition_matrix.csv",
    index_col=0
)

fig, ax = plt.subplots(figsize = (8,6))

sns.heatmap(
    df * 100, # data: rectangular dataset. 2D dataset that can be coerced into an ndarray.
    annot=True, # annot: bool or rectangular dataset, optional. If True, write the data value in each cell.
    fmt=".1f", # fmt: str, optional. String formatting code to use when adding annotations.
    cmap="Blues", # cmap: matplotlib colormap name or object, or list of colors, optional
    ax=ax # ax: matplotlib Axes, optional. Axes in which to draw the plot, otherwise use the currently-active Axes.
)

ax.set_title("Premier League Tier Transition Probabilities")
ax.set_xlabel("Next Tier")
ax.set_ylabel("Current Tier")

plt.tight_layout() # make sure the titles show correctly

plt.savefig(
    FIGURES_DIR / "transition_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show() # calling show() can make figure saved to be blank

# cumulative relegation risk

df = pd.read_csv(
    TABLES_DIR / "cumulative_relegation_risk.csv",
    index_col=0
)

df.columns = [
    "1 Season",
    "2 Seasons",
    "3 Seasons",
    "5 Seasons"
]

fig, ax = plt.subplots(figsize=(9,6))

for tier in df.index:
    ax.plot(
        df.columns,
        df.loc[tier],
        marker="o",
        label=f"Tier {tier}"
    )

ax.set_title("Cumulative Relegation Risk Over Time")
ax.set_xlabel("Time Horizon")
ax.set_ylabel("Cumulative Relegation Risk (%)")

ax.legend(title="Starting Tier")

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "cumulative_relegation_risk.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# expected time to relegation

df = pd.read_csv(
    TABLES_DIR / "expected_time_to_relegation.csv",
    index_col=0
)

fig, ax = plt.subplots(figsize=(8, 5))

bars = ax.barh(
    df.index,
    df["Expected_Seasons_To_Relegation"]
)

ax.bar_label(
    bars,
    fmt="%.1f"
)

ax.set_title("Modeled Expected Time to Relegation by Starting Tier")
ax.set_xlabel("Expected Seasons to Relegation")
ax.set_ylabel("Starting Tier")

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "expected_time_to_relegation.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()