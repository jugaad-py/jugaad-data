# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.31.2] - 2026-03-14

### Fixed
- Fixed issue #112: NSE option chain tests failing due to empty API responses during market closure
- Implemented mocking for option chain tests to be market-hours independent
- Tests now use realistic fixture data instead of depending on live API responses

## [0.31.1] - 2026-03-14

### Changed
- Added guidelines for debug/test script cleanup after development
- Enhanced branch naming requirements to clearly reflect the problem being solved
- Improved developer workflow documentation with emphasis on branch naming conventions

## [0.31] - 2026-03-14

### Changed
- Refined developer workflow documentation with explicit step-by-step guide
- Improved clarity on workflow sequence and mandatory steps
- Added detailed descriptions and best practices for each workflow step
- Updated developer workflow to use GitHub CLI (gh) for PR creation
- Added detailed examples for gh pr create command
