# Step by step

# 1. Validate all 31 raw csv files

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

