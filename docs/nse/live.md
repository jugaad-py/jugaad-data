# NSE Live

The NSE Live module provides real-time market data and quotes from the National Stock Exchange including stock quotes, option chains, market status, and more.

## Classes

### NSELive Class

Fetches live market data from NSE website.

```python
from jugaad_data.nse import NSELive

nse = NSELive()
```

#### Attributes

- `time_out` (int): Cache timeout in seconds (default: 5)
- `base_url` (str): "https://www.nseindia.com/api"
- `page_url` (str): Reference page URL for session initialization

#### Live Caching

Most methods are decorated with `@live_cache` which caches results for `time_out` seconds to prevent excessive API calls.

#### Methods

##### `stock_quote(symbol)`
Get real-time stock quote.

**Parameters:**
- `symbol` (str): Stock symbol (e.g., "RELIANCE", "TCS")

**Returns:**
- dict: Complete stock quote information

**Example:**
```python
nse = NSELive()
quote = nse.stock_quote("RELIANCE")

# Access price information
price_info = quote['priceInfo']
print(f"Last Price: {price_info['lastPrice']}")
print(f"Change: {price_info['change']}")
print(f"% Change: {price_info['pChange']:.2f}%")
```

**Response Structure:**
```python
{
    'info': {...},  # Company information
    'priceInfo': {
        'lastPrice': 2635.0,
        'change': -49.05,
        'pChange': -1.83,
        'previousClose': 2684.05,
        'open': 2661.0,
        'close': 2632.75,
        'vwap': 2645.57,
        'lowerCP': '2415.65',  # Lower circuit price
        'upperCP': '2952.45',  # Upper circuit price
        'intraDayHighLow': {'min': 2615.6, 'max': 2688.45, 'value': 2635},
        'weekHighLow': {'min': 1473.45, 'max': 2777.15, 'value': 2635}
    },
    'industryInfo': {...},
    'preOpenMarket': {...}
}
```

##### `stock_quote_fno(symbol)`
Get F&O stock quote with derivatives information.

**Parameters:**
- `symbol` (str): Stock symbol

**Returns:**
- dict: Stock quote with F&O data

##### `trade_info(symbol)`
Get detailed trade information for a stock.

**Parameters:**
- `symbol` (str): Stock symbol

**Returns:**
- dict: Trade details and statistics

##### `market_status()`
Get current market status.

**Returns:**
- dict: Market status for all segments

**Example:**
```python
status = nse.market_status()
for market in status['marketState']:
    print(f"{market['market']}: {market['marketStatus']}")
```

##### `chart_data(symbol, indices=False)`
Get intraday chart data.

**Parameters:**
- `symbol` (str): Symbol name
- `indices` (bool): True for index data, False for stocks

**Returns:**
- dict: Chart data with time series

**Example:**
```python
# Stock chart data
stock_chart = nse.chart_data("RELIANCE")

# Index chart data  
nifty_chart = nse.chart_data("NIFTY 50", indices=True)
```

##### `tick_data(symbol, indices=False)`
Alias for `chart_data()` method.

##### `market_turnover()`
Get market-wide turnover data.

**Returns:**
- dict: Turnover statistics for all segments

##### `eq_derivative_turnover(type="allcontracts")`
Get equity derivatives turnover data.

**Parameters:**
- `type` (str): Contract type filter (default: "allcontracts")

**Returns:**
- dict: Derivatives turnover data

##### `all_indices()`
Get data for all NSE indices.

**Returns:**
- dict: List of all indices with current values

**Example:**
```python
indices = nse.all_indices()
for index in indices['data']:
    print(f"{index['index']}: {index['last']}")
```

##### `live_index(symbol="NIFTY 50")`
Get live data for a specific index.

**Parameters:**
- `symbol` (str): Index name (default: "NIFTY 50")

**Returns:**
- dict: Live index data

##### `index_option_chain(symbol="NIFTY")`
Get option chain for index.

**Parameters:**
- `symbol` (str): Index symbol (default: "NIFTY")

**Returns:**
- dict: Complete option chain data

**Example:**
```python
option_chain = nse.index_option_chain("NIFTY")

# Access strike data
strikes = option_chain['records']['data']
for strike in strikes[:5]:  # First 5 strikes
    ce = strike.get('CE', {})
    pe = strike.get('PE', {})
    print(f"Strike {strike['strikePrice']}: CE={ce.get('lastPrice', 'N/A')}, PE={pe.get('lastPrice', 'N/A')}")
```

##### `equities_option_chain(symbol)`
Get option chain for equity stock.

**Parameters:**
- `symbol` (str): Stock symbol

**Returns:**
- dict: Stock option chain data

##### `currency_option_chain(symbol="USDINR")`
Get currency option chain.

**Parameters:**
- `symbol` (str): Currency pair (default: "USDINR")

**Returns:**
- dict: Currency option chain data

##### `live_fno()`
Get live F&O securities data.

**Returns:**
- dict: List of securities in F&O segment

##### `pre_open_market(key="NIFTY")`
Get pre-open market data.

**Parameters:**
- `key` (str): Market segment (default: "NIFTY")

**Returns:**
- dict: Pre-open market data

##### `holiday_list()`
Get trading holiday list.

**Returns:**
- dict: List of trading holidays

**Example:**
```python
holidays = nse.holiday_list()
for holiday in holidays['FO']:  # F&O holidays
    print(f"{holiday['tradingDate']}: {holiday['description']}")
```

##### `corporate_announcements(segment='equities', from_date=None, to_date=None, symbol=None)`
Get corporate announcements.

**Parameters:**
- `segment` (str): Market segment (default: 'equities')
- `from_date` (date): Start date filter
- `to_date` (date): End date filter  
- `symbol` (str): Symbol filter

**Returns:**
- dict: Corporate announcements data

**Example:**
```python
from datetime import date

# Get all announcements
announcements = nse.corporate_announcements()

# Get announcements for specific date range
announcements = nse.corporate_announcements(
    from_date=date(2024, 1, 1),
    to_date=date(2024, 1, 31)
)

# Get announcements for specific symbol
rel_announcements = nse.corporate_announcements(symbol="RELIANCE")
```

## Usage Examples

### Basic Stock Quote

```python
from jugaad_data.nse import NSELive

nse = NSELive()

# Get stock quote
quote = nse.stock_quote("TCS")
price = quote['priceInfo']

print(f"TCS Current Price: ₹{price['lastPrice']}")
print(f"Day's Range: ₹{price['intraDayHighLow']['min']} - ₹{price['intraDayHighLow']['max']}")
print(f"Previous Close: ₹{price['previousClose']}")
print(f"Change: ₹{price['change']:.2f} ({price['pChange']:.2f}%)")
```

### Market Overview

```python
# Check market status
status = nse.market_status()
print("Market Status:")
for market in status['marketState']:
    print(f"  {market['market']}: {market['marketStatus']}")

# Get top indices
indices = nse.all_indices()
print("\nMajor Indices:")
for index in indices['data'][:5]:
    change_color = "📈" if index['change'] > 0 else "📉"
    print(f"  {index['index']}: {index['last']} {change_color} {index['change']:.2f}")
```

### Option Chain Analysis

```python
# Get NIFTY option chain
option_chain = nse.index_option_chain("NIFTY")
records = option_chain['records']

print(f"NIFTY Spot: {records['underlyingValue']}")
print(f"Expiry: {records['expiryDates'][0]}")

# Analyze strikes around current price
spot_price = records['underlyingValue']
strikes = records['data']

print("\nOption Chain (Around Spot):")
print("Strike\t\tCE LTP\t\tPE LTP")
print("-" * 40)

for strike in strikes:
    strike_price = strike['strikePrice']
    if abs(strike_price - spot_price) <= 200:  # Within 200 points
        ce_ltp = strike.get('CE', {}).get('lastPrice', 'N/A')
        pe_ltp = strike.get('PE', {}).get('lastPrice', 'N/A')
        print(f"{strike_price}\t\t{ce_ltp}\t\t{pe_ltp}")
```

### Live Market Monitoring

```python
import time
from datetime import datetime

def monitor_stocks(symbols, interval=30):
    """Monitor multiple stocks with periodic updates"""
    nse = NSELive()
    
    while True:
        print(f"\n=== Market Update at {datetime.now().strftime('%H:%M:%S')} ===")
        
        for symbol in symbols:
            try:
                quote = nse.stock_quote(symbol)
                price = quote['priceInfo']
                
                change_symbol = "▲" if price['change'] > 0 else "▼"
                print(f"{symbol:10} ₹{price['lastPrice']:8.2f} {change_symbol} {price['change']:6.2f} ({price['pChange']:5.2f}%)")
                
            except Exception as e:
                print(f"{symbol:10} Error: {e}")
        
        time.sleep(interval)

# Monitor selected stocks
monitor_stocks(["RELIANCE", "TCS", "HDFC", "INFY", "ICICIBANK"])
```

### Corporate Announcements Tracker

```python
from datetime import date, timedelta

# Get recent announcements
recent_date = date.today() - timedelta(days=7)
announcements = nse.corporate_announcements(
    from_date=recent_date,
    to_date=date.today()
)

print("Recent Corporate Announcements:")
for announcement in announcements[:10]:  # Latest 10
    print(f"📄 {announcement['symbol']}: {announcement['subject'][:60]}...")
    print(f"   Date: {announcement['an_dt']}")
    print()
```

## Error Handling

### Common Issues

1. **Session Management**: NSELive automatically handles session cookies
2. **Rate Limiting**: Built-in caching prevents excessive requests
3. **Network Issues**: Handle network timeouts gracefully

### Best Practices

```python
def safe_quote(symbol):
    """Safely get stock quote with error handling"""
    try:
        nse = NSELive()
        quote = nse.stock_quote(symbol)
        return quote['priceInfo']
    except KeyError as e:
        print(f"Data structure changed for {symbol}: {e}")
        return None
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

# Usage
price_info = safe_quote("RELIANCE")
if price_info:
    print(f"Current price: {price_info['lastPrice']}")
```

## Live Data Caching

### Cache Behavior
- Each method caches results for 5 seconds by default
- Prevents redundant API calls within the timeout period
- Cache keys generated from method name and parameters

### Cache Control
```python
# Different instances have separate caches
nse1 = NSELive()
nse2 = NSELive()

# Force fresh data by creating new instance
def get_fresh_quote(symbol):
    fresh_nse = NSELive()
    return fresh_nse.stock_quote(symbol)
```

## Integration with Other Modules

### Combine with Historical Data

```python
from jugaad_data.nse import NSELive, stock_df
from datetime import date, timedelta

# Get current price
nse = NSELive()
current = nse.stock_quote("RELIANCE")['priceInfo']

# Get historical data
end_date = date.today() - timedelta(days=1)  # Yesterday
start_date = end_date - timedelta(days=30)   # 30 days ago
df = stock_df("RELIANCE", start_date, end_date)

# Compare current with historical
historical_avg = df['CLOSE'].mean()
print(f"Current: ₹{current['lastPrice']}")
print(f"30-day average: ₹{historical_avg:.2f}")
print(f"Above average: {current['lastPrice'] > historical_avg}")
```