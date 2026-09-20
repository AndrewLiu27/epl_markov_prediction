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

processed_seasons = []

for file_path in sorted(RAW_DIR.glob("*.csv")): # This is for reusable bulk process

# Step 2, consider how to add "Season" and rename columns for a single copied csv file (take 1995-96.csv file as an example):

    df = pd.read_csv(file_path) # file path in the parenthesis

    processed = df.copy() # processed is a copy of the DataFrame(1995-96.csv)

    processed["Season"] = file_path.stem # Get the final path component, minus its last suffix. Now it's the csv file names: e.g. 1996-97

    processed = processed.rename(columns={'Squad':'Club', 'Rk' : "Position"}) # rename completed

    processed_seasons.append(processed)

master = pd.concat(processed_seasons, ignore_index=True) # ignore_index = True means to ignore the default csv index



    



# Step by step

# 1. Validate all 31 raw csv files [Checked]
#   Check the docs/raw_validation_specification.md

# 2. For each raw CSV:
#     - add "Season" column from filename
#     - rename columns (Rk -> Position, Squad -> Club)

# 3. Combine all 31 DataFrames into one master DataFrame

# 4. Assign Tier column based on Position

# 5. Sort master DataFrame by Club + Season (Prepared for Spell_ID)

# 6. Assign Spell_ID based on gaps between consecutive seasons

# 7. Set final column order and final row order

# 8. Validate the processed master DataFrame


# What if one problem interrupt the following validating checks?











# deal with season column first, need to specify which season it is.

# how do we extract the first 4 characters in the file name and convert it into integer to put into the season value.

# Column name: starting_year



# pathlib.Path to avoid writing paths everywhere as strings:

# from pathlib import Path

# RAW_DIR = Path("data/raw")

# file_path = RAW_DIR / "1995-96.csv"

