import pandas as pd  # import the pandas module and use pd as an alias.

df = pd.read_csv("data/raw/1995-96.csv") # Use the pandas.read_csv() to load the data frame.

# print(df.head())          print sample rows of the data frame
# print(df.shape)           print the shape of the data frame
# print(df.columns)         print the columns 

processed = df.copy()    # Create an independent copy of processed data frame.

processed["Season"] = "1995-96"  # Use bracket to refer to the column or create a new column.

def assign_tier(rank):      # Create a function named assign_tier.
    if 1 <= rank <= 4:      # rank as input (parameter), and string characters (return value) as output
        return "A"
    elif 5 <= rank <= 8:
        return "B"
    elif 9 <= rank <= 13:
        return "C"
    elif 14 <= rank <= 17:
        return "D"
    elif 18 <= rank <= 20:
        return "E"
    else:
        return None

processed["Tier"] = processed["Rk"].apply(assign_tier) # Assign tiers

print(processed[["Season", "Rk", "Squad", "Tier"]])  # Refer to specific columns and print out the values.
print(processed["Tier"].value_counts().sort_index()) # Counts how many rows belong to each tier, then sorts the tier labels alphabetically.
print(processed["Tier"].isna().sum())

print(processed) # Print out the data frame. Usually use print(processed.to_string()).