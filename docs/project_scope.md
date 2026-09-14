# Premier League Competitive Mobility Analysis

## Problem

Why am I analyzing Premier League team movement?

A fan sees their club finish in a certain part of the table this season. Based on Premier League history, what usually happens to teams in that position next season?

## Main Question

What is the single most important question I want the data to answer?

The promotion/relegation system creates meaningful movement between competitive positions, and I want to understand the historical risk of teams falling toward relegation.

## Why This Matters

Why would someone interested in the Premier League care about the answer?

Fans can use historical patterns to understand how teams finishing in similar positions have tended to perform in following seasons.

## Study Population

Which clubs will be included in the analysis?

All the club that appeared at least once in the English Premier League during the studied seasons will be included in the analysis.

## Time Period

Which seasons will be analyzed?

Currently, I am planning to study from the season 1995-96 to the season 2025-26.

## Observation Unit

What does one row of the final analytical dataset represent?

One row in the main analytical dataset represents one club's performance in one season.

## Performance Tier Definition

| Tier  | EPL Position | Label                 | Definition / Reasoning                                                                                                            |
| ----- | -----------: | --------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **A** |          1–4 | Elite / Top Four      | Represents the strongest-performing clubs at the top of the Premier League table.                                                 |
| **B** |          5–8 | European Contenders   | Represents strong upper-table clubs that are typically competing for European qualification.                                      |
| **C** |         9–13 | Mid-table / Safe Zone | Represents clubs positioned in the middle of the table, generally away from both the top positions and immediate relegation risk. |
| **D** |        14–17 | Relegation Risk       | Represents lower-table clubs that remain in the Premier League but are relatively close to the relegation positions.              |
| **E** |        18–20 | Relegated             | Represents clubs finishing in the bottom three positions and therefore relegated from the Premier League.                         |

## Spell

In order to actually serve the purpose of tracking the transition inside the EPL, we deleted Tier F.

We use a "spell" to track each club's EPL journey. When a club finishes a season in Tier E and is relegated, that EPL spell ends.

One club can have multiple spells, since it can get promoted after the relegation.

Not every spell ends in E inside the data (The observation window ends while the club is still in the EPL).

A spell begins when a club enters the EPL, either because it is promoted or because it is already presented at the beginning of the study period.

## Data Requirements

What information do I need for each team-season row in order to assign tiers, identify spells, and eventually create season-to-season transitions?

### Raw Variables
- Season
- Club
- Position

### Derived Variables
- Tier
- Spell_ID
- Current_Tier (For transition calculation, from current_tier to next_tier)
- Next_Tier