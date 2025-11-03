# NSE Module

The NSE (National Stock Exchange) module provides comprehensive access to Indian equity, derivatives, and index data from the National Stock Exchange.

## Submodules

### [Archives](archives.md)
Historical data downloads including bhavcopy files, bulk deals, and derivatives data.

### [History](history.md) 
Time series data for stocks, indices, and derivatives with support for various time ranges.

### [Live](live.md)
Real-time market data including stock quotes, option chains, and market status.

## Quick Examples

### Historical Stock Data
```python
from jugaad_data.nse import stock_df, stock_csv
from datetime import date

# Get DataFrame
df = stock_df(symbol="SBIN", from_date=date(2020,1,1), 
              to_date=date(2020,1,30), series="EQ")

# Save to CSV
stock_csv(symbol="SBIN", from_date=date(2020,1,1), 
          to_date=date(2020,1,30), output="sbin_data.csv")
```

### Live Market Data
```python
from jugaad_data.nse import NSELive

nse = NSELive()
quote = nse.stock_quote("RELIANCE")
print(f"Current Price: {quote['priceInfo']['lastPrice']}")
```

### Bhavcopy Downloads
```python
from jugaad_data.nse import bhavcopy_save
from datetime import date

# Download equity bhavcopy
bhavcopy_save(date(2020,1,1), "/path/to/save/")
```

## Available Functions

### Top-level Functions

#### Stock Data Functions
- `stock_raw(symbol, from_date, to_date, series="EQ")` - Raw stock data
- `stock_df(symbol, from_date, to_date, series="EQ")` - Stock data as pandas DataFrame  
- `stock_csv(symbol, from_date, to_date, series="EQ", output="", show_progress=True)` - Save stock data to CSV

#### Index Data Functions
- `index_raw(symbol, from_date, to_date)` - Raw index data
- `index_df(symbol, from_date, to_date)` - Index data as pandas DataFrame
- `index_csv(symbol, from_date, to_date, output="", show_progress=False)` - Save index data to CSV
- `index_pe_raw(symbol, from_date, to_date)` - Raw index PE/PB data  
- `index_pe_df(symbol, from_date, to_date)` - Index PE/PB data as DataFrame

#### Derivatives Data Functions
- `derivatives_raw(symbol, from_date, to_date, expiry_date, instrument_type, strike_price, option_type)` - Raw derivatives data
- `derivatives_df(symbol, from_date, to_date, expiry_date, instrument_type, strike_price=None, option_type=None)` - Derivatives data as DataFrame
- `derivatives_csv(symbol, from_date, to_date, expiry_date, instrument_type, strike_price=None, option_type=None, output="", show_progress=False)` - Save derivatives data to CSV

#### Archive Functions
- `bhavcopy_raw(dt)` - Raw bhavcopy text for a date
- `bhavcopy_save(dt, dest, skip_if_present=True)` - Download and save bhavcopy
- `full_bhavcopy_raw(dt)` - Raw full bhavcopy text
- `full_bhavcopy_save(dt, dest, skip_if_present=True)` - Download and save full bhavcopy
- `bhavcopy_fo_raw(dt)` - Raw F&O bhavcopy text
- `bhavcopy_fo_save(dt, dest, skip_if_present=True)` - Download and save F&O bhavcopy
- `bhavcopy_index_raw(dt)` - Raw index bhavcopy text
- `bhavcopy_index_save(dt, dest, skip_if_present=True)` - Download and save index bhavcopy
- `expiry_dates(dt, instrument_type="", symbol="", contracts=0)` - Get expiry dates from F&O bhavcopy

## Parameters

### Common Parameters

- **symbol** (str): Stock/Index symbol (e.g., "SBIN", "NIFTY 50")
- **from_date** (date): Start date for data range
- **to_date** (date): End date for data range  
- **series** (str): Series type (default: "EQ" for equity)
- **dt** (date): Specific date for bhavcopy downloads
- **dest** (str): Destination directory path for downloads
- **output** (str): Output file path for CSV exports

### Derivatives Parameters

- **expiry_date** (date): Expiry date for derivatives contracts
- **instrument_type** (str): Type of instrument
  - "FUTSTK" - Stock futures
  - "FUTIDX" - Index futures  
  - "OPTSTK" - Stock options
  - "OPTIDX" - Index options
- **strike_price** (float): Strike price for options (required for options)
- **option_type** (str): Option type "CE" or "PE" (required for options)

### Optional Parameters

- **show_progress** (bool): Show download progress bar (default varies by function)
- **skip_if_present** (bool): Skip download if file exists (default: True)

## Classes

- **[NSEHistory](history.md#nsehistory-class)** - Historical data fetching
- **[NSELive](live.md#nselive-class)** - Live market data
- **[NSEArchives](archives.md#nsearchives-class)** - Archive data downloads
- **[NSEIndicesArchives](archives.md#nseindicesarchives-class)** - Index archive data
- **[NSEIndexHistory](history.md#nseindexhistory-class)** - Index historical data

## Data Format

### Stock Data Columns
- DATE, SERIES, OPEN, HIGH, LOW, PREV. CLOSE, LTP, CLOSE
- VWAP, 52W H, 52W L, VOLUME, VALUE, NO OF TRADES, SYMBOL

### Index Data Columns  
- INDEX_NAME, HistoricalDate, OPEN, HIGH, LOW, CLOSE

### Derivatives Data Columns

**Futures:**
- DATE, EXPIRY, OPEN, HIGH, LOW, CLOSE, LTP, SETTLE PRICE
- TOTAL TRADED QUANTITY, MARKET LOT, PREMIUM VALUE, OPEN INTEREST, CHANGE IN OI, SYMBOL

**Options:**  
- DATE, EXPIRY, OPTION TYPE, STRIKE PRICE, OPEN, HIGH, LOW, CLOSE, LTP, SETTLE PRICE
- TOTAL TRADED QUANTITY, MARKET LOT, PREMIUM VALUE, OPEN INTEREST, CHANGE IN OI, SYMBOL

## Error Handling

Common exceptions you may encounter:

- **ModuleNotFoundError**: When pandas is required but not installed
- **ReadTimeout**: Network timeout, often due to holidays or server issues
- **Exception**: Invalid instrument types or missing required parameters for derivatives

## Caching

The NSE module implements intelligent caching:
- Historical data is cached per month to optimize large date range requests
- Live data has configurable timeout (default: 5 seconds)
- Cache directory can be set via `J_CACHE_DIR` environment variable