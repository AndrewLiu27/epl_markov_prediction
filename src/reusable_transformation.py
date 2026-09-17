import pandas as pd
from pathlib import Path
RAW_DIR = Path("data/raw")
# e.g.: file_path = RAW_DIR / "1995-96.csv"

# Step by step

# 1. Validate all 31 raw csv files
#   Check the docs/raw_validation_specification.md
def validate_raw_season(file_name):

    df = pd.read_csv(RAW_DIR / file_name)

    errors = [] # Create a master error list for future output

    # 1. Schema
    expected_columns = ['Rk', 'Squad', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']

    if list(df.columns) != expected_columns:
        errors.append("Unexpected columns")

    # 2. Row / missing-values check

    # 2.1 Exactly 20 rows
    if len(df) != 20:
        errors.append(f"Unexpected row count: expected 20, got {len(df)}")

    # 2.2 No missing-values
    if df.isna().any().any(): # any() returns whether at least one element evaluates to True over a specific axis. Acting like an "OR" logical operator across the dataset.
        errors.append("Missing values detected")

    # 3. Uniqueness checks

    # 3.1 no duplicated rows check
    if df.duplicated().any(): # any row
        errors.append("Duplicated rows detected")

    # 3.2 no duplicated Squad check
    if df["Squad"].duplicated().sum() != 0:
        errors.append("Duplicated Squads detected")

    # 3.3 no duplicated Rk check
    if df["Rk"].duplicated().sum() !=0:
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
validate_raw_season("2000-01.csv")

# 2. For each raw CSV:
#     - add "Season" column from filename
#     - rename columns (Rk -> Position, Squad -> Club)

# 3. Combine all 31 DataFrames into one master DataFrame

# 4. Assign Tier column based on Position

# 5. Sort master DataFrame by Club + Season (Prepared for Spell_ID)

# 6. Assign Spell_ID based on gaps between consecutive seasons

# 7. Set final column order and final row order

# 8. Validate the processed master DataFrame











# deal with season column first, need to specify which season it is.

# how do we extract the first 4 characters in the file name and convert it into integer to put into the season value.

# Column name: starting_year



# pathlib.Path to avoid writing paths everywhere as strings:

# from pathlib import Path

# RAW_DIR = Path("data/raw")

# file_path = RAW_DIR / "1995-96.csv"

