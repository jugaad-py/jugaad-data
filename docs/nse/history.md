# NSE History

The NSE History module provides access to historical time series data for stocks, indices, and derivatives from the National Stock Exchange.

## Classes

### NSEHistory Class

Fetches historical time series data for stocks and derivatives.

```python
from jugaad_data.nse.history import NSEHistory

history = NSEHistory()
```

#### Attributes

- `base_url` (str): "https://www.nseindia.com"
- `cache_dir` (str): Cache directory path (default: ".cache")
- `workers` (int): Number of worker threads (default: 2)
- `use_threads` (bool): Enable threaded downloads (default: True)
- `show_progress` (bool): Show progress indicators (default: False)
- `ssl_verify` (bool): SSL certificate verification (default: True)

#### Methods

##### `stock_raw(symbol, from_date, to_date, series="EQ")`
Fetch raw historical stock data.

**Parameters:**
- `symbol` (str): Stock symbol (e.g., "SBIN", "RELIANCE")
- `from_date` (date): Start date
- `to_date` (date): End date  
- `series` (str): Series type (default: "EQ")

**Returns:**
- list[dict]: List of daily data records

**Example:**
```python
from datetime import date
from jugaad_data.nse.history import NSEHistory

history = NSEHistory()
data = history.stock_raw("SBIN", date(2020, 1, 1), date(2020, 1, 31))
```

##### `derivatives_raw(symbol, from_date, to_date, expiry_date, instrument_type, strike_price, option_type)`
Fetch raw historical derivatives data.

**Parameters:**
- `symbol` (str): Underlying symbol
- `from_date` (date): Start date
- `to_date` (date): End date
- `expiry_date` (date): Contract expiry date
- `instrument_type` (str): "FUTSTK", "FUTIDX", "OPTSTK", "OPTIDX"
- `strike_price` (float): Strike price (required for options)
- `option_type` (str): "CE" or "PE" (required for options)

**Returns:**
- list[dict]: List of daily derivatives data records

### NSEIndexHistory Class

Fetches historical index data from NSE Indices website.

```python
from jugaad_data.nse.history import NSEIndexHistory

index_history = NSEIndexHistory()
```

#### Attributes

- `base_url` (str): "https://niftyindices.com"

#### Methods

##### `index_raw(symbol, from_date, to_date)`
Fetch raw historical index data.

**Parameters:**
- `symbol` (str): Index name (e.g., "NIFTY 50", "NIFTY BANK")
- `from_date` (date): Start date
- `to_date` (date): End date

**Returns:**
- list[dict]: List of daily index data records

##### `index_pe_raw(symbol, from_date, to_date)`
Fetch raw historical index PE/PB data.

**Parameters:**
- `symbol` (str): Index name
- `from_date` (date): Start date  
- `to_date` (date): End date

**Returns:**
- list[dict]: List of daily PE/PB data records

## Module-level Functions

### Stock Data Functions

#### `stock_raw(symbol, from_date, to_date, series="EQ")`
Get raw stock data using the default NSEHistory instance.

#### `stock_df(symbol, from_date, to_date, series="EQ")`
Get stock data as a pandas DataFrame.

**Returns:**
- pandas.DataFrame: Stock data with columns:
  - DATE, SERIES, OPEN, HIGH, LOW, PREV. CLOSE, LTP, CLOSE
  - VWAP, 52W H, 52W L, VOLUME, VALUE, NO OF TRADES, SYMBOL

**Example:**
```python
from datetime import date
from jugaad_data.nse import stock_df

df = stock_df("SBIN", date(2020, 1, 1), date(2020, 1, 31))
print(df.head())
```

#### `stock_csv(symbol, from_date, to_date, series="EQ", output="", show_progress=True)`
Save stock data to CSV file.

**Parameters:**
- `output` (str): Output file path (auto-generated if empty)
- `show_progress` (bool): Show download progress bar

**Returns:**
- str: Path to saved CSV file

### Index Data Functions

#### `index_raw(symbol, from_date, to_date)`
Get raw index data using the default NSEIndexHistory instance.

#### `index_df(symbol, from_date, to_date)`  
Get index data as a pandas DataFrame.

**Returns:**
- pandas.DataFrame: Index data with columns:
  - INDEX_NAME, HistoricalDate, OPEN, HIGH, LOW, CLOSE

**Example:**
```python
from datetime import date
from jugaad_data.nse import index_df

df = index_df("NIFTY 50", date(2020, 1, 1), date(2020, 1, 31))
print(df.head())
```

#### `index_csv(symbol, from_date, to_date, output="", show_progress=False)`
Save index data to CSV file.

#### `index_pe_raw(symbol, from_date, to_date)`
Get raw index PE/PB data.

#### `index_pe_df(symbol, from_date, to_date)`
Get index PE/PB data as a pandas DataFrame.

**Returns:**
- pandas.DataFrame: PE/PB data with columns:
  - Index Name, DATE, pe, pb, divYield

### Derivatives Data Functions

#### `derivatives_raw(symbol, from_date, to_date, expiry_date, instrument_type, strike_price, option_type)`
Get raw derivatives data using the default NSEHistory instance.

#### `derivatives_df(symbol, from_date, to_date, expiry_date, instrument_type, strike_price=None, option_type=None)`
Get derivatives data as a pandas DataFrame.

**Returns:**
- pandas.DataFrame: Derivatives data with columns varying by instrument type

**Futures Columns:**
- DATE, EXPIRY, OPEN, HIGH, LOW, CLOSE, LTP, SETTLE PRICE
- TOTAL TRADED QUANTITY, MARKET LOT, PREMIUM VALUE, OPEN INTEREST, CHANGE IN OI, SYMBOL

**Options Columns:**
- DATE, EXPIRY, OPTION TYPE, STRIKE PRICE, OPEN, HIGH, LOW, CLOSE, LTP, SETTLE PRICE
- TOTAL TRADED QUANTITY, MARKET LOT, PREMIUM VALUE, OPEN INTEREST, CHANGE IN OI, SYMBOL

#### `derivatives_csv(symbol, from_date, to_date, expiry_date, instrument_type, strike_price=None, option_type=None, output="", show_progress=False)`
Save derivatives data to CSV file.

## Data Types and Processing

### Data Type Conversion

The module uses utility functions for data type conversion:

- `ut.np_date()` - Convert to numpy datetime64
- `ut.np_float()` - Convert to numpy float64  
- `ut.np_int()` - Convert to numpy int64

### Date Range Optimization

Large date ranges are automatically broken into monthly chunks for efficient API usage:

```python
# Internally breaks 2020-2021 range into monthly requests
df = stock_df("SBIN", date(2020, 1, 1), date(2021, 12, 31))
```

### Threading and Performance

- Multiple worker threads for parallel month-wise downloads
- Configurable worker count via `NSEHistory.workers`
- Progress bars for long-running operations

## Error Handling

### Common Exceptions

- **ModuleNotFoundError**: Pandas not installed (for DataFrame functions)
- **Exception**: Invalid instrument_type for derivatives
- **Exception**: Missing strike_price or option_type for options

### Validation

- Instrument types are validated against: ["OPTIDX", "OPTSTK", "FUTIDX", "FUTSTK"]
- Options require both strike_price and option_type parameters
- Automatic date range validation and breaking

## Caching Strategy

### Cache Key Generation
- Historical data cached by symbol, date range, and other parameters
- Monthly data chunks cached separately for optimal reuse
- Cache keys generated from function parameters

### Cache Location
- Default: `.cache` directory in current working directory
- Override with `J_CACHE_DIR` environment variable
- Organized by app name and parameter combinations

## Examples

### Basic Stock Data

```python
from datetime import date
from jugaad_data.nse import stock_df

# Get HDFC stock data for January 2020
df = stock_df("HDFC", date(2020, 1, 1), date(2020, 1, 31))

# Basic analysis
print(f"Average closing price: {df['CLOSE'].mean():.2f}")
print(f"Highest price: {df['HIGH'].max():.2f}")
print(f"Total volume: {df['VOLUME'].sum():,}")
```

### Index Analysis

```python
from jugaad_data.nse import index_df, index_pe_df

# Get NIFTY 50 price data
price_df = index_df("NIFTY 50", date(2020, 1, 1), date(2020, 12, 31))

# Get NIFTY 50 valuation metrics
pe_df = index_pe_df("NIFTY 50", date(2020, 1, 1), date(2020, 12, 31))

# Merge data
merged = price_df.merge(pe_df, left_on='HistoricalDate', right_on='DATE')
```

### Options Data Analysis

```python
from jugaad_data.nse import derivatives_df

# Get NIFTY call option data
call_df = derivatives_df(
    symbol="NIFTY",
    from_date=date(2020, 1, 1),
    to_date=date(2020, 1, 31), 
    expiry_date=date(2020, 1, 30),
    instrument_type="OPTIDX",
    strike_price=12000.0,
    option_type="CE"
)

# Analyze option premium
print(f"Option premium range: {call_df['CLOSE'].min():.2f} - {call_df['CLOSE'].max():.2f}")
```

### Bulk Data Download with Progress

```python
from jugaad_data.nse import stock_csv
from datetime import date

# Download multiple stocks with progress bars
stocks = ["SBIN", "HDFC", "ICICIBANK", "RELIANCE"]

for stock in stocks:
    output_file = f"{stock}_2020_data.csv"
    stock_csv(
        symbol=stock,
        from_date=date(2020, 1, 1),
        to_date=date(2020, 12, 31),
        output=output_file,
        show_progress=True
    )
    print(f"Saved {stock} data to {output_file}")
```