# 1st goal: Given start_year = 1997, automatically construct the correct FBref URL and print it.

# 2nd goal: Read the page with pd.read_html() and print the number of tables found.

# 3rd goal: Figure out which table is the Premier League standings table.

# 4th goal: Save that one table.

# pathlib.Path to avoid writing paths everywhere as strings:

# from pathlib import Path

# RAW_DIR = Path("data/raw")

# file_path = RAW_DIR / "1995-96.csv"

start_year = 1997
end_year = start_year + 1

# My attempt:
# construct the FBref URL using these two variables
