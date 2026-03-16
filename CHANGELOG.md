# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.33.1] - 2026-03-16

### Fixed
- Issue #97: `derivatives_df()` and `derivatives_csv()` returning empty or failing with 404 error
  - NSE deprecated `/api/historical/fo/derivatives` endpoint
  - Now uses updated `/api/historicalOR/foCPV` endpoint
  - Added `year` parameter to API requests as required by new endpoint
  - Historical data availability limited to recent periods per NSE data retention

### Added
- Test coverage for `derivatives_df()` with both futures (FUTIDX) and options (OPTIDX) data
- Test coverage for `derivatives_raw()` with different instrument types
- Documentation note about historical data availability for derivatives

## [0.33.0] - 2026-03-16

### Changed
- **BREAKING CHANGE**: `stock_quote_fno()` now returns NSE NextApi response format (see API_REFERENCE.md)
  - **Old format**: Nested structure with `stocks[*].metadata` and `stocks[*].tradeInfo`
  - **New format**: Flat array structure with `data[*]` containing all contract info
  - Returns all available contracts (futures + all expiries of calls and puts) in single response
  - Each contract now includes comprehensive fields: `identifier`, `instrumentType`, `expiryDate`, `optionType`, `strikePrice`, `lastPrice`, `openInterest`, etc.
  - Response also includes `timestamp` field

### Fixed
- Issue #105: `stock_quote_fno()` returning empty data - NSE deprecated old `/api/quote-derivative` endpoint
  - Now uses NSE NextApi endpoint (`getSymbolDerivativesData`) which provides current derivatives data
  - Resolves `IndexError: list index out of range` when accessing `stocks[0]`

### Updated
- Enhanced test coverage: `test_stock_quote_fno()` now validates actual data presence, not just structure
- Updated API documentation with new response fields and format
- Updated LIVE_DATA_GUIDE with examples for processing new response format
- Updated QUICKSTART guide with new usage examples

## [0.32.0] - 2026-03-16

### Added
- New `NSEDailyReports` class to handle NSE daily-reports API (39+ report types)
- `NSEArchives.download_report()` method to download any NSE report by file key
- `NSEArchives.list_available_reports()` method to discover available report types
- Hybrid bhavcopy format support: UDiff (recent) + BHAVDATA-FULL (historical)
- Tests for new report discovery and download functionality

### Fixed
- Issue #81: NSE bhavcopy downloads failing for dates >= July 8, 2024 (BadZipFile error)
- Issue #83: Bhavcopy format change - implemented automatic fallback to BHAVDATA-FULL
- Bhavcopy now works for all dates using hybrid approach:
  - Recent dates (Jul 8, 2024+): Uses new UDiff format from daily-reports API
  - Historical dates: Uses BHAVDATA-FULL format (available for all dates)

### Changed
- `bhavcopy_raw()` now automatically handles both UDiff and BHAVDATA-FULL formats
- Data returned as-is per NSE updates (no backward compatibility guarantee)

## [0.31.2] - 2026-03-16

### Fixed
- Fixed NSE option chain APIs to work with new v3 endpoint
- Updated `index_option_chain()` and `equities_option_chain()` to use `/api/option-chain-v3` endpoint
- Added `option_chain_contract_info()` method to fetch available expiry dates
- Both option chain methods now accept optional `expiry` parameter, automatically defaulting to nearest available expiry
- Issue #112: Option chain tests were failing due to NSE API changes

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
