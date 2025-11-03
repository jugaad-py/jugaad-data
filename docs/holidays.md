# Holidays Module

The holidays module provides a comprehensive list of trading holidays for Indian stock exchanges to help avoid requesting data on non-trading days.

## Functions

### `holidays(year=None, month=None)`

Get list of trading holidays for Indian stock exchanges.

**Parameters:**
- `year` (int, optional): Filter holidays by specific year
- `month` (int, optional): Filter holidays by specific month (1-12)

**Returns:**
- list[date]: List of holiday dates

**Example:**
```python
from jugaad_data.holidays import holidays
from datetime import date

# Get all holidays
all_holidays = holidays()
print(f"Total holidays: {len(all_holidays)}")

# Get holidays for 2024
holidays_2024 = holidays(year=2024)
print(f"Holidays in 2024: {len(holidays_2024)}")

# Get holidays for January 2024
jan_2024_holidays = holidays(year=2024, month=1)
for holiday in jan_2024_holidays:
    print(holiday)
```

## Holiday Coverage

The module contains holidays from **1997 to 2025**, including:

- **National Holidays**: Republic Day, Independence Day, Gandhi Jayanti
- **Religious Festivals**: Diwali, Holi, Eid, Christmas, Dussehra
- **Regional Observances**: State-specific holidays affecting exchanges
- **Special Market Closures**: Emergency closures and special events

## Practical Usage

### Check if Date is Trading Day

```python
from jugaad_data.holidays import holidays
from datetime import date

def is_trading_day(check_date):
    """Check if a date is a trading day"""
    # Get holidays for the year
    year_holidays = holidays(year=check_date.year)
    
    # Check if weekend (Saturday=5, Sunday=6)
    if check_date.weekday() >= 5:
        return False
    
    # Check if holiday
    if check_date in year_holidays:
        return False
    
    return True

# Usage
test_date = date(2024, 1, 26)  # Republic Day
print(f"Is {test_date} a trading day? {is_trading_day(test_date)}")
```

### Generate Trading Calendar

```python
from jugaad_data.holidays import holidays
from datetime import date, timedelta

def trading_calendar(start_date, end_date):
    """Generate list of trading days between two dates"""
    trading_days = []
    holiday_list = holidays()
    
    current_date = start_date
    while current_date <= end_date:
        # Skip weekends and holidays
        if current_date.weekday() < 5 and current_date not in holiday_list:
            trading_days.append(current_date)
        current_date += timedelta(days=1)
    
    return trading_days

# Get trading days for January 2024
jan_trading_days = trading_calendar(date(2024, 1, 1), date(2024, 1, 31))
print(f"Trading days in January 2024: {len(jan_trading_days)}")
```

### Safe Data Download

```python
from jugaad_data.holidays import holidays
from jugaad_data.nse import bhavcopy_save
from datetime import date, timedelta

def safe_bhavcopy_download(start_date, end_date, dest_dir):
    """Download bhavcopy files only for trading days"""
    holiday_list = holidays()
    failed_downloads = []
    successful_downloads = []
    
    current_date = start_date
    while current_date <= end_date:
        # Only try trading days
        if current_date.weekday() < 5 and current_date not in holiday_list:
            try:
                file_path = bhavcopy_save(current_date, dest_dir)
                successful_downloads.append((current_date, file_path))
                print(f"✅ Downloaded: {current_date}")
            except Exception as e:
                failed_downloads.append((current_date, str(e)))
                print(f"❌ Failed: {current_date} - {e}")
        else:
            print(f"⏭️  Skipped: {current_date} (Holiday/Weekend)")
        
        current_date += timedelta(days=1)
    
    return successful_downloads, failed_downloads

# Usage
downloads, failures = safe_bhavcopy_download(
    date(2024, 1, 1), 
    date(2024, 1, 31), 
    "./bhavcopy/"
)
```

## Integration with CLI

The holidays module can be used to enhance CLI operations:

```python
from jugaad_data.holidays import holidays
import sys
from datetime import date

def validate_trading_date(date_str):
    """Validate if a date string represents a trading day"""
    try:
        check_date = date.fromisoformat(date_str)
        holiday_list = holidays(year=check_date.year)
        
        if check_date.weekday() >= 5:
            print(f"Warning: {date_str} is a weekend")
            return False
        
        if check_date in holiday_list:
            print(f"Warning: {date_str} is a trading holiday")
            return False
        
        return True
    except ValueError:
        print(f"Error: Invalid date format {date_str}")
        return False

# Usage in scripts
if __name__ == "__main__":
    if len(sys.argv) > 1:
        date_to_check = sys.argv[1]
        if validate_trading_date(date_to_check):
            print(f"{date_to_check} is a valid trading day")
        else:
            print(f"{date_to_check} is not a trading day")
```

## Holiday Analysis

### Monthly Holiday Distribution

```python
from jugaad_data.holidays import holidays
from collections import Counter
import calendar

def analyze_holiday_distribution(year):
    """Analyze holiday distribution by month"""
    year_holidays = holidays(year=year)
    
    # Count holidays by month
    month_counts = Counter(holiday.month for holiday in year_holidays)
    
    print(f"Holiday Distribution for {year}:")
    print("-" * 30)
    
    for month in range(1, 13):
        month_name = calendar.month_name[month]
        count = month_counts.get(month, 0)
        print(f"{month_name:12}: {count} holidays")
    
    # Find month with most holidays
    if month_counts:
        max_month = max(month_counts, key=month_counts.get)
        max_count = month_counts[max_month]
        print(f"\nMonth with most holidays: {calendar.month_name[max_month]} ({max_count})")

# Usage
analyze_holiday_distribution(2024)
```

### Trading Days Per Month

```python
from jugaad_data.holidays import holidays
import calendar
from datetime import date

def trading_days_per_month(year):
    """Calculate number of trading days per month"""
    year_holidays = holidays(year=year)
    
    print(f"Trading Days per Month - {year}:")
    print("-" * 40)
    
    total_trading_days = 0
    
    for month in range(1, 13):
        # Get number of days in month
        days_in_month = calendar.monthrange(year, month)[1]
        
        trading_days = 0
        for day in range(1, days_in_month + 1):
            check_date = date(year, month, day)
            
            # Skip weekends and holidays
            if check_date.weekday() < 5 and check_date not in year_holidays:
                trading_days += 1
        
        month_name = calendar.month_name[month]
        print(f"{month_name:12}: {trading_days:2d} trading days")
        total_trading_days += trading_days
    
    print(f"\nTotal trading days in {year}: {total_trading_days}")
    return total_trading_days

# Usage
trading_days_per_month(2024)
```

## Data Source and Accuracy

The holiday data is based on:
- **Zipline Trading Calendar**: Reference implementation for holiday calendars
- **NSE Official Circulars**: Exchange notifications for trading holidays
- **Historical Records**: Verified against actual market closures

### Coverage Notes

- **Weekend Handling**: Module only contains specific holidays, weekends should be handled separately
- **Emergency Closures**: Special market closures due to extraordinary circumstances may not be included
- **Regional Variations**: Some holidays may vary by exchange or region

## Custom Holiday Management

### Extend Holiday List

```python
from jugaad_data.holidays import holidays
from datetime import date

def custom_holidays(year=None, additional_holidays=None):
    """Extend official holidays with custom dates"""
    official_holidays = holidays(year=year)
    
    if additional_holidays:
        # Add custom holidays
        all_holidays = official_holidays + additional_holidays
        # Remove duplicates and sort
        all_holidays = sorted(list(set(all_holidays)))
        
        # Filter by year if specified
        if year:
            all_holidays = [h for h in all_holidays if h.year == year]
        
        return all_holidays
    
    return official_holidays

# Usage - add company-specific holidays
company_holidays = [
    date(2024, 3, 15),  # Company foundation day
    date(2024, 8, 30),  # Special company holiday
]

extended_holidays = custom_holidays(
    year=2024, 
    additional_holidays=company_holidays
)
```

### Holiday Validation

```python
from jugaad_data.holidays import holidays
from datetime import date

def validate_date_range(start_date, end_date, min_trading_days=1):
    """Validate that a date range has minimum trading days"""
    holiday_list = holidays()
    trading_days = 0
    
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5 and current_date not in holiday_list:
            trading_days += 1
        current_date += timedelta(days=1)
    
    if trading_days < min_trading_days:
        raise ValueError(f"Date range has only {trading_days} trading days, minimum {min_trading_days} required")
    
    return trading_days

# Usage
try:
    days = validate_date_range(date(2024, 1, 26), date(2024, 1, 28), min_trading_days=2)
    print(f"Valid range with {days} trading days")
except ValueError as e:
    print(f"Invalid range: {e}")
```

## Best Practices

1. **Always Check Holidays**: Before downloading historical data, verify dates are trading days
2. **Use in Batch Operations**: Integrate holiday checking in automated download scripts
3. **Handle Edge Cases**: Account for emergency market closures not in the list
4. **Validate Date Ranges**: Ensure sufficient trading days in analysis periods
5. **Update Regularly**: Keep library updated for latest holiday information