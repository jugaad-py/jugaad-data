# Command Line Interface (CLI)

The Jugaad Data CLI provides powerful command-line tools for downloading market data without needing to write Python code.

## Installation and Setup

After installing jugaad-data, the `jdata` command becomes available:

```bash
pip install jugaad-data
jdata --help
```

## Commands Overview

### Main Commands

- `jdata bhavcopy` - Download NSE bhavcopy files
- `jdata stock` - Download historical stock data
- `jdata index` - Download historical index data  
- `jdata derivatives` - Download F&O derivatives data

## Command Reference

### `jdata bhavcopy`

Download NSE bhavcopy files for specified dates.

```bash
jdata bhavcopy --help
```

**Usage:**
```bash
jdata bhavcopy -d /path/to/directory [OPTIONS]
```

**Options:**
- `-d, --dest` (required): Destination directory path
- `-f, --from`: From date (YYYY-MM-DD format)
- `-t, --to`: To date (YYYY-MM-DD format)  
- `--fo/--no-fo`: Download F&O bhavcopy (default: False)
- `--idx/--no-idx`: Download Index bhavcopy (default: False)
- `--full/--no-full`: Download full bhavcopy (default: False)

**Examples:**

```bash
# Download today's bhavcopy
jdata bhavcopy -d /path/to/dir

# Download bhavcopy for specific date
jdata bhavcopy -d /path/to/dir -f 2020-01-01

# Download bhavcopy for date range
jdata bhavcopy -d /path/to/dir -f 2020-01-01 -t 2020-02-01

# Download F&O bhavcopy
jdata bhavcopy -d /path/to/dir -f 2020-01-01 --fo

# Download index bhavcopy
jdata bhavcopy -d /path/to/dir -f 2020-01-01 --idx

# Download full bhavcopy (detailed data)
jdata bhavcopy -d /path/to/dir -f 2020-01-01 --full
```

### `jdata stock`

Download historical stock data and save to CSV.

```bash
jdata stock --help
```

**Usage:**
```bash
jdata stock -s SYMBOL -f FROM_DATE -t TO_DATE [OPTIONS]
```

**Options:**
- `-s, --symbol` (required): Stock symbol (e.g., SBIN, RELIANCE)
- `-f, --from` (required): From date (YYYY-MM-DD)
- `-t, --to` (required): To date (YYYY-MM-DD)
- `-S, --series`: Series type (default: EQ)
- `-o, --output`: Output file path (auto-generated if not specified)

**Examples:**

```bash
# Download SBIN data for January 2020
jdata stock -s SBIN -f 2020-01-01 -t 2020-01-31

# Specify output file
jdata stock -s SBIN -f 2020-01-01 -t 2020-01-31 -o SBIN-Jan2020.csv

# Download with different series
jdata stock -s SBIN -f 2020-01-01 -t 2020-01-31 -S BE

# Download full year data
jdata stock -s RELIANCE -f 2020-01-01 -t 2020-12-31 -o RELIANCE-2020.csv
```

**Output:**
```
SBIN  [####################################]  100%

Saved file to : SBIN-Jan2020.csv
```

### `jdata index`

Download historical index data and save to CSV.

```bash
jdata index --help
```

**Usage:**
```bash
jdata index -s "INDEX_NAME" -f FROM_DATE -t TO_DATE [OPTIONS]
```

**Options:**
- `-s, --symbol` (required): Index name (e.g., "NIFTY 50", "NIFTY BANK")
- `-f, --from` (required): From date (YYYY-MM-DD)
- `-t, --to` (required): To date (YYYY-MM-DD)
- `-o, --output`: Output file path

**Examples:**

```bash
# Download NIFTY 50 data
jdata index -s "NIFTY 50" -f 2020-01-01 -t 2020-01-31

# Download NIFTY BANK data with custom output
jdata index -s "NIFTY BANK" -f 2020-01-01 -t 2020-12-31 -o nifty-bank-2020.csv

# Download sectoral indices
jdata index -s "NIFTY IT" -f 2020-01-01 -t 2020-01-31
jdata index -s "NIFTY PHARMA" -f 2020-01-01 -t 2020-01-31
```

### `jdata derivatives`

Download historical derivatives (F&O) data.

```bash
jdata derivatives --help
```

**Usage:**
```bash
jdata derivatives -s SYMBOL -f FROM_DATE -t TO_DATE -e EXPIRY_DATE -i INSTRUMENT [OPTIONS]
```

**Options:**
- `-s, --symbol` (required): Stock/Index symbol
- `-f, --from` (required): From date (YYYY-MM-DD)
- `-t, --to` (required): To date (YYYY-MM-DD)
- `-e, --expiry` (required): Expiry date (YYYY-MM-DD)
- `-i, --instru` (required): Instrument type
  - `FUTSTK` - Stock futures
  - `FUTIDX` - Index futures
  - `OPTSTK` - Stock options
  - `OPTIDX` - Index options
- `-p, --price`: Strike price (required for options)
- `--ce/--pe`: Call/Put option type (required for options)
- `-o, --output`: Output file path

**Examples:**

**Stock Futures:**
```bash
jdata derivatives -s SBIN -f 2020-01-01 -t 2020-01-30 -e 2020-01-30 -i FUTSTK -o sbin_futures.csv
```

**Index Futures:**
```bash
jdata derivatives -s NIFTY -f 2020-01-01 -t 2020-01-30 -e 2020-01-30 -i FUTIDX -o nifty_futures.csv
```

**Stock Options (Call):**
```bash
jdata derivatives -s SBIN -f 2020-01-01 -t 2020-01-30 -e 2020-01-30 -i OPTSTK -p 330 --ce -o sbin_call.csv
```

**Stock Options (Put):**
```bash
jdata derivatives -s SBIN -f 2020-01-01 -t 2020-01-30 -e 2020-01-30 -i OPTSTK -p 330 --pe -o sbin_put.csv
```

**Index Options (Call):**
```bash
jdata derivatives -s NIFTY -f 2020-01-01 -t 2020-01-30 -e 2020-01-23 -i OPTIDX -p 11000 --ce -o nifty_call.csv
```

**Index Options (Put):**
```bash
jdata derivatives -s NIFTY -f 2020-01-01 -t 2020-01-30 -e 2020-01-23 -i OPTIDX -p 11000 --pe -o nifty_put.csv
```

## Progress Indicators

The CLI includes progress bars for long-running operations:

```
SBIN  [####################################]  100%
Downloading Bhavcopies  [##########----------]  50%
```

## Error Handling

### Common Errors and Solutions

**Timeout Errors:**
```
Error: Timeout while downloading, This may be due to-
1. Bad internet connection
2. Today is holiday or file is not ready yet
```

**Solution:**
- Check internet connection
- Verify the date is a trading day
- Try downloading data for a different date

**Invalid Dates:**
- Ensure dates are in YYYY-MM-DD format
- Check that from_date <= to_date
- Verify dates are valid trading days

**Missing Files:**
```
Failed to download for below dates, these might be holidays, please check -
2020-01-26
2020-02-21
```

**Solution:**
- These are typically holidays or weekends
- Use the holidays module to check: `from jugaad_data.holidays import holidays`

## Batch Operations

### Download Multiple Stocks

Create a shell script for batch downloads:

**Windows (batch file):**
```batch
@echo off
set stocks=SBIN HDFC ICICIBANK RELIANCE TCS INFY
set from_date=2020-01-01
set to_date=2020-12-31

for %%s in (%stocks%) do (
    echo Downloading %%s...
    jdata stock -s %%s -f %from_date% -t %to_date% -o %%s-2020.csv
)
```

**Linux/Mac (bash script):**
```bash
#!/bin/bash
stocks=("SBIN" "HDFC" "ICICIBANK" "RELIANCE" "TCS" "INFY")
from_date="2020-01-01"
to_date="2020-12-31"

for stock in "${stocks[@]}"; do
    echo "Downloading $stock..."
    jdata stock -s "$stock" -f "$from_date" -t "$to_date" -o "${stock}-2020.csv"
done
```

### Download Full Year Bhavcopies

```bash
# Download all bhavcopy types for 2020
jdata bhavcopy -d ./bhavcopy_2020/ -f 2020-01-01 -t 2020-12-31
jdata bhavcopy -d ./bhavcopy_2020/ -f 2020-01-01 -t 2020-12-31 --fo
jdata bhavcopy -d ./bhavcopy_2020/ -f 2020-01-01 -t 2020-12-31 --idx
```

## Output File Formats

### Stock Data CSV

```csv
DATE,SERIES,OPEN,HIGH,LOW,PREV. CLOSE,LTP,CLOSE,VWAP,52W H,52W L,VOLUME,VALUE,NO OF TRADES,SYMBOL
2020-01-01,EQ,305.0,308.9,304.05,304.8,307.4,307.7,306.98,373.8,149.45,15388597,4722550986.85,207780,SBIN
```

### Index Data CSV

```csv
INDEX_NAME,HistoricalDate,OPEN,HIGH,LOW,CLOSE
NIFTY 50,01-Jan-2020,12282.7,12293.1,12254.0,12282.2
```

### Derivatives Data CSV

**Futures:**
```csv
DATE,EXPIRY,OPEN,HIGH,LOW,CLOSE,LTP,SETTLE PRICE,TOTAL TRADED QUANTITY,MARKET LOT,PREMIUM VALUE,OPEN INTEREST,CHANGE IN OI,SYMBOL
```

**Options:**
```csv
DATE,EXPIRY,OPTION TYPE,STRIKE PRICE,OPEN,HIGH,LOW,CLOSE,LTP,SETTLE PRICE,TOTAL TRADED QUANTITY,MARKET LOT,PREMIUM VALUE,OPEN INTEREST,CHANGE IN OI,SYMBOL
```

## Integration with Other Tools

### Use with Excel/Google Sheets

CSV files can be directly imported into spreadsheet applications for analysis.

### Use with Python

```python
import pandas as pd

# Read CLI-generated CSV
df = pd.read_csv('SBIN-2020.csv')
print(df.head())
```

### Use with R

```r
# Read CSV in R
data <- read.csv('SBIN-2020.csv')
head(data)
```

## Performance Tips

1. **Use Date Ranges Wisely**: Large date ranges are automatically split into monthly chunks
2. **Specify Output Files**: Avoid auto-generated filenames for better organization
3. **Batch Similar Operations**: Download multiple instruments of the same type together
4. **Check Holidays**: Use holiday calendar to avoid unnecessary requests
5. **Use Progress Bars**: Enable progress indicators for long operations

## Troubleshooting

### CLI Not Found

If `jdata` command is not recognized:

```bash
# Check if jugaad-data is installed
pip list | grep jugaad-data

# Reinstall if necessary
pip install --upgrade jugaad-data

# Use full path if needed
python -m jugaad_data.cli --help
```

### Permission Errors

Ensure write permissions to destination directory:

```bash
# Linux/Mac
chmod 755 /path/to/directory

# Windows - Run as administrator if needed
```

### Network Issues

For network-related errors:
- Check internet connectivity
- Try with smaller date ranges
- Use retry logic in batch scripts