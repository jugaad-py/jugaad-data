# Jugaad Data - API Reference Documentation

Welcome to the comprehensive API reference for **jugaad-data**, a Python library for downloading historical and live stock market data from NSE, BSE, and RBI websites.

## Overview

Jugaad Data provides a simple and powerful interface to access Indian financial market data. It supports both historical data downloads and live market data fetching with built-in caching mechanisms.

## Modules

### Core Modules
- [**NSE (National Stock Exchange)**](nse/index.md) - Historical and live NSE data
- [**BSE (Bombay Stock Exchange)**](bse/index.md) - BSE live data and corporate announcements
- [**RBI (Reserve Bank of India)**](rbi/index.md) - Economic data and current rates
- [**CLI (Command Line Interface)**](cli.md) - Command-line tools for data downloads
- [**Utilities**](utilities.md) - Helper functions and decorators
- [**Holidays**](holidays.md) - Trading holiday calendar for Indian exchanges

### NSE Submodules
- [**NSE Archives**](nse/archives.md) - Historical data downloads (bhavcopy, bulk deals)
- [**NSE History**](nse/history.md) - Time series data for stocks, indices, and derivatives
- [**NSE Live**](nse/live.md) - Real-time quotes and market data

## Quick Start

```python
from datetime import date
from jugaad_data.nse import stock_df, NSELive

# Get historical stock data
df = stock_df(symbol="SBIN", from_date=date(2020,1,1), 
              to_date=date(2020,1,30), series="EQ")

# Get live stock quote
nse = NSELive()
quote = nse.stock_quote("HDFC")
print(quote['priceInfo'])
```

## Installation

```bash
pip install jugaad-data
```

## Features

- ✅ **New NSE Website Support** - Works with current NSE infrastructure
- ✅ **Built-in Caching** - Efficient data retrieval with automatic caching
- ✅ **Pandas Integration** - Optional pandas DataFrame support
- ✅ **Command Line Interface** - Easy-to-use CLI tools
- ✅ **Multiple Data Sources** - NSE, BSE, and RBI data access
- ✅ **Live and Historical Data** - Real-time quotes and historical time series

## Data Coverage

| Exchange | Data Type | Status |
|----------|-----------|--------|
| NSE | Equity | ✅ Supported |
| NSE | Equity F&O | ✅ Supported |
| NSE | Index | ✅ Supported |
| NSE | Index F&O | ✅ Supported |
| BSE | Corporate Announcements | ✅ Supported |
| RBI | Current Rates | ✅ Supported |

## Error Handling

The library implements robust error handling for common scenarios:
- Network timeouts and connectivity issues
- Market holidays and non-trading days
- Invalid symbols or date ranges
- Rate limiting and API restrictions

## Caching Strategy

Jugaad Data implements intelligent caching to:
- Reduce load on exchange websites
- Improve performance for repeated requests
- Prevent getting blocked due to excessive requests
- Cache live data with configurable timeouts

## Next Steps

- Browse the [NSE module documentation](nse/index.md) for equity and derivatives data
- Check out the [CLI documentation](cli.md) for command-line usage
- Explore [utility functions](utilities.md) for advanced features