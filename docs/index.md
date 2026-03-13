# Jugaad Data Documentation

Complete documentation for the `jugaad-data` Python library for downloading historical and live stock market data from NSE, BSE, and economic data from RBI.

## Overview

`jugaad-data` is a Python library that provides easy-to-use interfaces for:

- **Live Market Data**: Real-time stock quotes, indices, option chains, derivatives
- **Historical Data**: OHLC data, bhavcopies, derivatives contracts
- **Economic Data**: RBI policy rates, T-bills, government securities
- **Command-Line Interface**: Download data without writing code

## Quick Navigation

### Getting Started
- [Quick Start Guide](QUICKSTART.md) - Installation and common examples
- [API Reference](API_REFERENCE.md) - Complete API documentation

### Data Modules

#### Live Data
- [Live Data Guide](LIVE_DATA_GUIDE.md) - Real-time quotes, indices, options, announcements

#### Historical Data  
- [Historical Data Guide](HISTORICAL_DATA_GUIDE.md) - Download OHLC, bhavcopies, derivatives

#### Economic Data
- [RBI Guide](RBI_GUIDE.md) - Policy rates, T-bills, government securities

## Key Features

✅ **Download Bhavcopies**
- Equity, derivatives, and index bhavcopies
- Daily complete market snapshots

✅ **Historical OHLC Data**
- Stocks, indices, and derivatives
- Pandas DataFrame or CSV output
- Date range support

✅ **Live Market Data**
- Real-time stock quotes
- Index data and market status
- Option chains (indices, equities, currencies)
- Derivative contracts
- Corporate announcements

✅ **RBI Economic Data**
- Policy rates (repo, MSF, bank rate)
- Banking rates (base rate, MCLR)
- Money market rates (call rates, T-bills)
- Government securities yields
- Major indices

✅ **Command-Line Interface**  
- Download data from terminal without coding
- Support for batching and scheduling

## Installation

```bash
# Basic installation
pip install jugaad-data

# With pandas support (recommended)
pip install jugaad-data pandas
```

## Quick Example

### Download Stock Data
```python
from datetime import date
from jugaad_data.nse import stock_df

df = stock_df("SBIN", date(2020, 1, 1), date(2020, 1, 31))
print(df.head())
```

### Get Live Quote
```python
from jugaad_data.nse import NSELive

n = NSELive()
quote = n.stock_quote("SBIN")
print(quote['priceInfo'])
```

### Fetch RBI Rates
```python
from jugaad_data.rbi import RBI

r = RBI()
rates = r.current_rates()
print(rates['Policy Repo Rate'])
```

### Command Line
```bash
# Download stock data
jdata stock -s SBIN -f 2020-01-01 -t 2020-01-31 -o sbin.csv

# Download index data
jdata index -s "NIFTY 50" -f 2020-01-01 -t 2020-01-31 -o nifty.csv

# Download bhavcopy
jdata bhavcopy -d ./data -f 2020-01-01
```

## Module Overview

### NSE Live (`jugaad_data.nse.NSELive`)

Real-time data from National Stock Exchange:

- Market status and statistics
- All indices data
- Stock quotes (price, company info, metadata)
- Option chains
- Derivatives data
- Corporate announcements
- Tick data and order book

**Key Methods:**
- `stock_quote(symbol)` - Live stock quote
- `live_index(symbol)` - Index data
- `index_option_chain(symbol)` - Index options
- `stock_quote_fno(symbol)` - Futures & options

### NSE Historical (`jugaad_data.nse`)

Historical OHLC data:

- Bhavcopies (daily snapshots)
- Stock historical data
- Index historical data
- Derivatives (futures, options)

**Key Functions:**
- `stock_df(symbol, from_date, to_date)` - Historical stock data
- `derivatives_df(symbol, from_date, to_date, ...)` - Derivatives data
- `bhavcopy_save(date, path)` - Download bhavcopies

### BSE (`jugaad_data.bse`)

Bombay Stock Exchange data (live):

- Stock quotes
- Live data

### RBI (`jugaad_data.rbi.RBI`)

Reserve Bank of India economic data:

- Policy rates (repo, reverse repo, MSF)
- Reserve requirements (CRR, SLR)
- Banking rates (base rate, MCLR)
- Deposit rates
- Money market rates (call rates)
- Government securities yields
- T-Bill rates
- Equity indices

**Key Methods:**
- `current_rates()` - All current rates and indices

## Data Structures

### Price Information
Consistent across live quotes:
- OHLC (Open, High, Low, Close)
- Change and percentage change
- VWAP (Volume weighted average price)
- 52-week highs and lows
- Volume and value data

### Indices
Standard index data includes:
- Name and symbol
- OHLC and intraday values
- P/E, P/B, dividend yield
- Advances/declines
- Performance metrics (30-day, 365-day)

### Derivatives
Futures and options data:
- Strike price
- Expiry date
- Open interest
- Greeks (for options)
- Bid-ask spreads
- Implied volatility

### Options Chains
Complete option chain structure:
- All strikes for expiry
- Call and put prices
- Open interest
- Greeks
- Implied volatility
- Greeks

## Common Use Cases

### Backtesting Trading Strategies
```python
from datetime import date
from jugaad_data.nse import stock_df
import pandas as pd

# Download historical data
df = stock_df("SBIN", date(2020, 1, 1), date(2020, 12, 31))

# Calculate indicators
df['SMA_20'] = df['CLOSE'].rolling(20).mean()
df['SMA_50'] = df['CLOSE'].rolling(50).mean()

# Test strategy
df['Signal'] = (df['SMA_20'] > df['SMA_50']).astype(int)
```

### Real-Time Monitoring
```python
from jugaad_data.nse import NSELive
import time

n = NSELive()
while True:
    quote = n.stock_quote("SBIN")
    print(f"SBIN: {quote['priceInfo']['lastPrice']}")
    time.sleep(60)
```

### Economic Analysis
```python
from jugaad_data.rbi import RBI

r = RBI()
rates = r.current_rates()

# Analyze monetary policy stance
policy_rate = float(rates['Policy Repo Rate'].replace('%', ''))
if policy_rate > 5:
    print("Tight monetary policy")
```

### Portfolio Analysis
```python
from datetime import date
from jugaad_data.nse import stock_df

# Track multiple stocks
portfolio = ["SBIN", "HDFC", "ICICI"]
returns = {}

for stock in portfolio:
    df = stock_df(stock, date(2020, 1, 1), date(2020, 12, 31))
    annual_return = (df['CLOSE'].iloc[-1] / df['CLOSE'].iloc[0]) - 1
    returns[stock] = annual_return

for stock, ret in sorted(returns.items(), key=lambda x: x[1], reverse=True):
    print(f"{stock}: {ret*100:.2f}%")
```

## Date Format

All dates should be `datetime.date` objects:

```python
from datetime import date

# Correct
from_date = date(2020, 1, 1)
to_date = date(2020, 12, 31)

# Do NOT use strings
# ❌ from_date = "2020-01-01"
```

## Error Handling

```python
try:
    df = stock_df("INVALIDTICKER", date(2020, 1, 1), date(2020, 1, 31))
except Exception as e:
    print(f"Error: {e}")
```

## Performance Tips

1. **Cache Results**: Use pickle or CSV to save downloaded data
2. **Batch Requests**: Download multiple symbols efficiently
3. **Rate Limiting**: Add delays between requests to avoid rate limiting
4. **Data Validation**: Check for data quality before processing
5. **Vector Operations**: Use pandas/numpy for calculations

## Limitations

- No historical data for options Greeks or IV
- Limited to NSE/BSE/RBI public data
- Rate limits apply during high traffic
- Holiday/weekend adjustments needed
- No real-time tick data streaming (snapshot only)

## Future Enhancements

Currently in pipeline:
- Corporate information
- Financial results
- More derivatives data
- Additional economic indicators

## Support & Issues

- **GitHub Repository**: https://github.com/jugaad-py/jugaad-data
- **Issue Tracker**: https://github.com/jugaad-py/jugaad-data/issues
- **Feature Requests**: Same as above

## Contributing

Contributions are welcome! If you find other data available on NSE/RBI/BSE websites, please raise a feature request or contribute code.

## License

Refer to the LICENSE file in the repository.

## Disclaimer

This library fetches data from publicly available sources (NSE, BSE, RBI official websites). The library author is not responsible for:
- Data accuracy or completeness
- Decisions made based on this data
- Market risks or losses
- Technical issues or API changes

Always verify critical data from official sources before making trading or investment decisions.

## Related Resources

- [NSE Website](https://www.nseindia.com)
- [BSE Website](https://www.bseindia.com)
- [RBI Website](https://www.rbi.org.in)
- [Marketsetup Blog](https://marketsetup.in)

---

**Last Updated**: March 2026
