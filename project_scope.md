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
| **F** |  Outside EPL | Outside               | Represents clubs in the study population that are not competing in the Premier League during the observed season.                 |

