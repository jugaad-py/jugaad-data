# Jugaad Data - Quick Start Guide

## Installation

```bash
pip install jugaad-data
```

Optionally install pandas for dataframe support:

```bash
pip install jugaad-data pandas
```

## Quick Examples

### Download Bhavcopies (Daily Market Snapshot)

```python
from datetime import date
from jugaad_data.nse import bhavcopy_save, bhavcopy_fo_save

# Download equity bhavcopy
bhavcopy_save(date(2020, 1, 1), "./")

# Download futures and options bhavcopy
bhavcopy_fo_save(date(2020, 1, 1), "./")
```

Output:
```
cm01Jan2020bhav.csv  fo01Jan2020bhav.csv
```

### Download Historical Stock Data

```python
from datetime import date
from jugaad_data.nse import stock_df, stock_csv

# Download as pandas dataframe
df = stock_df(symbol="SBIN", from_date=date(2020, 1, 1),
              to_date=date(2020, 1, 30), series="EQ")
print(df.head())

# Download as CSV file
stock_csv(symbol="SBIN", from_date=date(2020, 1, 1),
          to_date=date(2020, 1, 30), series="EQ", output="/path/to/file.csv")
```

### Fetch Live Stock Quotes

```python
from jugaad_data.nse import NSELive

n = NSELive()

# Get quote for a stock
quote = n.stock_quote("HDFC")
print(quote['priceInfo'])  # Price information
print(quote['info'])       # Company information
print(quote['metadata'])   # Stock metadata
```

### Fetch Live Index Data

```python
from jugaad_data.nse import NSELive

n = NSELive()

# Get all indices
all_indices = n.all_indices()
for idx in all_indices['data']:
    print(f"{idx['index']} - {idx['last']}")

# Get specific index data
nifty = n.live_index("NIFTY 50")
print(nifty['marketStatus'])  # Market status
print(nifty['data'])          # Price data
```

### Fetch Option Chains

```python
from jugaad_data.nse import NSELive

n = NSELive()

# Index option chain
option_chain = n.index_option_chain("NIFTY")

# Equity option chain
eq_option_chain = n.equities_option_chain("RELIANCE")

# Currency option chain
curr_option_chain = n.currency_option_chain("USDINR")

# Get expiry dates
print(option_chain['records']['expiryDates'])

# Print option chain
for option in option_chain['filtered']['data']:
    CE = option['CE']['lastPrice']
    strike = option['strikePrice']
    PE = option['PE']['lastPrice']
    print(f"{CE}\t{strike}\t{PE}")
```

### Fetch Live Derivatives Data

```python
from jugaad_data.nse import NSELive

n = NSELive()

# Stock futures and options
quotes = n.stock_quote_fno("HDFC")
for quote in quotes['stocks']:
    print(f"{quote['metadata']['identifier']}\t{quote['metadata']['lastPrice']}")

# Equity derivative turnover
turnover = n.eq_derivative_turnover()
for t in turnover['value'][:10]:
    print(f"{t['identifier']}\t{t['totalTurnover']}")
```

### Download Historical Derivatives Data

```python
from datetime import date
from jugaad_data.nse import derivatives_df, derivatives_csv

# Stock Futures
df = derivatives_df(symbol="SBIN", from_date=date(2020, 1, 1),
                    to_date=date(2020, 1, 30),
                    expiry_date=date(2020, 1, 30),
                    instrument_type="FUTSTK")

# Stock Options (Call)
df = derivatives_df(symbol="SBIN", from_date=date(2020, 1, 1),
                    to_date=date(2020, 1, 30),
                    expiry_date=date(2020, 1, 30),
                    instrument_type="OPTSTK",
                    option_type="CE", strike_price=300)

# Index Futures
df = derivatives_df(symbol="NIFTY", from_date=date(2020, 1, 1),
                    to_date=date(2020, 1, 30),
                    expiry_date=date(2020, 1, 30),
                    instrument_type="FUTIDX")

# Index Options (Put)
df = derivatives_df(symbol="NIFTY", from_date=date(2020, 1, 1),
                    to_date=date(2020, 1, 30),
                    expiry_date=date(2020, 1, 30),
                    instrument_type="OPTIDX",
                    option_type="PE", strike_price=12000)
```

### Fetch RBI Economic Data

```python
from jugaad_data.rbi import RBI

r = RBI()
current_rates = r.current_rates()
print(current_rates)
```

Output includes:
- Policy Repo Rate
- Reverse Repo Rate
- Bank Rate
- CRR, SLR
- Base Rate, MCLR
- T-Bill rates
- Government Securities rates
- Index values (Sensex, Nifty 50)

### Download NSE Daily Reports (39+ Report Types)

NSE publishes 39+ different reports daily including volatility data, advance/decline data, and more.

```python
from jugaad_data.nse import list_available_reports, download_report

# Discover all available reports
reports = list_available_reports()
for report in reports[:5]:  # Show first 5
    print(f"{report['key']}: {report['name']}")

# Download a specific report (e.g., CM Volatility)
download_report("CM-VOLATILITY", output="cm_volatility.csv")

# Download another report type
download_report("NIFTY-50-ADVANCE-DECLINE", output="nifty_advance_decline.csv")
```

Available reports include:
- CM-VOLATILITY: Equity segment volatility measures
- NIFTY-50-ADVANCE-DECLINE: NIFTY 50 advance/decline statistics
- NIFTY-NEXT-50-ADVANCE-DECLINE: NIFTY Next 50 statistics
- And 36+ more report types

### Command Line Interface

```bash
# Download today's bhavcopy
$ jdata bhavcopy -d /path/to/dir

# Download bhavcopy for specific date
$ jdata bhavcopy -d /path/to/dir -f 2020-01-01

# Download bhavcopy date range
$ jdata bhavcopy -d /path/to/dir -f 2020-01-01 -t 2020-01-30

# Download derivatives bhavcopy
$ jdata bhavcopy -d /path/to/dir -f 2020-01-01 -t 2020-01-30 --fo

# Download index bhavcopy
$ jdata bhavcopy -d /path/to/dir -f 2020-01-01 -t 2020-01-30 --idx

# Download historical stock data
$ jdata stock -s SBIN -f 2020-01-01 -t 2020-01-31 -o SBIN-Jan.csv

# Download historical index data
$ jdata index -s "NIFTY 50" -f 2020-01-01 -t 2020-01-31 -o NIFTY-Jan.csv

# Download stock futures
$ jdata derivatives -s SBIN -f 2020-01-01 -t 2020-01-30 -e 2020-01-30 -i FUTSTK -o file.csv

# Download stock call options
$ jdata derivatives -s SBIN -f 2020-01-01 -t 2020-01-30 -e 2020-01-30 -i OPTSTK -p 330 --ce -o file.csv

# Download index put options
$ jdata derivatives -s NIFTY -f 2020-01-01 -t 2020-01-23 -e 2020-01-23 -i OPTIDX -p 11000 --pe -o file.csv
```

## Data Sources

- **NSE (National Stock Exchange)**: Stock & index data from the new NSE website API
- **BSE (Bombay Stock Exchange)**: Available through BSE live module
- **RBI (Reserve Bank of India)**: Economic data and rates

## Key Features

✅ Download bhavcopies for stocks, indices, and derivatives
✅ Download historical stock, index, and derivatives data
✅ Fetch live quotes for stocks and derivatives
✅ Fetch live index and turnover data
✅ Fetch option chains
✅ Fetch current rates from RBI website
✅ Download 39+ NSE daily reports (volatility, advance/decline, etc.)
✅ Pandas dataframe support
✅ Command-line interface

## In Pipeline

- Corporate information
- Financial results

## Notes

- This library uses NSE's new website API, making it future-proof
- Many other libraries rely on old NSE website which may stop working
- Beginner Python users: Master dictionaries and lists as NSE returns large nested data structures
