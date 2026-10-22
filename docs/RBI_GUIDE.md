# Jugaad Data - RBI Economic Data Guide

Fetch the current policy rates, reserve ratios, lending/deposit rates, FX reference rates, G-Sec and T-bill yields shown on the [RBI home page](https://www.rbi.org.in).

```python
from jugaad_data.rbi import RBI

r = RBI()
rates = r.current_rates()
```

## Format

`current_rates()` returns a JSON-serialisable dict:

- Percentages are **fractions**: `5.5%` is `0.055`.
- A range is `{"min": ..., "max": ...}`.
- A value RBI shows as `-` (for example a T-bill with no recent auction cut-off) is `None`.
- Rows RBI adds to the page that are not listed below are ignored.

```python
{
    "policy_repo_rate": 0.055,
    "standing_deposit_facility_rate": 0.0525,
    "marginal_standing_facility_rate": 0.0575,
    "bank_rate": 0.0575,
    "fixed_reverse_repo_rate": 0.0335,
    "crr": 0.03,
    "slr": 0.18,
    "base_rate": {"min": 0.084, "max": 0.1},
    "mclr_overnight": {"min": 0.078, "max": 0.08},
    "savings_deposit_rate": 0.025,
    "term_deposit_rate_gt_1y": {"min": 0.06, "max": 0.0675},
    "call_rate": {"min": 0.0485, "max": 0.059},
    "fx": [{"currency": "USD", "units": 1, "inr": 94.6986},
           {"currency": "JPY", "units": 100, "inr": 60.25}, ...],   # INR per `units` of currency
    "gsec": [{"coupon": 0.062, "maturity_year": 2029, "yield": 0.06947}, ...],
    "tbill": [{"days": 91, "yield": None}, {"days": 182, "yield": None}, {"days": 364, "yield": None}],
    "indices": {"sensex": 73709.69, "nifty_50": 22811.35}
}
```

The benchmark G-Secs shown by RBI change over time, so look them up by iterating the `gsec` list, not by a fixed name.

## Examples

```python
rates = r.current_rates()

# Repo rate in percent
print(rates["policy_repo_rate"] * 100)            # 5.5

# Rate corridor
print(rates["fixed_reverse_repo_rate"], rates["policy_repo_rate"], rates["marginal_standing_facility_rate"])

# Lending rate = base rate + spread (ranges are dicts)
spread = 0.015
lo = rates["base_rate"]["min"] + spread
hi = rates["base_rate"]["max"] + spread

# G-Sec yield curve
curve = {g["maturity_year"]: g["yield"] for g in rates["gsec"]}

# USD/INR
usd = next(f["inr"] / f["units"] for f in rates["fx"] if f["currency"] == "USD")
```

### T-bills

Unavailable T-bill yields are `None` in `current_rates()`, so the rest of the data stays usable. To get a single number and fail loudly when it is missing, use `tbill_rate(days)`:

```python
from jugaad_data.rbi import RBI, RateNotAvailable

try:
    y = RBI().tbill_rate(91)        # fraction, e.g. 0.0661
except RateNotAvailable:
    ...                             # RBI shows no cut-off at the moment
```

## Limitations

- Latest values only, no history.
- Equity index levels on the RBI page can be stale; use `NSELive` for market data.
- Parsing depends on the RBI home page markup, so a redesign can break it. Parser tests use saved HTML in `tests/fixtures/`, and a live test (`-m live`) checks the real page.
