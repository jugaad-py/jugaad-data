# Jugaad Data - API Reference

## Table of Contents

1. [NSE Live Data Module](#nse-live-data-module)
2. [NSE Historical Data Module](#nse-historical-data-module)
3. [BSE Module](#bse-module)
4. [RBI Module](#rbi-module)

---

## NSE Live Data Module

The `NSELive` class provides access to real-time market data from NSE.

### Initialization

```python
from jugaad_data.nse import NSELive

n = NSELive()
```

### Market Status and Indices

#### `market_status()`
Get status of different market segments.

```python
status = n.market_status()
# Returns list of market segments with status, index, and current value
# Includes: Capital Market, Currency, Commodity, Debt, Currency Futures
```

#### `all_indices()`
Get data for all indices at NSE.

```python
all_indices = n.all_indices()
# Returns dict with keys:
# - 'data': List of all indices with OHLC, PE, PB, DY values
# - 'timestamp': Last update time
# - 'advances': Number of stocks advanced
# - 'declines': Number of stocks declined
# - 'unchanged': Number of stocks unchanged
```

#### `live_index(symbol)`
Get detailed data for a specific index.

**Parameters:**
- `symbol` (str): Index name (e.g., "NIFTY 50", "NIFTY BANK")

**Returns:**
```python
{
    'name': str,                  # Index name
    'timestamp': str,             # Last update time
    'data': list,                 # OHLC and market data
    'metadata': dict,             # Repeated market data
    'marketStatus': dict,         # Market open/close status
    'advance': dict,              # Advances/declines
    'date30dAgo': str,           # 30-day performance
    'date365dAgo': str           # 1-year performance
}
```

#### `market_turnover()`
Get turnover across different market segments.

```python
turnover = n.market_turnover()
# Returns dict with 'data' containing:
# - Equities
# - Index Futures
# - Index Options
# - Stock Futures
# - Stock Options
# - Currency Futures
# - Currency Options
# - Commodity Futures
# - Commodity Options
# - Interest Rate Futures/Options
```

### Stock Data

#### `stock_quote(symbol)`
Get detailed quote for a stock.

**Parameters:**
- `symbol` (str): Stock symbol (e.g., "HDFC", "SBIN", "RELIANCE")

**Returns:**
```python
{
    'priceInfo': dict,           # OHLC, change, VWAP, price bands
    'info': dict,                # Company info, series, ISINflagsuspension
    'metadata': dict,            # ISIN, listing date, industry, PE ratios
    'securityInfo': dict,        # Board status, derivatives, face value
    'preOpenMarket': dict,       # Pre-open prices, order book, IEP
    'sddDetails': dict,          # SDD status
    'industryInfo': dict,        # Sector, macro data
}
```

#### `tick_data(symbol)`
Get minute-by-minute tick data for a stock.

**Parameters:**
- `symbol` (str): Stock symbol

**Returns:**
```python
{
    'grapthData': list,          # List of [timestamp (ms), price] tuples
    'timestamp': str
}
```

#### `trade_info(symbol)`
Get detailed trade information for a stock.

**Parameters:**
- `symbol` (str): Stock symbol

**Returns:**
```python
{
    'noBlockDeals': bool,
    'bulkBlockDeals': list,
    'marketDeptOrderBook': dict, # Order book with bid/ask
    'securityWiseDP': dict,      # Delivery info
}
```

#### `stock_quote_fno(symbol)` - [BREAKING CHANGE v0.33]
Get futures and options quotes for a symbol.

**Parameters:**
- `symbol` (str): Stock or index symbol (e.g., 'RELIANCE', 'NIFTY')

**Returns:**
```python
{
    'data': [
        {
            'identifier': 'FUTSTKRELIANCE30-Mar-2026XX0.00',
            'instrumentType': 'FUTSTK',           # FUTSTK (Futures) or OPTSTK (Options)
            'underlying': 'RELIANCE',
            'expiryDate': '30-Mar-2026',
            'optionType': 'XX',                  # XX (Futures), CE (Call), PE (Put)
            'strikePrice': '0.00',
            'lastPrice': 2850.5,
            'change': 15.2,
            'pchange': 0.54,
            'openPrice': 2835.0,
            'highPrice': 2860.0,
            'lowPrice': 2820.0,
            'closePrice': 2835.3,
            'prevClose': 2835.3,
            'totalTradedVolume': 45678,
            'totalTurnover': 1296789420,
            'openInterest': 123456,
            'changeinOpenInterest': 1234,
            'pchangeinOpenInterest': 1.01,
            'underlyingValue': 2850.5,
            'volumeFreezeQuantity': 240001,
            'ticksize': 0.05,
            ...other fields
        },
        ...more contracts
    ],
    'timestamp': '16-Mar-2026 15:30:00'
}
```

**Note:** Response includes all available contracts (futures + all expiries of calls and puts) for the given symbol.

### Option Chains

#### `index_option_chain(symbol, expiry_date=None)`
Get option chain for an index.

**Parameters:**
- `symbol` (str): Index symbol (e.g., "NIFTY")
- `expiry_date` (str, optional): Filter by expiry date

**Returns:**
```python
{
    'records': dict,             # Metadata and expiry dates
    'filtered': dict,            # Filtered option chain data
    # Each row contains:
    # - strikePrice
    # - CE (Call option data)
    # - PE (Put option data)
}
```

#### `equities_option_chain(symbol, expiry_date=None)`
Get option chain for equity stock.

**Parameters:**
- `symbol` (str): Stock symbol

#### `currency_option_chain(symbol, expiry_date=None)`
Get option chain for currency pair.

**Parameters:**
- `symbol` (str): Currency pair (e.g., "USDINR")

### Derivatives Data

#### `eq_derivative_turnover()`
Get equity derivative turnover data.

```python
turnover = n.eq_derivative_turnover()
# Returns derivatives ordered by turnover
# Each contract shows:
# - identifier, instrumentType, expiryDate
# - lastPrice, change, pChange
# - numberOfContractsTraded, totalTurnover
# - openInterest, underlyingValue
```

### Market Data Indices

#### `get_expiry_dates(date, contract_type=None)`
Get available contract expiry dates for a given date.

**Parameters:**
- `date` (date): Reference date
- `contract_type` (str, optional): Filter by type (e.g., "FUTSTK", "OPTIDX")

**Returns:**
```python
list  # List of datetime.date objects for contract expiries
```

### Corporate Announcements

#### `corporate_announcements(symbol=None, from_date=None, to_date=None)`
Get corporate announcements/disclosures.

**Parameters:**
- `symbol` (str, optional): Stock symbol filter
- `from_date` (date, optional): Start date
- `to_date` (date, optional): End date

**Returns:**
```python
{
    'an_dt': str,                # Announcement datetime
    'symbol': str,               # Stock symbol
    'desc': str,                 # Description type
    'attchmntText': str,        # Announcement text
    'attchmntFile': str,        # PDF URL
    'fileSize': str,            # File size
    'sm_name': str,             # Company name
    'sm_isin': str,             # ISIN
    'sort_date': str            # Sort timestamp
}
```

---

## NSE Historical Data Module

Download historical OHLC data and bhavcopies.

### Bhavcopies

#### `bhavcopy_save(date, path)`
Download equity bhavcopy for a date.

**Parameters:**
- `date` (datetime.date): Date to download
- `path` (str): Directory to save CSV file

**File format:** `cm{date}bhav.csv`

#### `full_bhavcopy_save(date, path)`
Download full equity bhavcopy (includes delivery data).

**Parameters:**
- `date` (datetime.date): Date to download
- `path` (str): Directory to save CSV file

**File format:** `cm{date}bhav.csv` with delivery percentage

#### `bhavcopy_fo_save(date, path)`
Download futures & options bhavcopy.

**Parameters:**
- `date` (datetime.date): Date to download
- `path` (str): Directory to save CSV file

**File format:** `fo{date}bhav.csv`

#### `bhavcopy_index_save(date, path)`
Download index bhavcopy.

**Parameters:**
- `date` (datetime.date): Date to download
- `path` (str): Directory to save CSV file

**File format:** `ind{date}bhav.csv`

### Historical Stock Data

#### `stock_df(symbol, from_date, to_date, series="EQ")`
Download historical stock data as pandas DataFrame.

**Parameters:**
- `symbol` (str): Stock symbol
- `from_date` (datetime.date): Start date
- `to_date` (datetime.date): End date
- `series` (str): Series type - "EQ" (default), "BE", etc.

**Returns:** pandas DataFrame with columns:
```
DATE, SERIES, OPEN, HIGH, LOW, PREV. CLOSE, LTP, CLOSE, 
VWAP, 52W H, 52W L, VOLUME, VALUE, NO OF TRADES, SYMBOL
```

#### `stock_csv(symbol, from_date, to_date, series="EQ", output=None)`
Download historical stock data and save to CSV.

**Parameters:**
- Same as `stock_df()`
- `output` (str): Path for output CSV file

### Historical Index Data

#### `index_df(symbol, from_date, to_date)`
Download historical index data as pandas DataFrame.

**Parameters:**
- `symbol` (str): Index name (e.g., "NIFTY 50")
- `from_date` (datetime.date): Start date
- `to_date` (datetime.date): End date

**Returns:** DataFrame with columns:
```
Index Name, INDEX_NAME, HistoricalDate, OPEN, HIGH, LOW, CLOSE
```

#### `index_csv(symbol, from_date, to_date, output=None)`
Download historical index data and save to CSV.

### Derivatives Data

#### `expiry_dates(date, contract_type=None)`
Get available expiry dates for contracts.

**Parameters:**
- `date` (datetime.date): Reference date
- `contract_type` (str, optional): Filter (e.g., "FUTSTK", "OPTIDX", "OPTIDX")

**Returns:**
```python
list  # List of datetime.date objects
```

#### `derivatives_df(symbol, from_date, to_date, expiry_date, instrument_type, option_type=None, strike_price=None)`
Download derivatives historical data as DataFrame.

**Parameters:**
- `symbol` (str): Stock/Index symbol
- `from_date` (datetime.date): Start date
- `to_date` (datetime.date): End date
- `expiry_date` (datetime.date): Contract expiry date
- `instrument_type` (str): "FUTSTK", "FUTIDX", "OPTSTK", "OPTIDX"
- `option_type` (str): "CE" or "PE" (for options only)
- `strike_price` (float): Strike price (for options only)

**Returns:** DataFrame with contract-specific columns

#### `derivatives_csv(symbol, from_date, to_date, expiry_date, instrument_type, option_type=None, strike_price=None, output=None)`
Download derivatives data and save to CSV.

**Parameters:**
- Same as `derivatives_df()`
- `output` (str): Path for output CSV file

**Note on Historical Data:**
- As of v0.34.0+, the derivatives API endpoint has been updated to use NSE's new `/api/historicalOR/foCPV` endpoint
- Historical data is available for recent periods (typically current and past few months)
- Data availability depends on NSE's data retention policies
- For very old historical data (prior to ~6 months), data may not be available

### NSE Daily Reports

#### `list_available_reports()`
Discover all available daily reports from NSE.

**Parameters:** None

**Returns:**
```python
list  # List of dictionaries with 'key' and 'name' for each report
```

**Example:**
```python
from jugaad_data.nse import list_available_reports

reports = list_available_reports()
# Returns: [{'key': 'CM-VOLATILITY', 'name': 'CM Volatility'}, ...]
```

#### `download_report(report_key, to_date=None, output=None)`
Download any NSE daily report (39+ report types available).

**Parameters:**
- `report_key` (str): Report key (e.g., "CM-VOLATILITY", "NIFTY-50-ADVANCE-DECLINE")
- `to_date` (datetime.date, optional): Date for report (defaults to NSE current date)
- `output` (str, optional): Path for output file

**Returns:** File saved at `output` path or temp directory

**Example:**
```python
from jugaad_data.nse import download_report

# List available reports first
download_report("CM-VOLATILITY", output="/path/to/file.csv")
```

#### `stock_df(symbol, from_date, to_date)` - Format Note
As of July 8, 2024, NSE transitioned from direct CSV format to compressed UDiff format. The library handles this automatically:
- Dates >= July 8, 2024: Returns UDiff format (newer column structure)
- Historical dates: Falls back to BHAVDATA-FULL format

Both formats are returned as raw CSV data with no column mapping. See [HISTORICAL_DATA_GUIDE](HISTORICAL_DATA_GUIDE.md) for detailed column specifications.

---

## BSE Module

Currently includes live data fetching for BSE stocks.

```python
from jugaad_data.bse import BSELive

# Note: BSE module implementation varies by version
```

---

## RBI Module

Fetch economic data from Reserve Bank of India website.

### Initialization

```python
from jugaad_data.rbi import RBI

r = RBI()
```

### Methods

#### `current_rates()`
Get current economic rates and indices from RBI.

**Returns:**
```python
{
    'Policy Repo Rate': str,          # e.g., "4.00%"
    'Reverse Repo Rate': str,
    'Marginal Standing Facility Rate': str,
    'Bank Rate': str,
    'CRR': str,                       # Cash Reserve Ratio
    'SLR': str,                       # Statutory Liquidity Ratio
    'Base Rate': str,
    'MCLR (Overnight)': str,
    'Savings Deposit Rate': str,
    'Term Deposit Rate > 1 Year': str,
    'Call Rates': str,
    '91 day T-bills': str,            # Treasury bills
    '182 day T-bills': str,
    '364 day T-bills': str,
    'Government Securities': dict,     # GS rates by maturity
    'S&P BSE Sensex': str,
    'Nifty 50': str
}
```

---

## Data Structures

### Price Information

Standard price info returned in live quotes:

```python
{
    'lastPrice': float,
    'change': float,
    'pChange': float,              # Percentage change
    'previousClose': float,
    'open': float,
    'high': float,
    'low': float,
    'close': float,
    'vwap': float,                 # Volume weighted average price
    'lowerCP': str,                # Lower circuit
    'upperCP': str,                # Upper circuit
    'pPriceBand': str,
    'basePrice': float,
    'weekHighLow': dict,
    'yearHighLow': dict,
    'intraDayHighLow': dict
}
```

### Market Depth

Order book information:

```python
{
    'totalBuyQuantity': int,
    'totalSellQuantity': int,
    'bid': list,                   # Bid levels
    'ask': list,                   # Ask levels
    # Each level: {'price': float, 'quantity': int}
}
```

---

## Error Handling

Common exceptions:

```python
try:
    df = stock_df(symbol="INVALID", from_date=date(2020,1,1), to_date=date(2020,1,31))
except Exception as e:
    print(f"Error: {e}")
```

---

## Rate Limiting

- NSE may have rate limits during high traffic
- Add delays between requests for production systems
- Corporate actions and holidays may affect data availability

---

## Date Formats

All dates should be `datetime.date` objects:

```python
from datetime import date
from_date = date(2020, 1, 1)
to_date = date(2020, 12, 31)
```

Not strings: Use `date(2020,1,1)` not `"2020-01-01"`

---

## Additional Resources

- GitHub: https://github.com/jugaad-py/jugaad-data
- Issues & Feature Requests: https://github.com/jugaad-py/jugaad-data/issues
