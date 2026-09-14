# Reusable Transformation

## Steps that every season must go through

Raw season files
    ↓
validate each file
    ↓
standardize each season
    ↓
add Season
rename columns
assign Tier
    ↓
combine all seasons into one master DataFrame
    ↓
sort by Club + Season
    ↓
assign Spell_ID

How would python know which season belongs to a new spell?
- Check the same team's previous season. If there is a gap between current season and the previous season, we should start a new spell.

How many spells should each club have, and what exact condition tells us when a new spell begins?
- At least 1. A new spell begins at the season that is not consecutive to the previous season.

How can python tell which season is it in this row?
- From the name of the file. Then the "Season" column, which contains str value. We need to extract the first four characters of the strings and convert them into integers.

bool = previous_season == current_season - 1

This checks if the seasons can be figured out.

I'll try to combine all the seasons first.