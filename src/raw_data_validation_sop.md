# Raw Data Validation SOP

## 1. Load the data

Load the source file into the analysis environment without modifying the original raw file.

Goal:

* confirm the file can be read successfully;
* preserve the original source data;
* establish the starting dataset.

---

## 2. Inspect the basic structure

Check:

* sample rows;
* number of rows and columns;
* column names;
* data types.

Questions to ask:

* Does one row represent what I expect it to represent?
* Are the expected columns present?
* Are any columns clearly unnecessary?
* Are numeric variables stored as numbers?
* Are text variables stored as text?

---

## 3. Identify key columns

Determine which columns are especially important for the analysis.

Examples may include:

* identifiers;
* dates or time periods;
* categories;
* rankings;
* numerical measures.

For each important column, define what valid data should look like.

Example:

```text
Column: Position
Expected:
- numeric
- no missing values
- unique within each season
- valid range
```

---

## 4. Check missing values

Inspect missing values across all columns.

Ask:

* Which columns contain missing data?
* Is the missingness expected?
* Does the missing value make the observation unusable?
* Should the value be corrected, removed, or retained?

Do not automatically delete missing observations before understanding why they are missing.

---

## 5. Check duplicates

Check both:

* fully duplicated rows;
* duplicates in important identifier columns.

Example distinction:

```text
Entire duplicated row
```

is different from:

```text
Duplicate club name
```

A row can be unique while still violating the expected uniqueness of an identifier.

---

## 6. Validate key column values

For important columns, check whether their values satisfy expected rules.

Possible checks include:

* unique-value count;
* minimum and maximum;
* expected categories;
* expected range;
* unexpected text values;
* impossible values;
* inconsistent formatting.

Example:

```text
Rank should contain exactly 1–20
```

Checking only for duplicates would not catch:

```text
1, 2, 3, ..., 19, 21
```

Therefore, validation should test the actual expected values whenever possible.

---

## 7. Check internal consistency

Look for relationships between columns that should logically agree.

Examples:

```text
Wins + Draws + Losses = Matches Played
```

or:

```text
Goals For - Goals Against = Goal Difference
```

These checks can detect errors that basic missing-value and duplicate checks cannot.

---

## 8. Investigate anomalies

If something looks unusual, inspect the affected rows before changing anything.

Examples:

* unexpected category;
* extreme value;
* duplicate identifier;
* missing identifier;
* invalid range;
* inconsistent calculation.

Do not silently correct anomalies.

Document what happened and why a correction was made.

---

## 9. Decide whether the dataset passes validation

Before transformation, answer:

```text
Is this dataset structurally reliable enough to continue?
```

Possible result:

```text
PASS
PASS WITH ISSUES
FAIL
```

If issues exist, record them before cleaning.

---

## 10. Begin cleaning and transformation

Only after validation should you:

* standardize names;
* rename columns;
* convert data types;
* create derived variables;
* filter observations;
* assign categories;
* combine datasets.

Conceptually:

```text
Load
 ↓
Inspect
 ↓
Identify key columns
 ↓
Validate
 ↓
Investigate issues
 ↓
Clean
 ↓
Transform
 ↓
Analyze
```

## 11. Internal Consistency
e.g.:
W + D + L = MP
GF - GA = GD