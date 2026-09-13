import pandas as pd

df = pd.read_csv("data/raw/1995-96.csv") #use ("data/.../filename", index=False) to tell pandas not to save the index (first unnamed column index)

# according the file load_data_and_validate_loaded_data.py, this raw csv file is validated.

processed_95 = df.copy()

# Adding a column for season for the dataframe
processed_95["Season"] = "1995-96"  # need to automate this by using the raw csv file name
processed_95 = processed_95.rename(columns={'Squad':'Club', 'Rk' : "Position"})

# Use pop and insert to change the location of column "Season".
col = processed_95.pop('Season')
processed_95.insert(0, 'Season', col)

# Use pop and insert to change the location of column "Club" and "Position"
col2 = processed_95.pop('Club')
processed_95.insert(1, 'Club', col2)

# Print out check session:
print(processed_95.head())
