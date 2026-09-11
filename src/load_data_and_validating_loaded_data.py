import pandas as pd

df = pd.read_csv("data/raw/1995-96.csv")

# print(df.dtypes)         # Checks the data types of the values in columns respectively
# print(df.isna().sum())   # Checks the total empty values in columns respectively
# print(df.duplicated())   # Checks whether any entire rows are duplicated
# print(df["Squad"].duplicated()) # Checks whether any club names appear more than once
# print(df.duplicated().sum()) # Checks the total number of duplicated row
# print(df["Squad"].duplicated().sum()) # Checks the total number of duplicated squads
# print(df["Rk"].duplicated().sum()) # Checks the toal number of duplicated Rk
# print(df["Rk"].count())   # 20 non-missing rank values
# print(df["Rk"].nunique()) # 20 distinct ranks
# print(df["Rk"].min())     # lowest rank is 1
# print(df["Rk"].max())     # highest rank is 20

# Internal Consistency
# 2 rules: W + D + L = MP, GF(Goal For) - GA(Goal Against) = GD

print(df["W"] + df["D"] + df["L"] == df["MP"]) # Checking 1st Rule
print(df["GF"] - df["GA"] == df["GD"]) # Checking 2nd Rule

# Logically Correct, but 20 boolean values are not very informative
# Improvement

print((df["W"] + df["D"] + df["L"] != df["MP"]).sum()) # Check the sum of rows violate the 1st rule
print((df["GF"] - df["GA"] != df["GD"]).sum()) # Checks the sum of the rows violate the 2nd rule

# THE BRACKETS SERVES AS A FILTER, A REFERENCE, OR A CREATING TOOL
