# Jugaad Data - Live Data Guide

A comprehensive guide to fetching real-time market data using `jugaad-data`.

## Table of Contents

1. [Initialization](#initialization)
2. [Live Market Status](#live-market-status)
3. [Live Index Data](#live-index-data)
4. [Live Stock Data](#live-stock-data)
5. [Live Derivatives Data](#live-derivatives-data)
6. [Live Option Chains](#live-option-chains)
7. [Corporate Announcements](#corporate-announcements)
8. [Best Practices](#best-practices)

---

## Initialization

```python
from jugaad_data.nse import NSELive

# Create instance
n = NSELive()
```

---

## Live Market Status

### Get Overall Market Status

```python
status = n.market_status()
```

Example output structure:

```python
[
    {
        'market': 'Capital Market',
        'marketStatus': 'Open' | 'Closed',
        'tradeDate': '22-Dec-2023 15:30',
        'index': 'NIFTY 50',
        'last': 21349.4,              # Last value
        'variation': 94.35,           # Absolute change
        'percentChange': 0.44,        # Percentage change
        'marketStatusMessage': 'Market is Open' | 'Market is Closed'
    },
    {
        'market': 'Currency',
        'marketStatus': 'Closed',
        'index': '',
        # ... (empty for closed segments)
    },
    # Additional segments: Commodity, Debt, Currency Futures
]
```

### Get Market Turnover

```python
turnover = n.market_turnover()

# Access by segment
for segment in turnover['data']:
    name = segment['name']  # e.g., "Equities", "Index Futures"
    today_data = segment['today']
    
    if today_data:
        volume = today_data['volume']
        value = today_data['value']
        print(f"{name} - Volume: {volume}, Value: {value}")
```

Example segments:
```
Equities
Index Futures
Index Options
Stock Futures
Stock Options
Currency Futures
Currency Options
Commodity Futures
Commodity Options
Interest Rate Futures
Interest Rate Options
```

---

## Live Index Data

### Get All Indices

```python
all_indices = n.all_indices()

# Timestamp of last update
print(all_indices['timestamp'])  # '25-Jan-2021 15:30:00'

# Lists
print(all_indices['advances'])   # Number of stocks advanced
print(all_indices['declines'])   # Number of stocks declined
print(all_indices['unchanged'])  # Number unchanged

# All index data
for idx in all_indices['data']:
    print(f"{idx['index']} - {idx['last']}")
```

### Index Data Structure

Each index contains:

```python
{
    'key': 'BROAD MARKET INDICES',           # Category
    'index': 'NIFTY 50',                    # Index name
    'indexSymbol': 'NIFTY 50',
    'last': 14238.9,                        # Last traded value
    'variation': -133,                      # Absolute change
    'percentChange': -0.93,                 # Percentage change
    'open': 14477.8,
    'high': 14491.1,
    'low': 14218.6,
    'previousClose': 14371.9,
    'yearHigh': 14753.55,
    'yearLow': 7511.1,
    'pe': '38.42',                          # P/E ratio
    'pb': '4.04',                           # P/B ratio
    'dy': '1.11',                           # Dividend yield
    'declines': '31',                       # Stocks declined
    'advances': '18',                       # Stocks advanced
    'unchanged': '1',
    'perChange365d': 17.49,                 # 1-year % change
    'date365dAgo': '27-Jan-2020',
    'chart365dPath': 'https://...',
    'perChange30d': 3.56,                   # 30-day % change
    'date30dAgo': '24-Dec-2020',
    'chart30dPath': 'https://...',
    'chartTodayPath': 'https://...',
    'previousDay': 14371.9,
    'oneWeekAgo': 14644.7,
    'oneMonthAgo': 13749.25,
    'oneYearAgo': 12119
}
```

### Get Specific Index Data

```python
nifty = n.live_index("NIFTY 50")

# Available keys
print(nifty['name'])                # 'NIFTY 50'
print(nifty['timestamp'])           # Last update time
print(nifty['marketStatus'])        # Market open/close
print(nifty['advance'])             # Advances/declines
print(nifty['data'][0])             # Detailed price data
print(nifty['metadata'])            # Repeated price info
```

### Common Indices

```
NIFTY 50
NIFTY NEXT 50
NIFTY 100
NIFTY 200
NIFTY 500
NIFTY MIDCAP 50
NIFTY MIDCAP 100
NIFTY SMALLCAP 50
NIFTY SMALLCAP 100
NIFTY BANK
NIFTY AUTO
NIFTY FINANCIAL SERVICES
NIFTY FMCG
NIFTY IT
NIFTY MEDIA
NIFTY METAL
NIFTY PHARMA
NIFTY REALTY
INDIA VIX
```

---

## Live Stock Data

### Get Stock Quote

```python
from jugaad_data.nse import NSELive

n = NSELive()
quote = n.stock_quote("HDFC")

# Available sections in quote
price_info = quote['priceInfo']      # OHLC, change, VWAP
info = quote['info']                 # Company info
metadata = quote['metadata']         # ISIN, listing date
security_info = quote['securityInfo'] # Trading status
pre_open = quote['preOpenMarket']   # Pre-open data
sdd = quote['sddDetails']           # Secured delivery details
```

### Price Information

```python
price_info = quote['priceInfo']

{
    'lastPrice': 2560,
    'change': -29.45,
    'pChange': -1.14,              # Percentage change
    'previousClose': 2589.45,
    'open': 2630.45,
    'close': 2551.4,
    'vwap': 2611.45,               # Volume weighted average price
    'lowerCP': '2330.55',           # Lower circuit limit
    'upperCP': '2848.35',           # Upper circuit limit
    'pPriceBand': 'No Band',
    'basePrice': 2589.45,
    'intraDayHighLow': {
        'min': 2543,
        'max': 2670,
        'value': 2560
    },
    'weekHighLow': {
        'min': 1473.45,
        'minDate': '24-Mar-2020',
        'max': 2777.15,
        'maxDate': '13-Jan-2021',
        'value': 2560
    }
}
```

### Company Information

```python
info = quote['info']

{
    'symbol': 'HDFC',
    'companyName': 'Housing Development Finance Corporation Limited',
    'industry': 'FINANCE - HOUSING',
    'activeSeries': ['EQ', 'W3'],
    'debtSeries': [],
    'tempSuspendedSeries': ['W1', 'W2'],
    'isFNOSec': True,              # Futures & Options available
    'isCASec': False,              # Corporate actions
    'isSLBSec': True,              # Securities lending available
    'isDebtSec': False,
    'isSuspended': False,
    'isETFSec': False,
    'isDelisted': False,
    'isin': 'INE001A13049',
    'isTop10': False,
    'identifier': 'HDFCEQN'
}
```

### Stock Metadata

```python
metadata = quote['metadata']

{
    'series': 'EQ',
    'symbol': 'HDFC',
    'isin': 'INE001A01036',
    'status': 'Listed',
    'listingDate': '23-Oct-1996',
    'industry': 'HOUSING FINANCE',
    'lastUpdateTime': '25-Jan-2021 16:00:00',
    'pdSectorPe': 30.46,           # Sector P/E
    'pdSymbolPe': 0,               # Stock P/E
    'pdSectorInd': 'NIFTY FINANCIAL SERVICES'
}
```

### Security Information

```python
security_info = quote['securityInfo']

{
    'boardStatus': 'Main',
    'tradingStatus': 'Active',
    'tradingSegment': 'Normal Market',
    'sessionNo': '-',
    'slb': 'Yes',                  # Securities lending/borrowing
    'classOfShare': 'Equity',
    'derivatives': 'Yes',
    'surveillance': '-',
    'faceValue': 2,
    'issuedCap': 1800191002        # Issued capital
}
```

### Tick Data (Minute-by-Minute)

```python
tick_data = n.tick_data("HDFC")

# Graph data: list of [timestamp in ms, price] pairs
for timestamp_ms, price in tick_data['grapthData'][:10]:
    print(f"{timestamp_ms}: {price}")
```

### Trade Information

```python
trade_info = n.trade_info("HDFC")

# Order book
order_book = trade_info['marketDeptOrderBook']

print(order_book['totalBuyQuantity'])
print(order_book['totalSellQuantity'])

# Top 5 bid levels
for bid in order_book['bid']:
    print(f"Bid: {bid['price']} @ {bid['quantity']}")

# Best 5 ask levels
for ask in order_book['ask']:
    print(f"Ask: {ask['price']} @ {ask['quantity']}")

# Trade information
trade_stats = order_book['tradeInfo']
print(f"Total Traded Volume: {trade_stats['totalTradedVolume']}")
print(f"Total Traded Value: {trade_stats['totalTradedValue']}")
print(f"Impact Cost: {trade_stats['impactCost']}")

# Delivery information
dp_info = trade_info['securityWiseDP']
print(f"Delivery Quantity: {dp_info['deliveryQuantity']}")
print(f"Delivery to Traded Ratio: {dp_info['deliveryToTradedQuantity']}%")
```

---

## Live Derivatives Data

### Get Derivative Turnover

```python
turnover = n.eq_derivative_turnover()

# Top contracts by turnover
for contract in turnover['value']:
    print(f"{contract['identifier']}: {contract['totalTurnover']}")
```

### Contract Structure

```python
contract = turnover['value'][0]

{
    'underlying': 'NIFTY',
    'identifier': 'FUTIDXNIFTY28-01-2021XX0.00',
    'instrumentType': 'FUTIDX',
    'instrument': 'Index Futures',
    'expiryDate': '28-Jan-2021',
    'optionType': '-',                 # '-' for futures, 'CE'/'PE' for options
    'strikePrice': 0,                  # 0 for futures
    'lastPrice': 14254,
    'pChange': -0.88,                  # Percentage change
    'openPrice': 14475,
    'highPrice': 14497.75,
    'lowPrice': 14233.6,
    'numberOfContractsTraded': 185139,
    'totalTurnover': 1993001.43,
    'premiumTurnover': 199300143255.75,
    'openInterest': 127322,
    'underlyingValue': 14238.9
}
```

### Futures and Options Quote for Stock

```python
# Get all F&O contracts for a symbol (includes all expiries and strikes)
fno_data = n.stock_quote_fno("RELIANCE")

# Response structure
{
    'data': [
        {
            'identifier': 'FUTSTKRELIANCE30-Mar-2026XX0.00',
            'instrumentType': 'FUTSTK',  # or 'OPTSTK'
            'underlying': 'RELIANCE',
            'expiryDate': '30-Mar-2026',
            'optionType': 'XX',          # 'XX' for Futures, 'CE' or 'PE' for Options
            'strikePrice': '0.00',
            'lastPrice': 2850.5,
            'openPrice': 2835.0,
            'highPrice': 2860.0,
            'lowPrice': 2820.0,
            'closePrice': 2835.3,
            'prevClose': 2835.3,
            'change': 15.2,
            'pchange': 0.54,
            'openInterest': 123456,
            'changeinOpenInterest': 1234,
            'totalTradedVolume': 45678,
            'totalTurnover': 1296789420,
            'underlyingValue': 2850.5,
            'volumeFreezeQuantity': 240001,
            'ticksize': 0.05,
        },
        ...more contracts
    ],
    'timestamp': '16-Mar-2026 15:30:00'
}
```

### Processing Contract Data

```python
# Iterate through all contracts
fno_data = n.stock_quote_fno("RELIANCE")

# Filter futures only
futures = [c for c in fno_data['data'] if c['instrumentType'] == 'FUTSTK']

# Filter call options with 30-Mar expiry
calls_mar = [c for c in fno_data['data'] 
             if c['instrumentType'] == 'OPTSTK' 
             and c['optionType'] == 'CE'
             and c['expiryDate'] == '30-Mar-2026']

# Get highest IV call option
calls_mar_sorted = sorted(calls_mar, key=lambda x: x['lastPrice'], reverse=True)
for call in calls_mar_sorted[:5]:
    print(f"Strike: {call['strikePrice']:8} | Price: {call['lastPrice']:8.2f} | OI: {call['openInterest']}")
```

### Working with Specific Contracts

```python
# Get a specific contract
contract = fno_data['data'][0]

# Extract key information
identifier = contract['identifier']
price = contract['lastPrice']
oi = contract['openInterest']
volume = contract['totalTradedVolume']
iv = contract.get('impliedVolatility', 'N/A')  # If available

print(f"Contract: {identifier}")
print(f"Current Price: {price}")
print(f"Open Interest: {oi}")
print(f"Volume: {volume}")
```

---

## Live Option Chains

### Index Option Chain

```python
# Without filter
option_chain = n.index_option_chain("NIFTY")

# With specific expiry
option_chain = n.index_option_chain("NIFTY", expiry_date="28-Jan-2021")
```

### Equity Option Chain

```python
option_chain = n.equities_option_chain("RELIANCE")
option_chain = n.equities_option_chain("HDFC", expiry_date="28-Jan-2021")
```

### Currency Option Chain

```python
option_chain = n.currency_option_chain("USDINR")
```

### Get Expiry Dates

```python
expiry_dates = option_chain['records']['expiryDates']
# ['28-Jan-2021', '04-Feb-2021', '11-Feb-2021', ...]
```

### Parse Option Chain Data

```python
# Filter option chain data
data = option_chain['filtered']['data']

for option in data:
    strike = option['strikePrice']
    ce_price = option['CE']['lastPrice'] if option['CE']['lastPrice'] else 0
    pe_price = option['PE']['lastPrice'] if option['PE']['lastPrice'] else 0
    
    print(f"Strike: {strike} | CE: {ce_price} | PE: {pe_price}")

# Typical output:
# Strike: 20800 | CE: 604 | PE: 14
# Strike: 20850 | CE: 558.95 | PE: 18
# Strike: 21200 | CE: 239 | PE: 50
```

### Option Data Structure

```python
option = data[0]

{
    'strikePrice': 20800,
    'CE': {              # Call option
        'strikePrice': 20800,
        'expiryDate': '28-Jan-2021',
        'optionType': 'CE',
        'lastPrice': 604,
        'change': -25.15,
        'pChange': -3.99,
        'bid': 602,
        'ask': 606,
        'bidQty': 300,
        'askQty': 300,
        'volume': 1250,
        'openInterest': 3200,
        'impliedVolatility': 48.5,
        'greeks': {
            'delta': 0.85,
            'theta': -5.2,
            'vega': 0.15
        }
    },
    'PE': {              # Put option
        'strikePrice': 20800,
        'expiryDate': '28-Jan-2021',
        'optionType': 'PE',
        'lastPrice': 14,
        'change': -2.5,
        'pChange': -15.15,
        'bid': 13,
        'ask': 15,
        'bidQty': 300,
        'askQty': 300,
        'volume': 850,
        'openInterest': 1200,
        'impliedVolatility': 35.2
    }
}
```

---

## Corporate Announcements

### Get Announcements

```python
# All recent announcements
announcements = n.corporate_announcements()

# Filter by symbol
announcements = n.corporate_announcements(symbol="NH")

# Filter by date range
from datetime import date
announcements = n.corporate_announcements(
    from_date=date(2025, 6, 9),
    to_date=date(2025, 6, 10),
    symbol="NH"
)
```

### Announcement Structure

```python
announcement = announcements[0]

{
    'an_dt': '10-Jun-2025 22:52:36',        # Announcement time
    'symbol': 'NH',
    'sm_name': 'Narayana Hrudayalaya Ltd.',
    'sm_isin': 'INE410P01011',
    'desc': 'General Updates',              # Category
    'attchmntText': 'Lorem ipsum...',       # Announcement text
    'attchmntFile': 'https://...pdf',       # PDF link
    'fileSize': '684 KB',
    'exchdisstime': '10-Jun-2025 22:52:37',
    'sort_date': '2025-06-10 22:52:36',
    'difference': '00:00:01'
}
```

### Common Announcement Types

- General Updates
- Analysts/Institutional Investor Meet/Con. Call Updates
- Press Release
- Board Meetings
- Dividend announcements
- Bonus announcements
- Rights issue
- Merger & Acquisition
- Financial results

---

## Best Practices

### Error Handling

```python
try:
    quote = n.stock_quote("SBIN")
except Exception as e:
    print(f"Error fetching quote: {e}")
    # Handle error appropriately
```

### Rate Limiting

```python
import time
from datetime import date

stocks = ["SBIN", "HDFC", "ICICI"]

for stock in stocks:
    quote = n.stock_quote(stock)
    # Process quote
    time.sleep(1)  # Be respectful to NSE servers
```

### Data Validation

```python
quote = n.stock_quote("SBIN")

# Check if data is available
if quote and 'priceInfo' in quote:
    price = quote['priceInfo']['lastPrice']
    if price > 0:
        print(f"Current price: {price}")
```

### Performance Tips

1. Cache repeated calls
2. Use list comprehensions for filtering
3. Batch process multiple stocks
4. Add delays between API calls
5. Handle temporary network issues with retries

```python
import time
from functools import lru_cache

@lru_cache(maxsize=32)
def get_cached_quote(symbol):
    return n.stock_quote(symbol)

# Subsequent calls return cached value
quote1 = get_cached_quote("SBIN")
quote2 = get_cached_quote("SBIN")  # Same object from cache
```

### Working with Large Data

```python
# Instead of loading all data at once
# for large option chains:

option_chain = n.index_option_chain("NIFTY")
data = option_chain['filtered']['data']

# Process in chunks
chunk_size = 100
for i in range(0, len(data), chunk_size):
    chunk = data[i:i+chunk_size]
    # Process chunk
```
