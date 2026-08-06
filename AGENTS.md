# AGENTS.md

Guidance for OpenCode (and other coding agents) working in this repo.

## Commands

### Setup
```bash
pip install -e .
pip install -r requirements.dev.txt
```
Use the project virtualenv at `env/`. Always prefix commands with `env/bin/` on macOS/Linux.

### Dependency rule
Never `pip install <pkg>` directly. Add new dependencies to `requirements.txt` (runtime) or `requirements.dev.txt` (dev/test), then install via `pip install -r <file>`.

### Run tests
```bash
env/bin/python -m pytest                              # all tests
env/bin/python -m pytest -m live                      # live/network tests only
env/bin/python -m pytest tests/test_nse.py            # single file
env/bin/python -m pytest tests/test_nse.py::test_cookie  # single test
```
Always use `env/bin/python -m pytest`. Bare `pytest` may pick up system Python. `pytest.ini` sets `testpaths = tests` to prevent crawling into `env/`.

### Live vs offline tests
Tests that make real network calls against external APIs (BSE/NSE) are marked `@pytest.mark.live`. They are **intentionally not mocked** so that any change to the upstream API surfaces as a failure. Because they are slow and depend on the network, they are excluded from CI and instead run on every `git push` via the `pre-push` hook.

- CI runs `pytest -m "not live"`.
- `pre-push` hook runs `pytest -m live`.

To enable the hook for your checkout:
```bash
git config core.hooksPath .githooks
```
To skip live checks on a push: `git push --no-verify`.

### Watch tests (auto-rerun on change)
```bash
env/bin/ptw
```

### CLI entry point
```bash
jdata --help
```

### Version info
Version is stored in two places and both must be updated:
- `pyproject.toml` → `version = "X.Y.Z"`
- `jugaad_data/__init__.py` → `__version__ = "X.Y.Z"`

`check-version.ps1` (PowerShell) verifies the version doesn't already exist on PyPI before release.

## Architecture

`jugaad-data` downloads Indian stock market data from NSE, BSE, and RBI.

### Package layout
- `jugaad_data/nse/` — primary module
  - `archives.py` — bulk archive files (Bhavcopy). `NSEArchives`, `NSEDailyReports`, `NSEIndicesArchives`. Module-level singletons: `bhavcopy_save`, `bhavcopy_fo_save`, etc.
  - `history.py` — historical stock/derivatives/index data via NSE API. `NSEHistory`, `NSEIndexHistory`. Module-level singletons: `stock_raw`, `derivatives_raw`, `index_raw`, `index_pe_raw`, `index_tri_raw`, `index_type_list`, `index_subtype_list`, `index_name_list`. Also `_csv` and `_df` variants. **`NSEIndexHistory` uses niftyindices.com** (not NSE) — endpoint paths are `/BackPage/...`, params wrapped as `{"cinfo": "{'key': 'val'}"}` (single-quoted dict string).
  - `live.py` — real-time quotes via `NSELive`. Uses `@live_cache` decorator.
- `jugaad_data/bse/live.py` — BSE live data (`BSELive`)
- `jugaad_data/rbi/` — RBI economic data (`RBI` class)
- `jugaad_data/holidays.py` — market holiday list
- `jugaad_data/util.py` — shared utilities (caching, date splitting, threading pool, numpy helpers)
- `jugaad_data/cli.py` — Click-based CLI (`jdata` command)

### Key patterns

**pandas is optional:** All `_df` functions check `if not pd` and raise `ModuleNotFoundError`. `util.py` numpy helpers (`np_float`, `np_date`, `np_int`) guard with `@np_exception` decorator.

**Caching (historical data):** `@ut.cached(APP_NAME)` in `util.py` persists responses as pickle files under `user_cache_dir` (or `$J_CACHE_DIR` env var). Cache key = sorted kwarg values. Cache is permanent (no expiry).

**Caching (live data):** `@live_cache` on `NSELive` methods stores results in `self._cache` dict with timestamp. Results reused within `self.time_out` seconds (default 5s).

**Date range splitting:** `util.break_dates()` splits into monthly chunks. `util.pool()` fetches chunks in parallel via `ThreadPoolExecutor` (max 2 workers).

**NSE session setup:** `NSEHistory` and `NSELive` must hit a page URL first to establish cookies before API calls work. `NSEHistory._get()` checks for the `nseappid` cookie and re-initializes the session if missing.

### Imports
`jugaad_data/nse/__init__.py` uses wildcard imports:
```python
from .history import *
from .archives import *
from .live import *
```
Any public name in those modules becomes importable from `jugaad_data.nse`.

## CI
GitHub Actions workflow `run-tests.yml` runs on push/PR to `master`:
- Python 3.10 on ubuntu-latest
- Installs requirements + `flake8 pytest` (but flake8 lint step is disabled/commented out)
- Runs `pytest`

## Additional instructions
This repo also has `.github/copilot-instructions.md` (Copilot-specific developer workflow) and `CLAUDE.md` (Claude Code guidance — **note that CLAUDE.md contains Windows-specific `env/Scripts/` paths that are incorrect for this macOS environment**).
