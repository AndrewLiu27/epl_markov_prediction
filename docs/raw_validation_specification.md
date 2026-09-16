# Raw CSV validation

1. Expected schema
    - Expected columns:
        Rk, Squad, MP, W, D, L, GF, GA, GD, Pts

2. Row / missing-value checks
    - exactly 20 rows
    - every expected column has 20 non-missing values

3. Uniqueness checks
    - no duplicated rows
    - no duplicated Squad
    - no duplicated Rk

4. Rank validity
    - Rk has 20 unique values
    - min(Rk) == 1
    - max(Rk) == 20

5. Match count
    - MP == 38 for every club

6. Match-record consistency
    - W + D + L == MP

7. Goal-difference consistency
    - GF - GA == GD