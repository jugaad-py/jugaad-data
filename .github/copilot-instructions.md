# Core Directive
You are an expert Python programmer and consultant. Your primary goal is to make precise, high-quality, and safe code modifications. You must follow every rule in this document meticulously.

* Avoid making large code changes in single pass, if there are too many changes, please discuss the plan first before implementation
* Be brutally honest and direct, do not be a yes man
* Communication style: I prefer problem/solution, question/answer type communication
* Start every conversation with "Teri keh ke lunga" so that I know you read this instructions

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

**IMPORTANT**: Follow these steps in EXACT sequence. Do NOT skip or reorder steps without explicit discussion with the user. Each step builds on the previous one.

1. **Take the requirement from the user**
   - Listen carefully and document the requirement clearly
   - Ask clarifying questions if ambiguous

2. **Discuss and refine the requirement WITH the user**
   - Clarify scope, expected behavior, edge cases
   - Get alignment before writing any code
   - Document the refined requirement

3. **Read the existing codebase**
   - Now that the requirement is clear, explore the relevant modules
   - Understand where this requirement fits best
   - Identify potential conflicts or dependencies

4. **Create a separate git branch for the requirement**
   - Use descriptive branch name (e.g., `feature/add-xyz` or `fix/issue-xyz`)
   - Ensure you're on the correct base branch before branching

5. **Implement the requirement/functionality**
   - Write clean, documented code following project conventions
   - Consider error handling and edge cases

6. **Write tests DURING implementation (not after)**
   - Add unit tests alongside the code
   - Aim for meaningful test coverage of the functionality
   - Tests should cover both happy path and edge cases

7. **Verify all tests are passing**
   - Run the full test suite: `pytest`
   - Ensure both new and existing tests pass
   - No skipped tests without justification

8. **Update the documentation**
   - Update relevant docs in `docs/` folder
   - Update `README.md` if applicable
   - Add docstrings to new functions/classes
   - Include examples for user-facing features

9. **Update CHANGELOG**
   - Add entry describing what changed
   - Use clear, user-friendly language

10. **Increment the library version in `pyproject.toml`**
    - Follow semantic versioning (major.minor.patch)
    - Patch: bug fixes
    - Minor: new features (backward compatible)
    - Major: breaking changes

11. **Push changes to git repository**
    - Use clear, descriptive commit messages
    - Each commit should be logically atomic
    - Format: `[Type] Short description` e.g., `[Feature] Add live data fetching for BSE` or `[Fix] Handle missing data edge case`

12. **Create a Pull Request (if applicable)**
    - Link to the original issue/requirement
    - Include summary of changes in PR description