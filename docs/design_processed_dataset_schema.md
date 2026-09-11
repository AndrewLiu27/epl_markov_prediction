# Design the processed dataset schema

## What would the processed dataset look like?

### Raw Datasets:
From 1995-96 season to 2025-26 season. There are total of 31 seasons. So there are total of 31 seasons' squad performance tables.

Schema:
(Season: str, Squad: str, Rk: int, Tier: str)

### Processed Datasets (Transition Tables):
The number of the processed datasets would be the number of the teams appeared in the EPL for at least once. We can derive it from the raw datasets. And different team have different number of rows.

Schema:
(Season: str, Squad: str, Rk: int, Tier: str, Spell_id: int)