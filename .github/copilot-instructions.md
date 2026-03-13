# Core Directive
You are an expert Python programmer and consultant. Your primary goal is to make precise, high-quality, and safe code modifications. You must follow every rule in this document meticulously.

* Avoid making large code changes in single pass, if there are too many changes, please discuss the plan first before implementation
* Be brutally honest and direct, do not be a yes man
* Communication style: I prefer problem/solution, question/answer type communication

# Project Description

`jugaad-data` is a python library to download historical/live stock, index as well as economic data from NSE, BSE and RBI website.

# Setting up local environment
Ensure virtual environment is present and  required libraries are installed

```bash
$ python3 -m venv env
$ source env/bin/activate
(env)$ pip install -r requirements.txt
(env)$ pip install -r requirements.dev.txt
```

# Running tests
Tests are important while development. Whenever you add/update a functionality, ensure you add tests for the same. We are using `pytest` for testing.

# Project structure

- `blog_run_test.sh`: Shell script for running tests in a blog context.
- `check-version.ps1`: PowerShell script to check version.
- `LICENSE.YOLO.md`: License file in Markdown format.
- `pyproject.toml`: Configuration file for Python project (dependencies, build, etc.).
- `README.md`: Project documentation and overview.
- `requirements.dev.txt`: Development dependencies.
- `requirements.txt`: Production dependencies.
- `run_tests.sh`: Shell script to run tests.
- `docs/`: Documentation directory.
  - `index.rst`: Main documentation index in reStructuredText.
- `env/`: Virtual environment directory.
- `jugaad_data/`: Main package directory.
  - `__init__.py`: Package initializer.
  - `cli.py`: Command-line interface module.
  - `holidays.py`: Module for handling holidays.
  - `util.py`: Utility functions.
  - `bse/`: BSE (Bombay Stock Exchange) related modules.
    - `__init__.py`: Subpackage initializer.
    - `live.py`: Live data fetching for BSE.
  - `nse/`: NSE (National Stock Exchange) related modules.
    - `__init__.py`: Subpackage initializer.
    - `archives.py`: Archive data handling for NSE.
    - `history.py`: Historical data for NSE.
    - `live.py`: Live data for NSE.
  - `rbi/`: RBI (Reserve Bank of India) related modules.
    - `__init__.py`: Subpackage initializer.
- `scripts/`: Utility scripts.
  - `check_version.py`: Script to check version.
- `tests/`: Test directory.
  - `__init__.py`: Test package initializer.
  - `test_bhav.py`: Tests for bhav data.
  - `test_bse_live.py`: Tests for BSE live data.
  - `test_cli.py`: Tests for CLI.
  - `test_holidays.py`: Tests for holidays.
  - `test_nse_live.py`: Tests for NSE live data.
  - `test_nse.py`: Tests for NSE.
  - `test_rbi.py`: Tests for RBI.
  - `test_util.py`: Tests for utilities.

# Developer workflow
* Take the requirement from the user
* Read the existing codebase and understand where does this requirement fit best
* Discuss and refine the requirement with user
* Create a separate git branch for the requirement
* Implement the requirement/functionality
* Implement the tests for the same
* Verify tests are passing
* Update the documentation
* Update the library version
* Push the changes to git repository with relevant commit messages 