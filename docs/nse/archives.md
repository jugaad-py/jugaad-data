# NSE Archives

The NSE Archives module provides access to historical archival data from NSE including bhavcopy files, bulk deals, and derivatives data.

## Classes

### NSEArchives Class

Downloads archival data from NSE Archives website.

```python
from jugaad_data.nse.archives import NSEArchives

archives = NSEArchives()
```

#### Attributes

- `base_url` (str): "https://nsearchives.nseindia.com/"
- `timeout` (int): Request timeout in seconds (default: 4)

#### Methods

##### `bhavcopy_raw(dt)`
Downloads raw bhavcopy text for a specific date.

**Parameters:**
- `dt` (date): Date for which to download bhavcopy

**Returns:**
- str: Raw CSV content of bhavcopy

**Example:**
```python
from datetime import date
archives = NSEArchives()
data = archives.bhavcopy_raw(date(2020, 1, 1))
```

##### `bhavcopy_save(dt, dest, skip_if_present=True)`
Downloads and saves bhavcopy CSV file.

**Parameters:**
- `dt` (date): Date for bhavcopy
- `dest` (str): Destination directory path
- `skip_if_present` (bool): Skip if file already exists

**Returns:**
- str: Path to saved file

**Example:**
```python
path = archives.bhavcopy_save(date(2020, 1, 1), "/path/to/save/")
```

##### `full_bhavcopy_raw(dt)`
Downloads full bhavcopy data (more detailed than regular bhavcopy).

**Parameters:**
- `dt` (date): Date for bhavcopy

**Returns:**
- str: Raw CSV content

**Note:** Full bhavcopy may not be available for dates before 2020.

##### `full_bhavcopy_save(dt, dest, skip_if_present=True)`
Downloads and saves full bhavcopy CSV file.

**Parameters:**
- `dt` (date): Date for bhavcopy  
- `dest` (str): Destination directory
- `skip_if_present` (bool): Skip if file exists

**Returns:**
- str: Path to saved file

##### `bhavcopy_fo_raw(dt)`
Downloads raw F&O (Futures & Options) bhavcopy text.

**Parameters:**
- `dt` (date): Date for F&O bhavcopy

**Returns:**
- str: Raw CSV content

##### `bhavcopy_fo_save(dt, dest, skip_if_present=True)`
Downloads and saves F&O bhavcopy CSV file.

**Parameters:**
- `dt` (date): Date for bhavcopy
- `dest` (str): Destination directory  
- `skip_if_present` (bool): Skip if file exists

**Returns:**
- str: Path to saved file

##### `bulk_deals_raw()`
Downloads current bulk deals data.

**Returns:**
- str: Raw CSV content of bulk deals

##### `bulk_deals_save(fname)`
Downloads and saves bulk deals to file.

**Parameters:**
- `fname` (str): Output file path

### NSEIndicesArchives Class

Downloads index bhavcopy data from NSE Indices website.

```python
from jugaad_data.nse.archives import NSEIndicesArchives

index_archives = NSEIndicesArchives()
```

#### Attributes

- `base_url` (str): "https://www.niftyindices.com"

#### Methods

##### `bhavcopy_index_raw(dt)`
Downloads raw index bhavcopy text.

**Parameters:**
- `dt` (date): Date for index bhavcopy

**Returns:**
- str: Raw CSV content

##### `bhavcopy_index_save(dt, dest, skip_if_present=True)`
Downloads and saves index bhavcopy CSV file.

**Parameters:**
- `dt` (date): Date for bhavcopy
- `dest` (str): Destination directory
- `skip_if_present` (bool): Skip if file exists

**Returns:**
- str: Path to saved file

## Module-level Functions

These are convenience functions that use pre-instantiated class objects:

### Equity Archives
- `bhavcopy_raw(dt)` - Raw equity bhavcopy
- `bhavcopy_save(dt, dest, skip_if_present=True)` - Save equity bhavcopy
- `full_bhavcopy_raw(dt)` - Raw full equity bhavcopy  
- `full_bhavcopy_save(dt, dest, skip_if_present=True)` - Save full equity bhavcopy

### F&O Archives
- `bhavcopy_fo_raw(dt)` - Raw F&O bhavcopy
- `bhavcopy_fo_save(dt, dest, skip_if_present=True)` - Save F&O bhavcopy

### Index Archives  
- `bhavcopy_index_raw(dt)` - Raw index bhavcopy
- `bhavcopy_index_save(dt, dest, skip_if_present=True)` - Save index bhavcopy

### Utility Functions

#### `expiry_dates(dt, instrument_type="", symbol="", contracts=0)`
Extract expiry dates from F&O bhavcopy data.

**Parameters:**
- `dt` (date): Date for F&O bhavcopy
- `instrument_type` (str): Filter by instrument type (optional)
- `symbol` (str): Filter by symbol (optional)  
- `contracts` (int): Minimum open interest filter (default: 0)

**Returns:**
- list[date]: List of unique expiry dates

**Example:**
```python
from datetime import date
from jugaad_data.nse.archives import expiry_dates

# Get all expiry dates
expiries = expiry_dates(date(2020, 1, 1))

# Get expiry dates for NIFTY index options
nifty_expiries = expiry_dates(date(2020, 1, 1), 
                             instrument_type="OPTIDX", 
                             symbol="NIFTY")
```

## File Naming Conventions

### Equity Bhavcopy
- Format: `cm{dd}{MMM}{yyyy}bhav.csv`
- Example: `cm01JAN2020bhav.csv`

### Full Bhavcopy  
- Format: `sec_bhavdata_full_{dd}{mm}{yyyy}bhav.csv`
- Example: `sec_bhavdata_full_01012020bhav.csv`

### F&O Bhavcopy
- Format: `fo{dd}{MMM}{yyyy}bhav.csv`  
- Example: `fo01JAN2020bhav.csv`

### Index Bhavcopy
- Format: `ind_close_all_{dd}{mm}{yyyy}.csv`
- Example: `ind_close_all_01012020.csv`

## Error Handling

### Common Exceptions

- **requests.exceptions.ReadTimeout**: Network timeout or data not available
  - Often occurs for holidays or when servers are down
  - For full bhavcopy, may indicate data not available for older dates

### Best Practices

1. **Check for Holidays**: Use the holidays module to avoid requesting data for non-trading days
2. **Handle Timeouts**: Wrap calls in try-catch blocks
3. **Batch Downloads**: Use skip_if_present=True for bulk downloads
4. **Verify Dates**: Ensure dates are trading days

## Example Usage

### Download Multiple Bhavcopy Files

```python
from datetime import date, timedelta
from jugaad_data.nse.archives import bhavcopy_save
from jugaad_data.holidays import holidays

start_date = date(2020, 1, 1)
end_date = date(2020, 1, 31)
dest_dir = "/path/to/bhavcopy/"

# Get list of holidays to skip
holiday_list = holidays(2020)

current_date = start_date
while current_date <= end_date:
    # Skip weekends and holidays
    if current_date.weekday() < 5 and current_date not in holiday_list:
        try:
            path = bhavcopy_save(current_date, dest_dir)
            print(f"Downloaded: {path}")
        except Exception as e:
            print(f"Failed for {current_date}: {e}")
    
    current_date += timedelta(days=1)
```

### Extract F&O Contract Information

```python
from datetime import date
from jugaad_data.nse.archives import bhavcopy_fo_raw

# Get F&O data and parse contracts
dt = date(2020, 1, 1)
fo_data = bhavcopy_fo_raw(dt)

# Parse CSV data
import csv
import io

reader = csv.DictReader(io.StringIO(fo_data))
contracts = list(reader)

# Filter for NIFTY options
nifty_options = [c for c in contracts 
                 if c['SYMBOL'] == 'NIFTY' and c['INSTRUMENT'] == 'OPTIDX']

print(f"Found {len(nifty_options)} NIFTY option contracts")
```