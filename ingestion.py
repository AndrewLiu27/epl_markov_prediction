import pandas as pd

df = pd.read_csv("data/raw/1995-96.csv")

# print(df.head())
# print(df.shape)
# print(df.columns)

processed = df.copy()

processed["season"] = "1995-96"

def assign_tier(rank):
    if 1 <= rank <= 4:
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

processed["tier"] = processed["Rk"].apply(assign_tier)

print(processed[["season", "Rk", "Squad", "tier"]])
print(processed["tier"].value_counts().sort_index())