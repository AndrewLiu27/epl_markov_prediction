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

### Processed Master Dataset:
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

Grain: One row still means one club in one EPL season.

### Derived Transition Dataset:
Derived from the Processed Dataset, season -> next season (actual transition happens)

Example:
    Schema:
        Club: str
        Spell_ID: int
        Season: str
        Current_Tier: str
        Next_Season: str
        Next_Tier: str

Club   Spell_ID   Season   Current_Tier  Next_Season   Next_Tier
Club X    1      2018-19       C           2019-20         D
Club Y    1      2018-19       D           2019-20         D      Contain all *valid transitions* for *all clubs*.
Club X    1      2019-20       D           2020-21         E

Grain: One row = one valid transition made by one club between two consecutive EPL seasons within the same spell.

If, for example, Arsenal has 25 valid EPL transitions, Arsenal contributes 25 rows. If another club only has 3 valid transitions, it contributes 3 rows. That is, differnt clubs contribute different rows in this transition dataset.


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

## Data Pipeline

Raw seasonal files (Load the raw data)
        ↓ 
     Validate (SOP)
        ↓ 
Standardize column names (Reasonable)
        ↓ 
    Add Season (Tag the season)
        ↓ 
Combine seasons (combine all the csv files)
        ↓ 
    Assign Tier (Function auto-assign)
        ↓ 
 Assign Spell_ID (Function auto-detect and auto-assign)
        ↓ 
Processed master dataset (To one master ready to use dataset)
        ↓ 
Create valid consecutive-season transitions (according to the spell)
        ↓ 
Transition dataset (Easier to refer to when it comes to transition)
        ↓ 
Transition probabilities / Markov analysis (Markov Transition Matrix)