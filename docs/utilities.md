# Utilities

The utilities module provides helper functions, decorators, and common functionality used across the jugaad-data library.

## Functions

### Data Type Conversion

#### `np_float(num)`
Convert value to numpy float64 with error handling.

**Parameters:**
- `num` (any): Value to convert

**Returns:**
- numpy.float64: Converted number or NaN if conversion fails

**Requires:** numpy to be installed

**Example:**
```python
from jugaad_data.util import np_float

value = np_float("123.45")  # Returns np.float64(123.45)
invalid = np_float("abc")   # Returns np.nan
```

#### `np_date(dt)`
Convert date string to numpy datetime64 with multiple format support.

**Parameters:**
- `dt` (str): Date string in various formats

**Returns:**
- numpy.datetime64: Converted date or NaT if conversion fails

**Supported Formats:**
- Standard datetime objects
- "DD-MMM-YYYY" (e.g., "01-JAN-2020")
- "DD MMM YYYY" (e.g., "01 JAN 2020")

**Example:**
```python
from jugaad_data.util import np_date

date1 = np_date("01-JAN-2020")  # numpy.datetime64('2020-01-01')
date2 = np_date("invalid")      # numpy.datetime64('NaT')
```

#### `np_int(num)`
Convert value to numpy int64 with error handling.

**Parameters:**
- `num` (any): Value to convert

**Returns:**
- numpy.int64: Converted integer or 0 if conversion fails

### Date Range Utilities

#### `break_dates(from_date, to_date)`
Break a date range into monthly chunks for efficient API usage.

**Parameters:**
- `from_date` (date): Start date
- `to_date` (date): End date

**Returns:**
- list[tuple]: List of (start_date, end_date) tuples for each month

**Example:**
```python
from datetime import date
from jugaad_data.util import break_dates

ranges = break_dates(date(2020, 1, 15), date(2020, 3, 10))
# Returns: [(date(2020, 1, 15), date(2020, 1, 31)), 
#           (date(2020, 2, 1), date(2020, 2, 29)), 
#           (date(2020, 3, 1), date(2020, 3, 10))]
```

### File and Cache Utilities

#### `kw_to_fname(**kw)`
Generate filename from keyword arguments for caching.

**Parameters:**
- `**kw`: Keyword arguments

**Returns:**
- str: Filename string based on sorted keyword arguments

**Example:**
```python
from jugaad_data.util import kw_to_fname

filename = kw_to_fname(symbol="SBIN", from_date="2020-01-01", series="EQ")
# Returns: "from_date-2020-01-01-series-EQ-symbol-SBIN"
```

### Threading and Parallel Processing

#### `pool(function, params, use_threads=True, max_workers=2)`
Execute function with multiple parameter sets using threading or sequential processing.

**Parameters:**
- `function` (callable): Function to execute
- `params` (list): List of parameter tuples for function calls
- `use_threads` (bool): Use ThreadPoolExecutor if True, sequential if False
- `max_workers` (int): Maximum number of worker threads

**Returns:**
- list: Results from all function calls

**Example:**
```python
from jugaad_data.util import pool

def fetch_data(symbol, date):
    # Some data fetching logic
    return f"Data for {symbol} on {date}"

params = [("SBIN", "2020-01-01"), ("HDFC", "2020-01-01")]
results = pool(fetch_data, params, max_workers=4)
# Returns: ["Data for SBIN on 2020-01-01", "Data for HDFC on 2020-01-01"]
```

## Decorators

### `@cached(app_name)`
File-based caching decorator for expensive function calls.

**Parameters:**
- `app_name` (str): Application name for cache directory organization

**Cache Location:**
- Default: `user_cache_dir(app_name, app_name)` (OS-specific)
- Override: Set `J_CACHE_DIR` environment variable

**Example:**
```python
from jugaad_data.util import cached

@cached("myapp")
def expensive_function(symbol, date):
    # Expensive operation (API call, computation, etc.)
    return f"Processed data for {symbol} on {date}"

# First call - executes function and caches result
result1 = expensive_function("SBIN", "2020-01-01")

# Second call - returns cached result
result2 = expensive_function("SBIN", "2020-01-01")  # Fast!
```

**Cache Behavior:**
- Creates cache directory if it doesn't exist
- Uses pickle for serialization
- Cache key generated from function parameters
- Persistent across Python sessions

### `@live_cache`
Memory-based caching decorator for live data with timeout.

**Cache Duration:** Configurable via `self.time_out` attribute (default: 5 seconds)

**Example:**
```python
from jugaad_data.util import live_cache

class DataFetcher:
    def __init__(self):
        self.time_out = 10  # Cache for 10 seconds
    
    @live_cache
    def get_live_price(self, symbol):
        # Fetch live price from API
        return f"Live price for {symbol}"

fetcher = DataFetcher()
price1 = fetcher.get_live_price("SBIN")  # API call
price2 = fetcher.get_live_price("SBIN")  # Cached (within 10 seconds)
```

**Cache Behavior:**
- Memory-based (not persistent)
- Separate cache per class instance
- Automatic expiration based on timestamp
- Ideal for live data that changes frequently

## Error Handling Decorators

### `@np_exception`
Decorator to handle numpy import errors gracefully.

**Usage:**
```python
from jugaad_data.util import np_exception

@np_exception
def process_data():
    import numpy as np
    return np.array([1, 2, 3])

# Raises ModuleNotFoundError if numpy not installed
result = process_data()
```

## Cache Management

### Environment Variables

- `J_CACHE_DIR`: Override default cache directory location

**Example:**
```bash
# Set custom cache directory
export J_CACHE_DIR="/path/to/custom/cache"

# Or in Python
import os
os.environ['J_CACHE_DIR'] = "/path/to/custom/cache"
```

### Cache Directory Structure

```
cache_dir/
├── nsehistory-stock/
│   ├── from_date-2020-01-01-series-EQ-symbol-SBIN-to_date-2020-01-31
│   └── ...
├── nsehistory-index/
└── ...
```

## Usage Examples

### Advanced Caching Strategy

```python
import os
from jugaad_data.util import cached, break_dates
from datetime import date

# Set custom cache location
os.environ['J_CACHE_DIR'] = "./my_cache"

@cached("stock_analysis")
def analyze_stock(symbol, from_date, to_date):
    """Expensive stock analysis with caching"""
    print(f"Analyzing {symbol} from {from_date} to {to_date}")
    
    # Simulate expensive computation
    import time
    time.sleep(2)
    
    return {
        'symbol': symbol,
        'analysis': f"Complex analysis for {symbol}",
        'period': f"{from_date} to {to_date}"
    }

# First call - takes 2+ seconds
result1 = analyze_stock("SBIN", date(2020, 1, 1), date(2020, 1, 31))

# Second call - instant (cached)
result2 = analyze_stock("SBIN", date(2020, 1, 1), date(2020, 1, 31))
```

### Parallel Data Processing

```python
from jugaad_data.util import pool, break_dates
from datetime import date

def fetch_monthly_data(symbol, start_date, end_date):
    """Simulate monthly data fetch"""
    return f"Data for {symbol}: {start_date} to {end_date}"

# Break large date range into monthly chunks
symbol = "SBIN"
from_date = date(2020, 1, 1)
to_date = date(2020, 12, 31)

date_ranges = break_dates(from_date, to_date)
params = [(symbol, start, end) for start, end in date_ranges]

# Fetch all months in parallel
results = pool(fetch_monthly_data, params, max_workers=4)

print(f"Fetched {len(results)} months of data")
for result in results[:3]:  # Show first 3
    print(result)
```

### Custom Live Cache Implementation

```python
from datetime import datetime, timedelta
from jugaad_data.util import live_cache

class CustomLiveData:
    def __init__(self, cache_timeout=30):
        self.time_out = cache_timeout  # Cache for 30 seconds
        
    @live_cache
    def get_market_status(self):
        """Get market status with caching"""
        print("Fetching fresh market status...")
        # Simulate API call
        return {
            'status': 'OPEN',
            'timestamp': datetime.now().isoformat()
        }
    
    @live_cache
    def get_stock_price(self, symbol):
        """Get stock price with caching"""
        print(f"Fetching fresh price for {symbol}...")
        # Simulate price fetch
        import random
        return {
            'symbol': symbol,
            'price': round(random.uniform(100, 500), 2),
            'timestamp': datetime.now().isoformat()
        }

# Usage
data_source = CustomLiveData(cache_timeout=15)

# First calls - fetch fresh data
status1 = data_source.get_market_status()
price1 = data_source.get_stock_price("SBIN")

# Subsequent calls within 15 seconds - return cached data
status2 = data_source.get_market_status()  # Cached
price2 = data_source.get_stock_price("SBIN")  # Cached

print("Status from cache:", status1 == status2)
print("Price from cache:", price1 == price2)
```

### Data Type Conversion Pipeline

```python
from jugaad_data.util import np_float, np_date, np_int

def clean_financial_data(raw_data):
    """Clean and convert financial data types"""
    cleaned = []
    
    for record in raw_data:
        cleaned_record = {
            'date': np_date(record['date']),
            'open': np_float(record['open']),
            'high': np_float(record['high']),
            'low': np_float(record['low']),
            'close': np_float(record['close']),
            'volume': np_int(record['volume']),
            'symbol': record['symbol']  # Keep as string
        }
        cleaned.append(cleaned_record)
    
    return cleaned

# Example usage
raw_data = [
    {
        'date': '01-JAN-2020',
        'open': '100.50',
        'high': '105.75',
        'low': '99.25',
        'close': '103.00',
        'volume': '1500000',
        'symbol': 'SBIN'
    }
]

cleaned_data = clean_financial_data(raw_data)
print(cleaned_data[0])
```

## Best Practices

### Caching Guidelines

1. **Use @cached for Historical Data**: Historical data doesn't change, ideal for persistent caching
2. **Use @live_cache for Real-time Data**: Live data changes frequently, use short-term memory caching
3. **Set Appropriate Cache Timeouts**: Balance freshness vs. performance
4. **Monitor Cache Size**: Large caches can consume significant disk space

### Performance Optimization

1. **Use Parallel Processing**: Leverage `pool()` for I/O-bound operations
2. **Break Large Date Ranges**: Use `break_dates()` for efficient API usage
3. **Handle Data Type Conversion**: Use utility functions for robust data processing
4. **Implement Proper Error Handling**: Use decorators and try-catch blocks

### Memory Management

1. **Clear Caches Periodically**: Remove old cache files to free disk space
2. **Use Appropriate Data Types**: Convert to numpy types for memory efficiency
3. **Limit Worker Threads**: Don't exceed system capabilities