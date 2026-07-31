# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Setup
```bash
pip install -e .
pip install -r requirements.dev.txt
```

> **Dependency rule:** Never install packages directly with `pip install <pkg>`. Always add new dependencies to `requirements.txt` (runtime) or `requirements.dev.txt` (dev/test), then install via `pip install -r <file>`.

> **Virtualenv rule:** Always use the project virtualenv at `env/`. Use `env/Scripts/pip3.exe` (or `env/Scripts/python.exe -m pip`) and `env/Scripts/python.exe` (Windows) for all installs and execution. Note: `env/Scripts/pip` does not exist — use `pip3.exe` instead.

> **Git push rule:** This repo uses `core.sshCommand = ssh -i ~/.ssh/github_personal -o IdentitiesOnly=yes` (set in local git config). Always push using this repo's git config — never override with `-F /dev/null`.

### Run tests
```bash
env/Scripts/python.exe -m pytest                        # all tests
env/Scripts/python.exe -m pytest tests/test_nse.py      # single file
env/Scripts/python.exe -m pytest tests/test_nse.py::test_cookie  # single test
```

> **pytest rule:** Always run pytest via `env/Scripts/python.exe -m pytest`. Do not use bare `pytest` — it may use the system Python and pick up tests from `env/`. A `pytest.ini` with `testpaths = tests` is in place to prevent crawling into `env/`.

### Watch tests (auto-rerun on change)
```bash
ptw
```

### CLI entry point
```bash
jdata --help
```

## Architecture

`jugaad-data` is a Python library for downloading Indian stock market data from NSE (National Stock Exchange), BSE, and RBI websites.

### Package structure

- `jugaad_data/nse/` — NSE data (the primary module)
  - `archives.py` — Download bulk archive files (Bhavcopy). Contains `NSEArchives` and `NSEIndicesArchives` classes. Module-level singletons expose top-level functions (`bhavcopy_save`, `bhavcopy_fo_save`, etc.).
  - `history.py` — Historical stock/derivatives/index data via NSE API. Contains `NSEHistory` and `NSEIndexHistory` classes. Module-level singletons expose `stock_raw`, `derivatives_raw`, `index_raw`, `index_pe_raw`, `index_tri_raw`, `index_type_list`, `index_subtype_list`, `index_name_list`. Also provides `_csv` and `_df` variants for stock/index data. `NSEIndexHistory` uses niftyindices.com (not NSE) — endpoint paths are `/BackPage/...`, params are wrapped as `{"cinfo": "{'key': 'val'}"}` (single-quoted dict string).
  - `live.py` — Real-time quotes via `NSELive` class. Uses `@live_cache` decorator to throttle repeated calls within `time_out` seconds.
- `jugaad_data/bse/live.py` — BSE live data
- `jugaad_data/rbi/` — RBI economic data
- `jugaad_data/holidays.py` — Market holiday data
- `jugaad_data/util.py` — Shared utilities
- `jugaad_data/cli.py` — Click-based CLI (`jdata` command)

### Key patterns

**Caching (historical data):** `@ut.cached(APP_NAME)` in `util.py` persists responses as pickle files under `user_cache_dir` (or `$J_CACHE_DIR` env var). Cache key is derived from function arguments. Cache is permanent (no expiry) — used to avoid re-fetching the same date range.

**Caching (live data):** `@live_cache` decorator on `NSELive` methods stores results in `self._cache` dict with a timestamp. Results are reused within `self.time_out` seconds (default 5s).

**Date range splitting:** `util.break_dates()` splits a date range into monthly chunks. `util.pool()` fetches chunks in parallel via `ThreadPoolExecutor`.

**NSE session setup:** Both `NSEHistory` and `NSELive` must hit a page URL first to establish cookies before API calls work. `NSEHistory._get()` checks for the `nseappid` cookie and re-initializes the session if missing.

**pandas is optional:** All `_df` functions check `if not pd` and raise `ModuleNotFoundError`. The `util.py` numpy helpers (`np_float`, `np_date`, `np_int`) similarly guard against missing numpy.

### Data flow for historical stock data
1. `stock_df()` / `stock_csv()` → `stock_raw()` (module-level alias)
2. `stock_raw()` → `NSEHistory.stock_raw()` → splits dates, calls `_stock()` in parallel
3. `_stock()` → decorated with `@ut.cached` → hits NSE API or returns pickle cache
