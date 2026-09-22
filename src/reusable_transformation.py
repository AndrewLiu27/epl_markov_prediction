import pandas as pd
from pathlib import Path
RAW_DIR = Path("data/raw")
# e.g.: file_path = RAW_DIR / "1995-96.csv"

def validate_raw_season(file_path):

    df = pd.read_csv(file_path) # Change to Path value to depend less on RAW_DIR. OG: (RAW_DIR / file_name) -> Now: (file_path) We use path to make less confusion with name and path

    errors = [] # Create a master error list for future output

    # 1. Schema
    expected_columns = ['Rk', 'Squad', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']

    if list(df.columns) != expected_columns:
        errors.append(f"Unexpected columns: expected {expected_columns}, got {list(df.columns)}")
        return errors # Stop early! Checks below rely on the completeness of columns.

    # 2. Row / missing-values check

    # 2.1 Exactly 20 rows
    if len(df) != 20:
        errors.append(f"Unexpected row count: expected 20, got {len(df)}")

    # 2.2 No missing-values
    if df.isna().any().any(): # any() returns whether at least one element evaluates to True over a specific axis(axis = 0 for default, which means checks down the rows of each column). Acting like an "OR" logical operator across the dataset.
        errors.append("Missing values detected") # df.isna() -> Check for every cell! If missing value, return Ture; Return False, if value exists.
                                                 # df.isna().any() -> Checks down the row of each column that if any value in that column contain any True?
                                                 # df.isna().any().any() -> Checks if any value in the result of (if there's any True in each column) contain any True?
                                                 # We are tranforming 20 * 10 = 200 bool values into 1 single bool value.
                                                 # That is, True if at least one missing value exists anywhere in the DataFrame

    # 3. Uniqueness checks

    # 3.1 no duplicated rows check
    if df.duplicated().any(): # df.duplicated(): Return Boolean value for each row, return True when the row is duplicated to previous row(s).
        errors.append("Duplicated rows detected") # df.duplicated().any(): Returns True if the result contains any True value.

    # 3.2 no duplicated Squad check
    if df["Squad"].duplicated().sum() != 0: # df["Squad"].duplicated(): Checks down the row of the column "Squad" and returns True if any duplicated value is found.
        errors.append("Duplicated Squads detected")

    # 3.3 no duplicated Rk check
    if df["Rk"].duplicated().sum() != 0:
        errors.append("Duplicated Rk detected")

    # 4. Rank validity
    
    # 4.1 Rk has 20 unique values check
    if df["Rk"].nunique() != 20:
        errors.append(f"Unique values count is incorrect, only {df['Rk'].nunique()} unique Rk values detected")

    # 4.2 minimum rank is 1 check
    if df["Rk"].min() != 1:
        errors.append("Rank doesn't start from 1")

    # 4.3 maximum rank is 20 check
    if df["Rk"].max() != 20:
        errors.append("Rank doesn't end with 20")

    # 5. Match count
    if not (df["MP"] == 38).all(): # be careful of the difference betwen .all() and .any()
        errors.append("Season not finished") # all() methods return True if all elements evaluate to True

    # 6. Match-record consistency check
    if not (df["W"] + df["D"] + df["L"] == df["MP"]).all():
        errors.append("W + D + L != MP")
    # 7. Goal-difference consistency
    if not (df["GF"] - df["GA"] == df["GD"]).all():
        errors.append("GF - GA != GD")

    # Return the error message:
    return errors

    
# Test Session:
# all_valid = True

# for file_path in sorted(RAW_DIR.glob("*.csv")): # glob() gives a Path

#     errors = validate_raw_season(file_path) # .name extract the file name instead of the Path("data/raw/1995-96.csv").

#     if errors:   # errors should be either an empty list or a list contains string elements. bool([]) is evaluated to be False; bool(["some errors"]) is evaluated to be True
#         all_valid = False # set all_valid metric to False when error encountered

#         print(f"{file_path.name}: Validation failed")
#         for error in errors:
#             print(f"  - {error}")
#     else:
#         print(f"{file_path.name}: Validation passed")

# if not all_valid:
#     raise ValueError("Raw data validation failed. Pipeline stopped.") # raise ValueError(...) not only prints out a message, but also stops execution.

# print("All raw CSV files passed validation.")

# Bifurcation starts from here:
# validate all raw files -> any problem? -> Yes -> Stop
#                               |-> No -> Transformation

#
# Transformation begins here:
#
# We create copies to transform. Finally we create a processed master database in the data/processed folder.

# Step 2 and Step 3:

processed_seasons = []

expected_columns = ["Position", "Club", "MP", "W", "D", "L", "GF", "GA", "GD", "Pts", "Season"]

EXPECTED_SEASONS = 31

CLUBS_PER_SEASON = 20

for file_path in sorted(RAW_DIR.glob("*.csv")): # This is for reusable bulk process

# Step 2, consider how to add "Season" and rename columns for a single copied csv file (take 1995-96.csv file as an example):

    processed = pd.read_csv(file_path) # df is the loaded dataframe from the original file. Changing it won't change the original file. We directly use processed to store the dataframe.

    processed["Season"] = file_path.stem # Get the final path component, minus its last suffix. Now it's the csv file names: e.g. 1996-97

    processed = processed.rename(
        columns={
            'Squad':'Club', 'Rk' : "Position"
        }
    ) # rename completed. Use inplace = True after the column clause with a comma to avoid using assignment

    # Validate the transformation before accepting the DataFrame
    assert list(processed.columns) == expected_columns

    processed_seasons.append(processed)

master = pd.concat(processed_seasons, ignore_index = True) # Concatenation happened. And ignore_index = True means to ignore the default csv index

# Master database level validation:
assert list(master.columns) == expected_columns
assert len(master) == EXPECTED_SEASONS * CLUBS_PER_SEASON
assert master["Season"].nunique() == EXPECTED_SEASONS
assert master.groupby("Season").size().eq(CLUBS_PER_SEASON).all() # Every individual season contributes exactly 20 clubs. all() returns True if every value is evaluated to be True
assert not master.duplicated(
    subset = ["Season", "Club"]
).any()
# print(master.head())
# print(master.tail())
# print(master.shape)

# Step 4 Applying assign_tier() to master["Position"]

def assign_tier(pos):
    if 1 <= pos <= 4:
        return "A"
    elif 5 <= pos <= 8:
        return "B"
    elif 9 <= pos <= 13:
        return "C"
    elif 14 <= pos <= 17:
        return "D"
    elif 18 <= pos <= 20:
        return "E"
    else:
        return None

master["Tier"] = master["Position"].apply(assign_tier) # Apply assign_tier() to master["Position"]

# Step 4 validation
assert master["Tier"].isna().sum() == 0

assert set(master["Tier"].unique()) == {"A", "B", "C", "D", "E"}

expected_tier_counts = {
    "A": 124,
    "B": 124,
    "C": 155,
    "D": 124,
    "E": 93
}

assert master["Tier"].value_counts().sort_index().to_dict() == expected_tier_counts

# Step 5: Sort Club + Season to detect the season gap:
# To show the spell's starting and ending point, we need to show season and club at the same row to determine if the seasons for the same club is consecutive

# Example:
# Season   Club
# 2001-02  Arsenal  (spell 1)
# 2002-03  Arsenal  (spell 1)
# 2005-06  Arsenal  (spell 2)
# 2005-06  Chelsea  (spell 1)
# 2006-07  Chelsea  (spell 1)


# master dataset
#     ↓
# group each club's rows together
#     ↓
# put that club's seasons in chronological order
#     ↓
# compare current season with previous season
#     ↓
# gap?
#  ┌───────┴────────┐
# No               Yes
# same spell       new spell

# season_club = master.sort_values(by=["Club","Season"])
# print(season_club.head())
# print(season_club.tail())
# print(season_club.shape)
# print(master[master["Club"] == "Arsenal"][["Club", "Season"]]) # Pay Attention
# single bracket: master["Club"] returns a pandas Series
# 1D Series:
# 0 Arsenal
# 1 Chelsea
# ... 
# Name: Club
#  !!!(a Series also has an index and a name)!!!
# double bracket: master[["Club"]] returns a pandas dataframe
# 2D dataframe: 
#     Club 
# 0 Arsenal 
# 1 Chelsea 
# ...  
# 
# ["Club", "Season"] is a list
# boolean mask: master["Club"] == "Arsenal" produces another Series, which contains boolean values:
# 0 True 
# 1 False 
# 2 False 
# ...

# master[boolean mask]: this means, keep only the rows where the value is True. This filters out the arsenal rows
# master[boolean mask][["Club", "Season"]]: only the arsenal rows dataframe and we only want 2 columns. 
# Structure: DataFrame[boolean mask][columns] (columns = ["Club", "Season"])
# DataFrame[boolean mask] -> DataFrame. DataFrame[columns] -> DataFrame with the selected columns.

# Result:
# Club       Season
# Arsenal    1995-96
# Arsenal    1996-97
# Arsenal    1997-98
# ...

# Same result with the .loc usage:
# master.loc[
#     master["Club"] == "Arsenal", # selecting row(s)
#     ["Club", "Season"] # selecting column(s)
# ]
# Read .loc as master.loc[rows, columns]



# Step 6 Assign Spell_ID
master["Season_Start"] = master["Season"].str[:4].astype(int)
# print(master["Season_Start"]) # Successful

# We are assigning spell_id. To figure out where does a spell start and ends.
# Spell starts when there is no consecutive season before. A new spell as a season that is not consecutive to that club's previous EPL season.
# Spell ends when the club have no consecutive next season or there is no next season. (Optional)

# Then we need club and season_start. And we need to separate clubs repectively.

# Adding a "Previous_Season" column next to the "Season_start" can make it obvious

# Club    Season_Start    Previous_Season
# Leeds       1995             NaN                 1995 - previous -> NA   (New Spell)
# Leeds       1996            1995                 1996 - previous -> 1995 (Same Spell)
# Leeds       2000            1996                 2000 - previous -> 1996 (New Spell)
# Leeds       2001            2000                 2001 - previous -> 2000 (Same Spell)

# if Season_Start - Previous_Season == 1 then same spell, if not start a new spell for season start

master["Previous_Season"] = master.groupby("Club")["Season_Start"].shift(1) # master -> group rows by Club -> select Season_Start within each group
# master.groupby("Club") -> group rows by Club
# master.groupby("Club")["Season_Start"] -> take "Season_Start" within each club
# master.groupby("Club")["Season_Start"].shift(1) -> moves the values down one row !!!within each club!!! shift(1) means previous row

# print(
#     master.loc[
#         master["Club"] == "Leeds United",                      # Rows
#         ["Club", "Season", "Season_Start", "Previous_Season"]  # Columns
#     ]
# )

# Status Check:
# print(master.head())
# print(master.tail())
# print(master.shape)

# Trying to assign Spell_ID:
master["New_Spell"] = (master["Previous_Season"].isna() | ((master["Season_Start"] - master["Previous_Season"]) != 1))
# Use "|" or "&" to express logical or, logical and.

# Status Check:
# print(
#     master.loc[
#         master["Club"] == "Leeds United",
#         ["Club", "Season", "Season_Start", "Previous_Season", "New_Spell"]
#     ]
# )

# We need to group by club to avoid increment throughout the whole master dataframe
master["Spell_ID"] = (master.groupby("Club")["New_Spell"].cumsum()) # Cumulative Sum: True -> 1 / False -> 0
# Cumulatively added the boolean value at each row. True increments the spell nubmer; False keeps it unchanged

# Status Check:
# print(
#     master.loc[
#         master["Spell_ID"] > 1,
#         ["Club", "Season", "Season_Start", "Previous_Season", "New_Spell", "Spell_ID"]
#     ].head(20)
# )

assert master.groupby("Club")["Spell_ID"].min().eq(1).all() # Checks that every club starts at spell 1


# Step 6 completed
# Step 7 Finalize processed master:
#   1. Remove helper columns ()
#   2. Set final column order
#   3. Decide final row order
master = master[
    [
        "Season",
        "Club",
        "Position",
        "MP",
        "W",
        "D",
        "L",
        "GF",
        "GA",
        "GD",
        "Pts",
        "Tier",
        "Spell_ID"
    ]
]

master = master.sort_values(["Season","Position"]).reset_index(drop=True)

# Check:
# print(master.head())
# print(master.tail())
# print(master.shape)


# Step 8: Final processed-dataset validation

# 5 areas:

# 1. Final Schema:
expected_final_columns = [
    "Season",
    "Club",
    "Position",
    "MP",
    "W",
    "D",
    "L",
    "GF",
    "GA",
    "GD",
    "Pts",
    "Tier",
    "Spell_ID"
]

assert list(master.columns) == expected_final_columns

# 2. Grain: One row per club-season
assert not master.duplicated(   # returns a boolean pandas.Series indicating whether each row in the DataFrame is a duplicated of a previous row.
    subset = ["Season", "Club"] # Scans only these two columns and returns True when detects two row with the same both column values (impossible to have 2 rows with the same season and same club)
).any()                         # .any(): Returns True if any boolean value is True 

# 3. Structure: Expected size
assert len(master) == EXPECTED_SEASONS * CLUBS_PER_SEASON
assert master["Season"].nunique() == EXPECTED_SEASONS
assert master.groupby("Season").size().eq(20).all() # size() counts how many rows are in each season group
# eq(20) checks if equal to 20 for each season

# 4. Derived columns: Tier + Spell_ID
assert master["Tier"].isna().sum() == 0
assert master["Spell_ID"].isna().sum() == 0

assert set(master["Tier"].unique()) == {  # Checks if unique tiers are A B C D E
    "A", "B", "C", "D", "E"
}

assert master.groupby("Club")["Spell_ID"].min().eq(1).all()

# 5. Row order: Final ordering
check = master.sort_values(["Season", "Position"]).reset_index(drop=True)

assert master.reset_index(drop=True).equals(check) # Confirms final dataset is ordered season-by-season and position-by-position


# Step 9: Save processed dataset
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
output_path = PROCESSED_DIR / "epl_master.csv"
master.to_csv(output_path, index=False) # index=False: pandas row index is not part of the analytical schema

# Output verification:
saved = pd.read_csv(output_path)

assert saved.shape == master.shape
assert list(saved.columns) == list(master.columns)


# Step 10: Create transition dataset

transition = pd.read_csv(output_path)

# Keep only required columns
transition = transition[["Club", "Spell_ID", "Season", "Tier"]]

# Rename "Tier" to "Current_Tier"
transition = transition.rename(
    columns= {
        "Tier" : "Current_Tier"
    }
)

# Get next season and next tier within the SAME spell (Group by both Club and Spell_ID to avoid shift in different spell)
transition["Next_Season"] = transition.groupby(["Club", "Spell_ID"])["Season"].shift(-1)
transition["Next_Tier"] = transition.groupby(["Club", "Spell_ID"])["Current_Tier"].shift(-1)


# We noticed the last season has no next season, so there is no transition for these rows
# Transition database only contain valid transitions
# So we need to drop the invalid rows

# Inspection:
# print(
#     transition[
#         transition["Next_Season"].isna()
#     ].head(20)
# )

# Actual Dropping:
transition = transition.dropna(
    subset=["Next_Season", "Next_Tier"]  # drop the rows in which contains null value in specified columns
).reset_index(drop=True)

# Verification:
# print(transition.head())
# print(transition.tail())
# print(transition.shape)


#########################
# Final validate:
expected_transition_columns = [
    "Club",
    "Spell_ID",
    "Season",
    "Current_Tier",
    "Next_Season",
    "Next_Tier"
]

assert list(transition.columns) == expected_transition_columns

assert transition["Next_Season"].isna().sum() == 0
assert transition["Next_Tier"].isna().sum() == 0

# Checks if all the rows represent a one-season step
current_start = transition["Season"].str[:4].astype(int)
next_start = transition["Next_Season"].str[:4].astype(int)

assert (next_start - current_start == 1).all()

# Validate the row count structurally
num_spells = master.groupby(["Club", "Spell_ID"]).ngroups

assert len(transition) == len(master) - num_spells

# Save it
transition_path = PROCESSED_DIR / "epl_transitions.csv"

transition.to_csv(transition_path, index=False)

# Step by step

# 1. Validate all 31 raw csv files [Checked]
#   Check the docs/raw_validation_specification.md

# 2. For each raw CSV:              [Checked]
#     - add "Season" column from filename
#     - rename columns (Rk -> Position, Squad -> Club)

# 3. Combine all 31 DataFrames into one master DataFrame    [Checked]

# 4. Assign Tier column based on Position   [Checked]

# 5. Sort master DataFrame by Club + Season (Prepared for Spell_ID) [Checked]

# 6. Assign Spell_ID based on gaps between consecutive seasons  [Checked]

# 7. Set final column order and final row order [Checked]

# 8. Validate the processed master DataFrame    [Checked]

# 9. Save processed master dataset  [Checked]

# 10. Build transition dataset  [Checked]

# What if one problem interrupt the following validating checks?











# deal with season column first, need to specify which season it is.

# how do we extract the first 4 characters in the file name and convert it into integer to put into the season value.

# Column name: starting_year



# pathlib.Path to avoid writing paths everywhere as strings:

# from pathlib import Path

# RAW_DIR = Path("data/raw")

# file_path = RAW_DIR / "1995-96.csv"

