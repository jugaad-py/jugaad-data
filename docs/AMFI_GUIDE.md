# Jugaad Data - AMFI Mutual Fund NAV History Guide

Guide to downloading mutual fund NAV history from the AMFI (Association of
Mutual Funds in India) website using `jugaad-data`.

## Overview

The `amfi` module downloads the daily NAV (Net Asset Value) history report from
AMFI, covering every mutual fund scheme and AMC. It exposes the same
`_raw` / `_df` / `_csv` pattern used by the rest of the library.

Data is grouped in the source file by **scheme type** and **category**, then by
**AMC**. The module flattens that hierarchy so every row carries the context:

- `scheme_type`: `Open Ended`, `Close Ended` or `Interval Fund`
- `category`: e.g. `Money Market`, `Equity Scheme - Multi Cap Fund`,
  `Debt Scheme - Liquid Fund`
- `amc`: the fund house, e.g. `HDFC Mutual Fund`

## Columns

| Column | Description |
|---|---|
| `scheme_code` | AMFI scheme code |
| `scheme_name` | Full scheme name |
| `plan` | `Direct Plan` / `Regular Plan` (blank where not applicable) |
| `option` | `Growth`, `IDCW`, etc. |
| `isin_growth` | ISIN (dividend payout / growth) |
| `isin_reinvest` | ISIN (dividend reinvestment) |
| `nav` | Net Asset Value |
| `date` | NAV date |
| `scheme_type` | Open Ended / Close Ended / Interval Fund |
| `category` | Scheme category |
| `amc` | Asset Management Company (fund house) |

## Usage

### Raw rows

```python
from datetime import date
from jugaad_data.amfi import nav_history_raw

rows = nav_history_raw(date(2026, 9, 1), date(2026, 10, 6))
print(rows[0])
```

### pandas DataFrame

```python
from datetime import date
from jugaad_data.amfi import nav_history_df

df = nav_history_df(date(2026, 9, 1), date(2026, 10, 6))
print(df.head())

# Filter by scheme type / AMC
print(df[df["scheme_type"] == "Interval Fund"].head())
```

`nav` is cast to float and `date` to a datetime.

### CSV

```python
from datetime import date
from jugaad_data.amfi import nav_history_csv

path = nav_history_csv(date(2026, 9, 1), date(2026, 10, 6), output="nav.csv")
```

### Discovery helpers

```python
from datetime import date
from jugaad_data.amfi import scheme_type_list, category_list, amc_list

print(scheme_type_list())              # ['Open Ended', 'Close Ended', 'Interval Fund']
print(category_list(date(2026, 9, 1), date(2026, 9, 1)))
print(amc_list(date(2026, 9, 1), date(2026, 9, 1)))
```

## Filtering by a single AMC

The AMFI endpoint accepts an `mf` AMC code. Passing it restricts the download to
one fund house (much smaller and faster). Pass it via the `mf` argument:

```python
rows = nav_history_raw(date(2026, 9, 1), date(2026, 10, 1), mf="53")
```

## Command line

```bash
jdata nav -f 2026-09-01 -t 2026-10-06 -o nav.csv
```

## Notes

- NAV history for past dates is immutable, so the downloaded report is cached on
  disk (same cache as the rest of the library; override with `$J_CACHE_DIR`).
- A full-range report across all AMCs can be large (tens of MB). Prefer a narrow
  date range or an `mf` filter when you only need a subset.
