# RBI Module

The RBI (Reserve Bank of India) module provides access to economic data and current interest rates from the Reserve Bank of India website.

## Classes

### RBI Class

Fetches current interest rates and economic data from RBI website.

```python
from jugaad_data.rbi import RBI

rbi = RBI()
```

#### Attributes

- `base_url` (str): "https://www.rbi.org.in/"

#### Methods

##### `current_rates()`

Fetch current interest rates and policy rates from RBI.

**Returns:**
- dict: Current rates and policy information

**Example:**
```python
from jugaad_data.rbi import RBI

rbi = RBI()
rates = rbi.current_rates()

# Print all available rates
for rate_name, rate_value in rates.items():
    print(f"{rate_name}: {rate_value}")
```

**Common Rate Types:**
- Policy Repo Rate
- Standing Deposit Facility Rate  
- Marginal Standing Facility Rate
- Bank Rate
- 91 day T-bills
- Savings Deposit Rate
- Term Deposit Rates

## Data Extraction

The module uses intelligent data extraction from RBI's website:

### Table-based Extraction
- Parses HTML tables containing rate information
- Handles multiple table formats and structures
- Automatically cleans data by removing special characters

### Text Pattern Matching
- Uses regex patterns to find rates in text content
- Specifically looks for T-bills and other instruments
- Handles various date and percentage formats

### Rate Mapping
- Maps RBI rate names to standardized keys
- Ensures consistency across different page layouts
- Provides fallback for legacy HTML structures

## Response Format

```python
{
    'Policy Repo Rate': '6.50%',
    'Marginal Standing Facility Rate': '6.75%', 
    'Savings Deposit Rate': '4.00%',
    '91 day T-bills': '6.45%',
    'Bank Rate': '6.75%',
    # Additional rates as available...
}
```

## Examples

### Basic Rate Fetching

```python
from jugaad_data.rbi import RBI

def get_current_rates():
    """Fetch and display current RBI rates"""
    rbi = RBI()
    
    try:
        rates = rbi.current_rates()
        
        print("🏦 Current RBI Rates")
        print("=" * 30)
        
        # Key policy rates
        policy_rates = [
            'Policy Repo Rate',
            'Marginal Standing Facility Rate', 
            'Bank Rate'
        ]
        
        print("📈 Policy Rates:")
        for rate in policy_rates:
            if rate in rates:
                print(f"  {rate}: {rates[rate]}")
        
        # Market rates
        print("\n💰 Market Rates:")
        for rate_name, rate_value in rates.items():
            if rate_name not in policy_rates:
                print(f"  {rate_name}: {rate_value}")
                
    except Exception as e:
        print(f"Error fetching rates: {e}")

# Usage
get_current_rates()
```

### Rate Change Tracking

```python
import json
from datetime import datetime
from pathlib import Path

def track_rate_changes(history_file="rate_history.json"):
    """Track RBI rate changes over time"""
    rbi = RBI()
    
    # Load existing history
    history_path = Path(history_file)
    if history_path.exists():
        with open(history_path, 'r') as f:
            history = json.load(f)
    else:
        history = []
    
    # Get current rates
    current_rates = rbi.current_rates()
    current_entry = {
        'date': datetime.now().isoformat(),
        'rates': current_rates
    }
    
    # Check for changes
    if history:
        last_rates = history[-1]['rates']
        changes = {}
        
        for rate_name, current_value in current_rates.items():
            last_value = last_rates.get(rate_name)
            if last_value and last_value != current_value:
                changes[rate_name] = {
                    'from': last_value,
                    'to': current_value
                }
        
        if changes:
            print("🚨 Rate Changes Detected!")
            for rate_name, change in changes.items():
                print(f"  {rate_name}: {change['from']} → {change['to']}")
            
            current_entry['changes'] = changes
        else:
            print("ℹ️  No rate changes since last check")
    
    # Save updated history
    history.append(current_entry)
    with open(history_path, 'w') as f:
        json.dump(history, f, indent=2)
    
    return current_rates

# Usage
track_rate_changes()
```

### Economic Dashboard

```python
from jugaad_data.rbi import RBI
from jugaad_data.nse import NSELive

def economic_dashboard():
    """Create a simple economic dashboard"""
    print("📊 Economic Dashboard")
    print("=" * 50)
    
    # RBI Rates
    print("🏦 RBI Policy Rates:")
    try:
        rbi = RBI()
        rates = rbi.current_rates()
        
        key_rates = ['Policy Repo Rate', 'Bank Rate', '91 day T-bills']
        for rate in key_rates:
            if rate in rates:
                print(f"  {rate}: {rates[rate]}")
    except Exception as e:
        print(f"  Error fetching RBI rates: {e}")
    
    # Market Indices
    print("\n📈 Market Indices:")
    try:
        nse = NSELive()
        indices = nse.all_indices()
        
        key_indices = ['NIFTY 50', 'NIFTY BANK', 'NIFTY IT']
        for index_data in indices['data']:
            if index_data['index'] in key_indices:
                change_symbol = "📈" if index_data['change'] > 0 else "📉"
                print(f"  {index_data['index']}: {index_data['last']} {change_symbol} {index_data['change']:.2f}")
    except Exception as e:
        print(f"  Error fetching market data: {e}")

# Usage
economic_dashboard()
```

### Rate Comparison Tool

```python
def compare_rates_with_benchmarks():
    """Compare current RBI rates with typical benchmarks"""
    rbi = RBI()
    
    try:
        rates = rbi.current_rates()
        
        # Define typical rate relationships
        benchmarks = {
            'Policy Repo Rate': {
                'description': 'Primary policy tool for liquidity',
                'typical_range': (4.0, 8.0)
            },
            'Marginal Standing Facility Rate': {
                'description': 'Emergency lending rate (usually Repo + 0.25%)',
                'typical_range': (4.25, 8.25)
            },
            'Bank Rate': {
                'description': 'Long-term lending rate',
                'typical_range': (4.25, 8.25)
            }
        }
        
        print("🎯 Rate Analysis")
        print("=" * 40)
        
        for rate_name, info in benchmarks.items():
            if rate_name in rates:
                rate_str = rates[rate_name]
                # Extract numeric value (assuming format like "6.50%")
                try:
                    rate_value = float(rate_str.replace('%', ''))
                    min_range, max_range = info['typical_range']
                    
                    if rate_value < min_range:
                        status = "🔵 Below typical range"
                    elif rate_value > max_range:
                        status = "🔴 Above typical range"
                    else:
                        status = "🟢 Within typical range"
                    
                    print(f"{rate_name}: {rate_str}")
                    print(f"  {info['description']}")
                    print(f"  {status} ({min_range}% - {max_range}%)")
                    print()
                    
                except ValueError:
                    print(f"{rate_name}: {rate_str} (Unable to parse)")
    
    except Exception as e:
        print(f"Error: {e}")

# Usage
compare_rates_with_benchmarks()
```

## Technical Implementation

### Web Scraping Strategy

The RBI module uses a robust web scraping approach:

1. **Session Management**: Uses requests.Session for efficient connection handling
2. **HTML Parsing**: BeautifulSoup for parsing complex HTML structures  
3. **Multiple Extraction Methods**: Both table-based and pattern-based extraction
4. **Data Cleaning**: Automatic removal of formatting characters and normalization

### Extraction Functions

#### `tr_to_json(wrapper)`
Legacy function for extracting rates from table rows.

#### `extract_rates_from_tables(bs)`
Modern function that:
- Finds all tables in the page
- Extracts key-value pairs from table cells
- Applies intelligent filtering for rate data
- Maps common rate names to standardized keys
- Uses regex patterns for specific instruments

### Error Handling

The module handles various edge cases:
- **Page Structure Changes**: Multiple extraction methods provide fallbacks
- **Network Issues**: Standard requests exception handling
- **Data Format Changes**: Flexible parsing with multiple patterns
- **Missing Data**: Graceful handling of incomplete rate information

## Data Reliability

### Update Frequency
- RBI typically updates rates during policy meetings
- Emergency rate changes may occur outside scheduled meetings
- Some rates (like T-bills) may update more frequently

### Data Accuracy
- Data extracted directly from official RBI website
- Multiple extraction methods ensure reliability
- Historical tracking can help identify data inconsistencies

### Limitations
- Dependent on RBI website structure
- May not capture all available rates if page format changes
- No historical rate data (only current rates)

## Integration Examples

### Combine with Market Data

```python
from jugaad_data.rbi import RBI
from jugaad_data.nse import NSELive

def interest_rate_impact_analysis():
    """Analyze potential impact of interest rates on banking stocks"""
    
    # Get current rates
    rbi = RBI()
    rates = rbi.current_rates()
    repo_rate = rates.get('Policy Repo Rate', 'N/A')
    
    # Get banking index
    nse = NSELive()
    bank_index = nse.live_index("NIFTY BANK")
    
    print(f"📊 Interest Rate Impact Analysis")
    print(f"Current Repo Rate: {repo_rate}")
    print(f"NIFTY Bank Index: {bank_index['data'][0]['last']}")
    print(f"Bank Index Change: {bank_index['data'][0]['change']:.2f}")
    
    # Get individual banking stocks
    banking_stocks = ["HDFCBANK", "ICICIBANK", "SBIN", "KOTAKBANK"]
    
    print(f"\n🏦 Banking Stock Performance:")
    for stock in banking_stocks:
        try:
            quote = nse.stock_quote(stock)
            price_info = quote['priceInfo']
            change_symbol = "📈" if price_info['change'] > 0 else "📉"
            print(f"  {stock}: ₹{price_info['lastPrice']} {change_symbol} {price_info['pChange']:.2f}%")
        except:
            print(f"  {stock}: Data unavailable")

# Usage
interest_rate_impact_analysis()
```