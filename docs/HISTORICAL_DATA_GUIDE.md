# Jugaad Data - Historical Data Guide

A comprehensive guide to downloading historical market data using `jugaad-data`.

## Table of Contents

1. [Bhavcopies](#bhavcopies)
2. [Historical Stock Data](#historical-stock-data)
3. [Historical Index Data](#historical-index-data)
4. [Historical Derivatives Data](#historical-derivatives-data)
5. [Command Line Interface](#command-line-interface)
6. [Data Processing Examples](#data-processing-examples)
7. [Best Practices](#best-practices)

---

## Bhavcopies

Bhavcopies are complete daily market snapshots published by stock exchanges after market close. They contain all traded contracts with their OHLC prices.

### Format Changes (July 8, 2024)

On July 8, 2024, NSE transitioned from the old ZIP-based bhavcopy format to the **Unified Distilled File Format (UDiff)**. The library now automatically handles both formats:

- **Recent Dates (≥ July 8, 2024):** Uses UDiff format from NSE's daily-reports API
  - Format: More comprehensive data structure
  - Availability: Current day + previous trading day (via API)
  
- **Historical Dates (< July 8, 2024):** Uses BHAVDATA-FULL format
  - Format: CSV with delivery information
  - Availability: All historical dates
  - No ZIP decompression required

**No action needed on your part** - the library automatically chooses the best available format!

### Types of Bhavcopies

1. **Equity Bhavcopy** - All equity securities traded on NSE
2. **Full Bhavcopy** - Equity bhavcopy with delivery information
3. **F&O Bhavcopy** - Futures & Options contracts
4. **Index Bhavcopy** - Index data snapshots

### Download Equity Bhavcopy

```python
from datetime import date
from jugaad_data.nse import bhavcopy_save

# Download for specific date (works for all dates, automatic format selection)
bhavcopy_save(date(2020, 1, 1), "/path/to/directory")
bhavcopy_save(date(2024, 9, 15), "/path/to/directory")  # Uses UDiff if API available, else BHAVDATA-FULL

# Download for date range
from datetime import timedelta
start_date = date(2024, 1, 1)
end_date = date(2024, 12, 31)
current = start_date
while current <= end_date:
    try:
        bhavcopy_save(current, "/path/to/directory")
        print(f"Downloaded bhavcopy for {current}")
    except:
        pass  # Holiday or weekend
    current += timedelta(days=1)
```

**Output file:** `cm01Jan2020bhav.csv` or `cm15Sep2024bhav.csv`

**CSV Columns:**
For historical dates (BHAVDATA-FULL format):
```
SYMBOL, SERIES, DATE, PREV_CLOSE, OPEN_PRICE, HIGH_PRICE, LOW_PRICE, 
LAST_PRICE, CLOSE_PRICE, AVG_PRICE, TTL_TRD_QNTY, TURNOVER_LACS, 
NO_OF_TRADES, DELIV_QTY, DELIV_PER
```

For recent dates (UDiff format):
```
TradDt, BizDt, Sgmt, Src, FinInstrmTp, FinInstrmId, ISIN, TckrSymb, 
SctySrs, XpryDt, ... (enhanced data structure)
```

### Download Full Bhavcopy (with Delivery Data)

```python
from jugaad_data.nse import full_bhavcopy_save

# Includes delivery quantity percentage
full_bhavcopy_save(date(2020, 1, 1), "/path/to/directory")
```

**Additional columns in full bhavcopy:**
```
Delivery Quantity %
```

### Download Other NSE Reports (39+ types available)

The library now provides access to 39+ NSE reports through the daily-reports API:

#### List Available Reports

```python
from jugaad_data.nse import NSEArchives

nse = NSEArchives()

# See all available reports
reports = nse.list_available_reports()

for file_key, info in reports.items():
    print(f"{file_key}: {info['displayName']}")
    print(f"  Available dates: {[d['date'] for d in info['dates']]}")
```

#### Download Specific Reports

```python
from jugaad_data.nse import NSEArchives

nse = NSEArchives()

# Download volatility data
info = nse.download_report('CM-VOLATILITY', "/path/to/save")
print(f"Downloaded: {info['file_name']}")
print(f"Trading date: {info['trading_date']}")

# Other available reports:
# 'CM-UDIFF-BHAVCOPY-CSV'   - UDiff format bhavcopy (zip)
# 'CM-BULK-DEAL'            - Bulk deals data
# 'CM-BLOCK-DEAL'           - Block deals data
# 'CM-SHORT-SELLING'        - Short selling data
# 'CM-VOLATILITY'           - Daily volatility
# 'CM-CIRCUIT'              - Circuit breaker updates
# ... and 33+ more report types
```

**Return Value:**
```python
{
    'file_path': '/path/to/save/filename.csv',  # Local file path
    'file_name': 'CMVOLT_13032026.CSV',         # Actual file name from NSE
    'trading_date': '13-Mar-2026',              # Trading date of report
    'size': '292.78 KB',                        # File size
    'cached': False                             # Whether file was cached
}
```

### Download F&O Bhavcopy

```python
from jugaad_data.nse import bhavcopy_fo_save

# Download for specific date
bhavcopy_fo_save(date(2020, 1, 1), "/path/to/directory")
```

**Output file:** `fo01Jan2020bhav.csv`

**CSV Columns:**
```
INSTRUMENT, SYMBOL, EXPIRY, STRIKE, OPTTYPE, OPEN, HIGH, LOW, CLOSE, 
SETTLE, CONTRACTS, VALUE, OPENINT, FILENAME, ISIN
```

### Download Index Bhavcopy

```python
from jugaad_data.nse import bhavcopy_index_save

# Download for specific date
bhavcopy_index_save(date(2020, 1, 1), "/path/to/directory")
```

**Output file:** `ind01Jan2020bhav.csv`

### Batch Download Bhavcopies

```python
from datetime import date, timedelta
from jugaad_data.nse import bhavcopy_save

start_date = date(2020, 1, 1)
end_date = date(2020, 1, 31)

current = start_date
while current <= end_date:
    try:
        bhavcopy_save(current, "/path/to/directory")
        print(f"Downloaded bhavcopy for {current}")
    except Exception as e:
        print(f"Skipped {current}: {e}")  # Holiday/weekend
    
    current += timedelta(days=1)
```

---

## Historical Stock Data

### Download as Pandas DataFrame

```python
from datetime import date
from jugaad_data.nse import stock_df

# Download historical data for SBIN from Jan 1-30, 2020
df = stock_df(
    symbol="SBIN",
    from_date=date(2020, 1, 1),
    to_date=date(2020, 1, 30),
    series="EQ"
)

print(df.head())
print(df.shape)
print(df.dtypes)
```

### DataFrame Structure

**Columns returned:**

```
DATE            - Trading date
SERIES          - Series type (EQ, BE, etc.)
OPEN            - Opening price
HIGH            - Day high
LOW             - Day low
PREV. CLOSE     - Previous close
LTP             - Last traded price
CLOSE           - Closing price
VWAP            - Volume weighted average price
52W H           - 52-week high
52W L           - 52-week low
VOLUME          - Total traded volume
VALUE           - Total traded value
NO OF TRADES    - Number of trades
SYMBOL          - Stock symbol
```

**Example output:**
```
        DATE SERIES    OPEN    HIGH     LOW  PREV. CLOSE     LTP   CLOSE
0 2020-01-30     EQ  316.75  316.75  305.65       316.45  310.00  310.70
1 2020-01-29     EQ  317.85  319.70  315.55       315.10  316.95  316.45
2 2020-01-28     EQ  317.95  320.00  311.05       316.20  316.40  315.10

     VWAP  52W H   52W L    VOLUME         VALUE  NO OF TRADES SYMBOL
0  311.18  373.8  244.35  35802330  1.114102e+10        227687   SBIN
1  317.75  373.8  244.35  23914114  7.598704e+09        143297   SBIN
2  316.67  373.8  244.35  26488426  8.388015e+09        173879   SBIN
```

### Download and Save to CSV

```python
from jugaad_data.nse import stock_csv

# Download and save directly to CSV
stock_csv(
    symbol="SBIN",
    from_date=date(2020, 1, 1),
    to_date=date(2020, 1, 30),
    series="EQ",
    output="/path/to/SBIN_2020_01.csv"
)
```

### Series Types

Common series values:
- `EQ` - Equity (main series)
- `BE` - Bulk/Block deals
- `GR` - Group contracts
- `ST` - Stock lending & borrowing
- Others as available on NSE

```python
# Download specific series
df = stock_df(
    symbol="HDFC",
    from_date=date(2020, 1, 1),
    to_date=date(2020, 1, 30),
    series="EQ"  # Can be "BE", "GR", etc.
)
```

### Data Processing with Pandas

```python
import pandas as pd
from datetime import date
from jugaad_data.nse import stock_df

# Download data
df = stock_df("SBIN", date(2020, 1, 1), date(2020, 1, 30))

# Convert DATE to datetime
df['DATE'] = pd.to_datetime(df['DATE'])

# Sort by date
df = df.sort_values('DATE')

# Calculate returns
df['Daily_Return'] = df['CLOSE'].pct_change()

# Calculate moving averages
df['MA_5'] = df['CLOSE'].rolling(window=5).mean()
df['MA_20'] = df['CLOSE'].rolling(window=20).mean()

# Filter high volume days
high_volume = df[df['VOLUME'] > df['VOLUME'].mean()]

print(high_volume[['DATE', 'CLOSE', 'VOLUME']])
```

---

## Historical Index Data

### Download as Pandas DataFrame

```python
from datetime import date
from jugaad_data.nse import index_df

# Download NIFTY 50 data
df = index_df(
    symbol="NIFTY 50",
    from_date=date(2020, 1, 1),
    to_date=date(2020, 1, 30)
)

print(df.head())
```

### DataFrame Structure

**Columns returned:**

```
Index Name      - Name of the index
INDEX_NAME      - Index symbol
HistoricalDate  - Trading date
OPEN            - Opening value
HIGH            - Day high
LOW             - Day low
CLOSE           - Closing value
```

**Example output:**
```
  Index Name INDEX_NAME HistoricalDate      OPEN      HIGH       LOW     CLOSE
0   Nifty 50   NIFTY 50     2020-01-30  12147.75  12150.30  12010.60  12035.80
1   Nifty 50   NIFTY 50     2020-01-29  12114.90  12169.60  12103.80  12129.50
2   Nifty 50   NIFTY 50     2020-01-28  12148.10  12163.55  12024.50  12055.80
```

### Download and Save to CSV

```python
from jugaad_data.nse import index_csv

# Download and save to CSV
index_csv(
    symbol="NIFTY 50",
    from_date=date(2020, 1, 1),
    to_date=date(2020, 1, 30),
    output="/path/to/NIFTY50_2020_01.csv"
)
```

### Multiple Indices Download

```python
indices = [
    "NIFTY 50",
    "NIFTY BANK",
    "NIFTY IT",
    "NIFTY PHARMA"
]

for index in indices:
    try:
        df = index_df(index, date(2020, 1, 1), date(2020, 1, 30))
        df.to_csv(f"/path/to/{index}_2020_01.csv", index=False)
        print(f"Downloaded {index}")
    except Exception as e:
        print(f"Error downloading {index}: {e}")
```

---

## Historical Derivatives Data

### Get Available Expiry Dates

```python
from datetime import date
from jugaad_data.nse import expiry_dates

# Get all expiry dates for a date
expiries = expiry_dates(date(2020, 1, 1))
print(expiries)

# Get expiry dates for specific contract type
expiries = expiry_dates(date(2020, 1, 1), contract_type="FUTSTK")
print(expiries)
```

**Contract types:**
- `FUTSTK` - Stock futures
- `FUTIDX` - Index futures
- `OPTSTK` - Stock options
- `OPTIDX` - Index options

### Stock Futures

```python
from datetime import date
from jugaad_data.nse import derivatives_df

# Download SBIN stock futures
df = derivatives_df(
    symbol="SBIN",
    from_date=date(2020, 1, 1),
    to_date=date(2020, 1, 30),
    expiry_date=date(2020, 1, 30),
    instrument_type="FUTSTK"
)

print(df.head())
```

**Columns returned:**
```
DATE, EXPIRY, OPEN, HIGH, LOW, CLOSE, LTP, SETTLE PRICE,
TOTAL TRADED QUANTITY, MARKET LOT, PREMIUM VALUE, 
OPEN INTEREST, CHANGE IN OI, SYMBOL
```

### Stock Options

```python
from jugaad_data.nse import derivatives_df

# Download SBIN 300 Call options
df = derivatives_df(
    symbol="SBIN",
    from_date=date(2020, 1, 1),
    to_date=date(2020, 1, 30),
    expiry_date=date(2020, 1, 30),
    instrument_type="OPTSTK",
    option_type="CE",           # "CE" for call, "PE" for put
    strike_price=300
)

print(df.head())
```

**Additional columns for options:**
```
OPTION TYPE, STRIKE PRICE
```

### Index Futures

```python
from jugaad_data.nse import derivatives_df

# Download NIFTY futures
df = derivatives_df(
    symbol="NIFTY",
    from_date=date(2020, 1, 1),
    to_date=date(2020, 1, 30),
    expiry_date=date(2020, 1, 30),
    instrument_type="FUTIDX"
)

print(df.head())
```

### Index Options

```python
from jugaad_data.nse import derivatives_df

# Download NIFTY 12000 Put options
df = derivatives_df(
    symbol="NIFTY",
    from_date=date(2020, 1, 1),
    to_date=date(2020, 1, 30),
    expiry_date=date(2020, 1, 30),
    instrument_type="OPTIDX",
    option_type="PE",
    strike_price=12000
)

print(df.head())
```

### Download Multiple Derivatives

```python
from datetime import date
from jugaad_data.nse import derivatives_csv

# Download multiple call options
strikes = [300, 310, 320, 330]

for strike in strikes:
    try:
        derivatives_csv(
            symbol="SBIN",
            from_date=date(2020, 1, 1),
            to_date=date(2020, 1, 30),
            expiry_date=date(2020, 1, 30),
            instrument_type="OPTSTK",
            option_type="CE",
            strike_price=strike,
            output=f"/path/to/SBIN_CE_{strike}.csv"
        )
        print(f"Downloaded CE {strike}")
    except Exception as e:
        print(f"Error for strike {strike}: {e}")
```

---

## Command Line Interface

### Bhavcopies via CLI

```bash
# Download today's bhavcopy
$ jdata bhavcopy -d ./data

# Download for specific date
$ jdata bhavcopy -d ./data -f 2020-01-01

# Download date range
$ jdata bhavcopy -d ./data -f 2020-01-01 -t 2020-01-31

# Download with delivery data
$ jdata bhavcopy -d ./data -f 2020-01-01 --full

# Download F&O bhavcopy
$ jdata bhavcopy -d ./data -f 2020-01-01 --fo

# Download index bhavcopy
$ jdata bhavcopy -d ./data -f 2020-01-01 --idx
```

### Historical Stock Data via CLI

```bash
# Basic usage
$ jdata stock -s SBIN -f 2020-01-01 -t 2020-01-31 -o sbin.csv

# With different series
$ jdata stock -s HDFC -f 2020-01-01 -t 2020-01-31 -S BE -o hdfc.csv

# Help
$ jdata stock --help
```

### Historical Index Data via CLI

```bash
# Download index data
$ jdata index -s "NIFTY 50" -f 2020-01-01 -t 2020-01-31 -o nifty50.csv

# With space in symbol
$ jdata index -s "NIFTY BANK" -f 2020-01-01 -t 2020-01-31 -o niftybank.csv

# Help
$ jdata index --help
```

### Derivatives Data via CLI

```bash
# Stock futures
$ jdata derivatives \
  -s SBIN \
  -f 2020-01-01 \
  -t 2020-01-30 \
  -e 2020-01-30 \
  -i FUTSTK \
  -o sbin_futures.csv

# Stock call options
$ jdata derivatives \
  -s SBIN \
  -f 2020-01-01 \
  -t 2020-01-30 \
  -e 2020-01-30 \
  -i OPTSTK \
  --ce \
  -p 330 \
  -o sbin_ce330.csv

# Index put options
$ jdata derivatives \
  -s NIFTY \
  -f 2020-01-01 \
  -t 2020-01-23 \
  -e 2020-01-23 \
  -i OPTIDX \
  --pe \
  -p 11000 \
  -o nifty_pe11000.csv

# Help
$ jdata derivatives --help
```

---

## Data Processing Examples

### Calculate Technical Indicators

```python
import pandas as pd
from datetime import date
from jugaad_data.nse import stock_df

# Download data
df = stock_df("SBIN", date(2020, 1, 1), date(2020, 12, 31))
df['DATE'] = pd.to_datetime(df['DATE'])
df = df.sort_values('DATE').reset_index(drop=True)

# Simple Moving Average
df['SMA_20'] = df['CLOSE'].rolling(window=20).mean()
df['SMA_50'] = df['CLOSE'].rolling(window=50).mean()

# Exponential Moving Average
df['EMA_12'] = df['CLOSE'].ewm(span=12).mean()
df['EMA_26'] = df['CLOSE'].ewm(span=26).mean()

# MACD
df['MACD'] = df['EMA_12'] - df['EMA_26']
df['Signal'] = df['MACD'].ewm(span=9).mean()
df['MACD_Histogram'] = df['MACD'] - df['Signal']

# Bollinger Bands
df['BB_Middle'] = df['CLOSE'].rolling(window=20).mean()
df['BB_Std'] = df['CLOSE'].rolling(window=20).std()
df['BB_Upper'] = df['BB_Middle'] + (df['BB_Std'] * 2)
df['BB_Lower'] = df['BB_Middle'] - (df['BB_Std'] * 2)

# RSI
def calculate_rsi(prices, period=14):
    deltas = prices.diff()
    gains = deltas.clip(lower=0)
    losses = -deltas.clip(upper=0)
    avg_gain = gains.rolling(window=period).mean()
    avg_loss = losses.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

df['RSI'] = calculate_rsi(df['CLOSE'])

# Display results
print(df[['DATE', 'CLOSE', 'SMA_20', 'SMA_50', 'MACD', 'RSI']].tail(20))
```

### Analyze Volatility

```python
import pandas as pd
import numpy as np
from datetime import date
from jugaad_data.nse import stock_df

df = stock_df("SBIN", date(2020, 1, 1), date(2020, 12, 31))
df['DATE'] = pd.to_datetime(df['DATE'])

# Daily returns
df['Returns'] = df['CLOSE'].pct_change()

# Volatility (standard deviation of returns)
df['Volatility_20'] = df['Returns'].rolling(window=20).std()
df['Volatility_60'] = df['Returns'].rolling(window=60).std()

# Annualized volatility
df['Annualized_Vol'] = df['Volatility_20'] * np.sqrt(252)

print(df[['DATE', 'CLOSE', 'Returns', 'Annualized_Vol']].tail(20))
```

### Find Support and Resistance

```python
import pandas as pd
from datetime import date
from jugaad_data.nse import stock_df

df = stock_df("HDFC", date(2020, 1, 1), date(2020, 12, 31))
df['DATE'] = pd.to_datetime(df['DATE'])
df = df.sort_values('DATE')

# Find local support (lows) and resistance (highs)
def find_support_resistance(df, window=20):
    df['Support'] = df['LOW'].rolling(window=window, center=True).min()
    df['Resistance'] = df['HIGH'].rolling(window=window, center=True).max()
    return df

df = find_support_resistance(df)

# Get recent support and resistance
recent = df.tail(30)
print(f"Recent Support: {recent['Support'].dropna().tail(1).values[0]}")
print(f"Recent Resistance: {recent['Resistance'].dropna().tail(1).values[0]}")
```

### Analyze Volume

```python
import pandas as pd
from datetime import date
from jugaad_data.nse import stock_df

df = stock_df("SBIN", date(2020, 1, 1), date(2020, 12, 31))
df['DATE'] = pd.to_datetime(df['DATE'])

# Volume analysis
print(f"Mean Volume: {df['VOLUME'].mean():,.0f}")
print(f"Median Volume: {df['VOLUME'].median():,.0f}")
print(f"Max Volume: {df['VOLUME'].max():,.0f}")
print(f"Min Volume: {df['VOLUME'].min():,.0f}")

# High volume days
high_vol = df[df['VOLUME'] > df['VOLUME'].quantile(0.90)]
print(f"\nHigh Volume Days (top 10%): {len(high_vol)} days")
print(high_vol[['DATE', 'CLOSE', 'VOLUME']].head(10))

# Volume weighted average price (VWAP)
print(f"\nRecent VWAP: {df['VWAP'].tail(1).values[0]}")
```

---

## Best Practices

### 1. Error Handling

```python
from datetime import date
from jugaad_data.nse import stock_df
import pandas as pd

def safe_download(symbol, from_date, to_date):
    try:
        df = stock_df(symbol, from_date, to_date)
        if df.empty:
            print(f"No data for {symbol}")
            return None
        return df
    except Exception as e:
        print(f"Error downloading {symbol}: {e}")
        return None

# Usage
df = safe_download("SBIN", date(2020, 1, 1), date(2020, 1, 31))
```

### 2. Date Handling

```python
from datetime import date, timedelta
from jugaad_data.nse import stock_csv

# Download previous business day
today = date(2020, 1, 2)  # Thursday
previous_day = today - timedelta(days=1)  # Wednesday

try:
    stock_csv("SBIN", previous_day, previous_day, output="sbin.csv")
except:
    # Try going back further (might be holiday)
    previous_day = today - timedelta(days=3)
    stock_csv("SBIN", previous_day, previous_day, output="sbin.csv")
```

### 3. Data Validation

```python
import pandas as pd
from jugaad_data.nse import stock_df

df = stock_df("SBIN", date(2020, 1, 1), date(2020, 1, 31))

# Check for missing values
if df.isnull().any().any():
    print("Warning: Missing data found")
    print(df.isnull().sum())

# Validate data types
assert df['CLOSE'].dtype in [float, int], "Price should be numeric"
assert df['VOLUME'].dtype in [float, int], "Volume should be numeric"

# Check date continuity
df['DATE'] = pd.to_datetime(df['DATE'])
date_gaps = df['DATE'].diff().max()
print(f"Maximum gap between dates: {date_gaps}")
```

### 4. Data Persistence

```python
import pandas as pd
from datetime import date
from jugaad_data.nse import stock_df

# Download once, save locally
df = stock_df("SBIN", date(2020, 1, 1), date(2020, 12, 31))
df.to_csv("sbin_2020.csv", index=False)

# Load from cache
df = pd.read_csv("sbin_2020.csv")
print(df.head())
```

### 5. Batch Processing

```python
from datetime import date, timedelta
from jugaad_data.nse import stock_csv
import os

# Download data for multiple stocks
symbols = ["SBIN", "HDFC", "ICICI", "TCS", "INFOSYS"]
output_dir = "./data"

os.makedirs(output_dir, exist_ok=True)

for symbol in symbols:
    try:
        stock_csv(
            symbol,
            from_date=date(2020, 1, 1),
            to_date=date(2020, 12, 31),
            series="EQ",
            output=f"{output_dir}/{symbol}_2020.csv"
        )
        print(f"✓ Downloaded {symbol}")
    except Exception as e:
        print(f"✗ Failed {symbol}: {e}")
```
