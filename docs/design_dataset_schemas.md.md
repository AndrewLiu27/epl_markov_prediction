# Design datasets' schemas

## What would the processed dataset look like?

### Raw Datasets:
From 1995-96 season to 2025-26 season. There are total of 31 seasons. So there are total of 31 seasons' squad performance tables.

Schema:
Rk
Squad
MP
W
D
L
GF
GA
GD
Pts

### Processed Dataset:
We can derive it from the raw datasets.
Schema:
Combine all 31 seasons into one long table:
Season   (Added)
Club     (Altered from Squad)
Position (Altered from Rk)
MP
W
D
L
GF
GA
GD
Pts
Tier     (Processed from Rk)
Spell_ID (Processed from Rk, Tier)

One row still means one club in one EPL season.

### Derived Transition Dataset:
Derived from the Processed Dataset, season -> next season (actual transition happens)

Grain: One row = one valid consecutive-season transition within an EPL spell.

Example:
    Schema:
        Club
        Spell_ID
        Season
        Current_Tier
        Next_Season
        Next_Tier

Club X   1   2018-19   C   2019-20   D
Club X   1   2019-20   D   2020-21   E


## Architecture:
31 raw season files
        ↓
validate + standardize each season
        ↓
ONE processed master table
        ↓
assign Tier + Spell_ID
        ↓
ONE derived transition table
        ↓
transition counts / probabilities / Markov analysis