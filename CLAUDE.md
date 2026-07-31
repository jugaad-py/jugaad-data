# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Setup
```bash
pip install -e .
pip install -r requirements.dev.txt
```

> **Dependency rule:** Never install packages directly with `pip install <pkg>`. Always add new dependencies to `requirements.txt` (runtime) or `requirements.dev.txt` (dev/test), then install via `pip install -r <file>`.

> **Virtualenv rule:** Always use the project virtualenv at `env/`. Use `env/Scripts/pip` and `env/Scripts/python` (Windows) for all installs and execution.

> **Git push rule:** This repo uses `core.sshCommand = ssh -i ~/.ssh/github_personal -o IdentitiesOnly=yes` (set in local git config). Always push using this repo's git config — never override with `-F /dev/null`.

### Run tests
```bash
pytest                        # all tests
pytest tests/test_nse.py      # single file
pytest tests/test_nse.py::test_cookie  # single test
```

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
  - `history.py` — Historical stock/derivatives/index data via NSE API. Contains `NSEHistory` and `NSEIndexHistory` classes. Module-level singletons expose `stock_raw`, `derivatives_raw`, `index_raw`. Also provides `_csv` and `_df` variants for each data type.
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
