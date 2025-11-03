# BSE Module

The BSE (Bombay Stock Exchange) module provides access to live market data and corporate announcements from the Bombay Stock Exchange.

## Classes

### BSELive Class

Fetches live data and corporate announcements from BSE.

```python
from jugaad_data.bse import BSELive

bse = BSELive()
```

#### Attributes

- `time_out` (int): Cache timeout in seconds (default: 5)
- `base_url` (str): "https://api.bseindia.com/BseIndiaAPI/api"
- `attachment_base_url` (str): Base URL for downloading attachments

#### Methods

##### `corporate_announcements(scrip_code=None, category="Result", subcategory="Financial+Results", from_date=None, to_date=None, page_no=1, search_type="P", announcement_type="C")`

Fetch corporate announcements from BSE.

**Parameters:**
- `scrip_code` (int): BSE scrip code (e.g., 532174 for ICICI Bank)
- `category` (str): Category filter (default: "Result")
- `subcategory` (str): Subcategory filter (default: "Financial+Results")
- `from_date` (datetime): Start date for filtering
- `to_date` (datetime): End date for filtering
- `page_no` (int): Page number for pagination (default: 1)
- `search_type` (str): Search type (default: "P")
- `announcement_type` (str): Announcement type (default: "C")

**Returns:**
- dict: Response with 'Table' (announcements) and 'Table1' (metadata)

**Example:**
```python
from datetime import datetime
from jugaad_data.bse import BSELive

bse = BSELive()

# Get ICICI Bank announcements
announcements = bse.corporate_announcements(
    scrip_code=532174,
    from_date=datetime(2024, 1, 1),
    to_date=datetime(2024, 12, 31)
)

# Print recent announcements
for announcement in announcements.get('Table', [])[:5]:
    print(f"Date: {announcement['NEWS_DT']}")
    print(f"Subject: {announcement['NEWSSUB']}")
    print(f"Category: {announcement['NEWS_CATEGORY']}")
    print("-" * 50)
```

##### `get_attachment_url(attachment_name)`

Construct full URL for downloading announcement attachments.

**Parameters:**
- `attachment_name` (str): Attachment filename from announcement data

**Returns:**
- str: Full download URL or None if no attachment

**Example:**
```python
# Get announcements with attachments
announcements = bse.corporate_announcements(scrip_code=532174)

for announcement in announcements.get('Table', []):
    attachment = announcement.get('ATTACHMENTNAME')
    if attachment:
        url = bse.get_attachment_url(attachment)
        print(f"Download: {url}")
```

##### `get_announcement_with_urls(scrip_code=None, category="Result", subcategory="Financial+Results", from_date=None, to_date=None, page_no=1, search_type="P", announcement_type="C")`

Convenience method that adds attachment URLs to announcement data.

**Returns:**
- dict: Announcements with added 'attachment_url' and 'file_size_formatted' fields

**Example:**
```python
result = bse.get_announcement_with_urls(scrip_code=532174)

for announcement in result.get('Table', []):
    if announcement.get('attachment_url'):
        print(f"File: {announcement['attachment_url']}")
        print(f"Size: {announcement['file_size_formatted']}")
```

##### `get_scrip_list(group=None, segment="Equity", status=None)`

Fetch list of all BSE scrips (stocks).

**Parameters:**
- `group` (str): Group filter ("A", "B", "X", etc.)
- `segment` (str): Market segment (default: "Equity")
- `status` (str): Status filter ("Active", "Delisted", etc.)

**Returns:**
- list[dict]: List of scrip information

**Example:**
```python
# Get all active scrips
active_scrips = bse.get_scrip_list(status="Active")
print(f"Total active scrips: {len(active_scrips)}")

# Get Group A scrips only
group_a = bse.get_scrip_list(group="A", status="Active")
```

##### `symbol_to_scrip_code(symbol)`

Convert BSE symbol to scrip code.

**Parameters:**
- `symbol` (str): BSE symbol (e.g., "ICICIBANK", "TCS")

**Returns:**
- str: BSE scrip code or None if not found

**Example:**
```python
scrip_code = bse.symbol_to_scrip_code("ICICIBANK")
print(scrip_code)  # Output: "532174"
```

##### `scrip_code_to_symbol(scrip_code)`

Convert BSE scrip code to symbol.

**Parameters:**
- `scrip_code` (str or int): BSE scrip code

**Returns:**
- str: BSE symbol or None if not found

**Example:**
```python
symbol = bse.scrip_code_to_symbol("532174")
print(symbol)  # Output: "ICICIBANK"
```

##### `get_scrip_info(symbol_or_code)`

Get detailed company information.

**Parameters:**
- `symbol_or_code` (str): BSE symbol or scrip code

**Returns:**
- dict: Complete scrip information or None if not found

**Example:**
```python
info = bse.get_scrip_info("ICICIBANK")
if info:
    print(f"Company: {info['Scrip_Name']}")
    print(f"ISIN: {info['ISIN_NUMBER']}")
    print(f"Market Cap: ₹{info['Mktcap']} Cr")
    print(f"Group: {info['GROUP']}")
```

##### `corporate_announcements_by_symbol(symbol, category="Result", subcategory="Financial+Results", from_date=None, to_date=None, page_no=1, search_type="P", announcement_type="C")`

Fetch corporate announcements using symbol instead of scrip code.

**Parameters:**
- `symbol` (str): BSE symbol (automatically converted to scrip code)
- Other parameters: Same as `corporate_announcements()`

**Returns:**
- dict: Corporate announcements data

**Example:**
```python
# Get TCS announcements using symbol
announcements = bse.corporate_announcements_by_symbol(
    symbol="TCS",
    from_date=datetime(2024, 10, 1),
    to_date=datetime(2024, 10, 31)
)
```

## Response Data Structure

### Corporate Announcements Response

```python
{
    'Table': [  # List of announcements
        {
            'SCRIP_CD': '532174',
            'SCRIP_ID': 'ICICIBANK',
            'Scrip_Name': 'ICICI Bank Ltd',
            'NEWS_DT': '16 Sep 2024',
            'NEWS_CATEGORY': 'Result',
            'NEWS_SUB_CATEGORY': 'Financial Results',
            'NEWSSUB': 'Results for the quarter ended June 30, 2024',
            'ATTACHMENTNAME': 'xyz.pdf',
            'Fld_Attachsize': 245760,  # File size in bytes
            # Additional fields...
        }
    ],
    'Table1': [  # Metadata
        {
            'ROWCNT': '150',  # Total records available
            # Additional metadata...
        }
    ]
}
```

### Scrip List Response

```python
[
    {
        'SCRIP_CD': '532174',
        'scrip_id': 'ICICIBANK',
        'Scrip_Name': 'ICICI Bank Ltd',
        'ISIN_NUMBER': 'INE090A01021',
        'GROUP': 'A',
        'Mktcap': '650000.00',  # Market cap in crores
        'status': 'Active',
        # Additional fields...
    }
]
```

## Practical Examples

### Track Company Announcements

```python
from datetime import datetime, timedelta
from jugaad_data.bse import BSELive

def track_company_announcements(symbol, days=30):
    """Track recent announcements for a company"""
    bse = BSELive()
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    try:
        announcements = bse.corporate_announcements_by_symbol(
            symbol=symbol,
            from_date=start_date,
            to_date=end_date
        )
        
        print(f"Recent announcements for {symbol}:")
        print("=" * 50)
        
        for announcement in announcements.get('Table', []):
            print(f"📅 {announcement['NEWS_DT']}")
            print(f"📋 {announcement['NEWSSUB']}")
            print(f"🏷️  {announcement['NEWS_CATEGORY']} - {announcement['NEWS_SUB_CATEGORY']}")
            
            # Check for attachments
            if announcement.get('ATTACHMENTNAME'):
                size = announcement.get('Fld_Attachsize', 0)
                size_mb = size / (1024 * 1024) if size > 1024*1024 else size / 1024
                unit = "MB" if size > 1024*1024 else "KB"
                print(f"📎 Attachment: {announcement['ATTACHMENTNAME']} ({size_mb:.1f} {unit})")
            
            print("-" * 30)
            
    except ValueError as e:
        print(f"Error: {e}")

# Usage
track_company_announcements("ICICIBANK", days=90)
```

### Download Company Financials

```python
import requests
from pathlib import Path

def download_financial_results(symbol, save_dir="downloads"):
    """Download financial result PDFs for a company"""
    bse = BSELive()
    
    # Create download directory
    Path(save_dir).mkdir(exist_ok=True)
    
    # Get announcements with attachment URLs
    result = bse.get_announcement_with_urls(
        scrip_code=bse.symbol_to_scrip_code(symbol),
        category="Result",
        subcategory="Financial+Results"
    )
    
    downloaded = 0
    for announcement in result.get('Table', []):
        if announcement.get('attachment_url'):
            filename = announcement['ATTACHMENTNAME']
            url = announcement['attachment_url']
            
            print(f"Downloading: {filename}")
            
            try:
                response = requests.get(url)
                response.raise_for_status()
                
                file_path = Path(save_dir) / f"{symbol}_{filename}"
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"✅ Saved: {file_path}")
                downloaded += 1
                
            except Exception as e:
                print(f"❌ Failed to download {filename}: {e}")
    
    print(f"\nDownloaded {downloaded} files to {save_dir}/")

# Usage
download_financial_results("TCS")
```

### BSE Symbol Lookup Tool

```python
def search_bse_companies(search_term):
    """Search for BSE companies by name or symbol"""
    bse = BSELive()
    
    scrips = bse.get_scrip_list(status="Active")
    search_term = search_term.upper()
    
    matches = []
    for scrip in scrips:
        symbol = scrip.get('scrip_id', '').upper()
        name = scrip.get('Scrip_Name', '').upper()
        
        if search_term in symbol or search_term in name:
            matches.append(scrip)
    
    print(f"Found {len(matches)} matches for '{search_term}':")
    print("-" * 60)
    
    for match in matches[:10]:  # Top 10 matches
        print(f"Symbol: {match['scrip_id']}")
        print(f"Name: {match['Scrip_Name']}")
        print(f"Code: {match['SCRIP_CD']}")
        print(f"Group: {match['GROUP']}")
        print(f"Market Cap: ₹{match.get('Mktcap', 'N/A')} Cr")
        print("-" * 30)

# Usage
search_bse_companies("BANK")
search_bse_companies("ICICI")
```

### Monitor Multiple Companies

```python
def monitor_announcements(symbols, categories=None):
    """Monitor announcements for multiple companies"""
    bse = BSELive()
    categories = categories or ["Result", "Board Meeting"]
    
    print("📊 BSE Announcements Monitor")
    print("=" * 50)
    
    for symbol in symbols:
        print(f"\n🏢 {symbol}:")
        
        try:
            scrip_code = bse.symbol_to_scrip_code(symbol)
            if not scrip_code:
                print(f"  ❌ Symbol not found")
                continue
            
            for category in categories:
                announcements = bse.corporate_announcements(
                    scrip_code=int(scrip_code),
                    category=category
                )
                
                count = len(announcements.get('Table', []))
                recent = announcements.get('Table', [])[:1]  # Most recent
                
                if recent:
                    latest = recent[0]
                    print(f"  📋 {category}: {count} total")
                    print(f"     Latest: {latest['NEWSSUB'][:50]}...")
                    print(f"     Date: {latest['NEWS_DT']}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")

# Usage
monitor_announcements(["ICICIBANK", "TCS", "RELIANCE", "HDFC"])
```

## Error Handling

### Common Issues

- **Symbol Not Found**: Handle when symbol doesn't exist in BSE scrip list
- **API Errors**: Network issues or API changes
- **Invalid Parameters**: Date format or missing required fields

### Best Practices

```python
def safe_bse_call(func, *args, **kwargs):
    """Safely execute BSE API calls with error handling"""
    try:
        return func(*args, **kwargs)
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None
    except KeyError as e:
        print(f"Data structure changed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# Usage
bse = BSELive()
result = safe_bse_call(bse.corporate_announcements, scrip_code=532174)
if result:
    print(f"Found {len(result.get('Table', []))} announcements")
```

## Caching and Performance

- Built-in live caching with 5-second timeout
- Symbol/scrip code mapping cached for performance
- Automatic session management
- Efficient bulk operations for multiple symbols