import pandas as pd

df = pd.read_csv("data/raw/1995-96.csv")

print(df.head())
print(df.shape)
print(df.columns)