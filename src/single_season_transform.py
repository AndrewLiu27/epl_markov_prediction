import pandas as pd

df = pd.read_csv("data/raw/1995-96.csv")

# according the file load_data_and_validate_loaded_data.py, this raw csv file is validated.

processed_95 = df.copy()

# Adding a column for season for the dataframe
processed_95["Season"] = "1995-96"  # need to automate this by using the raw csv file name
processed_95 = processed_95.rename(columns={'Squad':'Club', 'Rk' : "Position"}) # Rename the columns to new ones

# # Use pop and insert to change the location of column "Season".
# col = processed_95.pop('Season')
# processed_95.insert(0, 'Season', col)

# # Use pop and insert to change the location of column "Club" and "Position"
# col2 = processed_95.pop('Club')
# processed_95.insert(1, 'Club', col2)

# Create a helper function to assign tier:
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

# Now create the Tier column
processed_95["Tier"] = processed_95["Position"].apply(assign_tier)

# Spell_ID column need to be derived from multi-season's data


# Alter the column adjust approach: (Set the final order of the dataframe)
processed_95 = processed_95[['Season', 'Club', 'Position', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts', 'Tier']]

# Dataframe Checking Section:
# print(processed_95.head())
# print(processed_95.tail())
# print(processed_95["Tier"].value_counts().sort_index())

# Processed Post Validation: (Did our transformation change anything it was not supposed to change compared to the raw database?)
print(processed_95.shape) # Shape
print(processed_95.columns) # Column names / order
print(processed_95.dtypes) # Data types
print(processed_95["Tier"].isna().sum()) # Missing Tier values
print(processed_95["Club"].duplicated().sum()) # Duplicate clubs
print(processed_95["Position"].nunique()) # Position range / uniqueness
print(processed_95["Position"].min())
print(processed_95["Position"].max())


# This transformation script is only for 1995-96.csv file.
# Need a reusable transformation process for one arbitrary season file.
