# Goal:

# epl_transitions.csv
#         ↓
# transition counts
#         ↓
# observed transition probabilities
#         ↓
# 5×5 absorbing Markov matrix
#         ↓
# multi-step probabilities
#         ↓
# relegation risk over time
#         ↓
# expected time to relegation

import pandas as pd
import numpy as np
from pathlib import Path

PROCESSED_DIR = Path("data/processed")

transition = pd.read_csv(
    PROCESSED_DIR / "epl_transitions.csv"
)

# Store each valid transition

# We need transition_count / total transition starting from the current tier
transition_count = transition.groupby(["Current_Tier", "Next_Tier"]).size()

transition_probabilities = (
    transition_count
    / transition_count.groupby(level="Current_Tier").transform("sum")
)

transition_matrix = transition_probabilities.unstack(fill_value=0)

tiers = ["A", "B", "C", "D", "E"]
markov_matrix = transition_matrix.reindex(
    index=tiers,
    columns=tiers,
    fill_value=0
)
markov_matrix.loc["E"] = [0, 0, 0, 0, 1]

# Validating:
# print(transition_count)
# print(transition_matrix)

# print(transition_matrix.sum(axis=1))

assert transition_matrix.sum(axis=1).round(10).eq(1).all()

# Now we save it
TABLES_DIR = Path("data/output/tables")
TABLES_DIR.mkdir(parents=True, exist_ok=True)
output_path = TABLES_DIR / "transition_matrix.csv"
transition_matrix.to_csv(output_path, index=True)

### Multi-step transition:
# P stands for the transition probability matrix
# P^2 represents the two-step transition probability matrix
# (P^2)_{ij} means the probability that a club starting in tier i will be in tier j after two seasons.

# P^2 gives the transition probabilities after two steps, and each row gives the two season distribution conditional on the starting tier.

# Calculate P^2, P^3, P^5

# P2 = markov_matrix @ markov_matrix

# P3 = markov_matrix @ markov_matrix @ markov_matrix

# P5 = markov_matrix @ markov_matrix @ markov_matrix @ markov_matrix @ markov_matrix

# print(P2)
# print(P3)
# print(P5)

# Output a table indicates the probability of the club getting relegated after different number of seasons and starting with different tier:

# Table structure:
# A to E in 1 season, 2 seasons, 3 seasons, and 5 seasons:
# B to E in ...
# C to E in ...
# D to E in ...
# E to E in

def matrix_power_df(matrix, n):
    powered = np.linalg.matrix_power(matrix.to_numpy(), n)

    return pd.DataFrame(
        powered,
        index=matrix.index,
        columns=matrix.columns
    )

P1 = matrix_power_df(markov_matrix, 1)
P2 = matrix_power_df(markov_matrix, 2)
P3 = matrix_power_df(markov_matrix, 3)
P5 = matrix_power_df(markov_matrix, 5)


# For one season, we need the column "E" of P1
# For two seasons, we need the column "E" of P2
# ...
# For five seasons, we need the column "E" of P5
relegation_risk = pd.DataFrame({
    "1_Season": P1["E"],
    "2_Season": P2["E"],
    "3_Season": P3["E"],
    "5_Season": P5["E"]
})

# Remove starting for E:
relegation_risk = relegation_risk.loc[
    ["A", "B", "C", "D"]
]

relegation_risk = (
    relegation_risk * 100
).round(1)

print(relegation_risk)
output_path = TABLES_DIR / "cumulative_relegation_risk.csv"
relegation_risk.to_csv(output_path, index=True)
# Expected time to relegation for every starting tier
# A -> ? seasons

transient_states = ["A", "B", "C", "D"]

Q = markov_matrix.loc[
    transient_states,
    transient_states
].to_numpy()

I = np.eye(len(transient_states))

# Calculate the fundamental matrix:
N = np.linalg.inv(I - Q)

# Calculate expected time:
ones = np.ones(len(transient_states)) # 1-D array doesn't have column or row shape difference

expected_time = N @ ones

# put the result back into a readable pandas Series:
expected_time_to_relegation = pd.Series( # 1-D array constructor
    expected_time,
    index=transient_states,
    name="Expected_Seasons_To_Relegation"
)

output_path = TABLES_DIR / "expected_time_to_relegation.csv"
expected_time_to_relegation.to_csv(output_path, index=True)

# print(N)

# print(expected_time_to_relegation.round(2))
# print("transition_matrix\n")
# print(transition_matrix)
# print("markov_matrix\n")
# print(markov_matrix)