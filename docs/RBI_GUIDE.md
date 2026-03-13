# Jugaad Data - RBI Economic Data Guide

Guide to fetching economic and financial data from Reserve Bank of India website using `jugaad-data`.

## Overview

The RBI module allows you to fetch current economic rates and indices from the Reserve Bank of India website. This includes policy rates, deposit rates, T-Bill rates, and government securities rates.

## Initialization

```python
from jugaad_data.rbi import RBI

r = RBI()
```

## Available Data

### Current Rates

Fetch all available rates and indices from RBI:

```python
from jugaad_data.rbi import RBI

r = RBI()
rates = r.current_rates()

# Returns a dictionary with all rates
print(rates)
```

### Monetary Policy Rates

**Policy Repo Rate**
- The rate at which RBI lends to banks
- Used as benchmark for other interest rates
- Directly influences lending rates

```python
rates = r.current_rates()
print(rates['Policy Repo Rate'])  # e.g., "4.00%"
```

**Reverse Repo Rate**
- Rate at which RBI borrows from banks
- Lower than policy repo rate
- Creates corridor for short-term rates

```python
print(rates['Reverse Repo Rate'])  # e.g., "3.35%"
```

**Marginal Standing Facility Rate (MSF)**
- Rate for emergency overnight loans to banks
- Highest in the corridor
- Default rate when other sources unavailable

```python
print(rates['Marginal Standing Facility Rate'])  # e.g., "4.25%"
```

**Bank Rate**
- Historic rate, now aligned with MSF
- Used for fixed rate operations

```python
print(rates['Bank Rate'])  # e.g., "4.25%"
```

### Reserve Requirements

**Cash Reserve Ratio (CRR)**
- Percentage of deposits banks must keep with RBI
- Used as monetary policy tool
- Reduces money supply when increased

```python
print(rates['CRR'])  # e.g., "3.50%"
```

**Statutory Liquidity Ratio (SLR)**
- Percentage of deposits banks must invest in securities
- Ensures bank liquidity
- Typically higher than CRR

```python
print(rates['SLR'])  # e.g., "18.00%"
```

### Bank Lending Rates

**Base Rate**
- Minimum lending rate banks can charge
- All loans must be above base rate + spread
- Varies by bank and loan type

```python
print(rates['Base Rate'])  # e.g., "7.40% - 8.80%"
```

**Minimum Marginal Cost of Funds Based Lending Rate (MCLR)**
- Minimum lending rate (since 2016)
- Varies by tenor (overnight to 1 year)
- Banks add spread for actual lending rate

```python
print(rates['MCLR (Overnight)'])      # e.g., "6.55% - 7.05%"
# Available for different tenors
```

### Deposit Rates

**Savings Deposit Rate**
- Rate banks pay on savings accounts
- Range shown by different banks
- Influenced by policy rates

```python
print(rates['Savings Deposit Rate'])  # e.g., "2.70% - 3.00%"
```

**Term Deposit Rate (>1 Year)**
- Rate on fixed deposits > 1 year
- Higher than shorter-term rates
- Varies by bank and amount

```python
print(rates['Term Deposit Rate > 1 Year'])  # e.g., "4.90% - 5.50%"
```

### Money Market Rates

**Call Rates**
- Overnight lending rates between banks
- Very short-term, unsecured
- Highly volatile
- Influenced by RBI's corridor

```python
print(rates['Call Rates'])  # e.g., "1.90% - 3.50%"
```

### Government Securities & T-Bills

Government securities (G-Secs) are issued by Government of India:

```python
rates = r.current_rates()

# Specific maturity examples
print(rates['5.85% GS 2030'])       # e.g., "6.0591%"
print(rates['5.77% GS 2030'])       # e.g., "6.2211%"
print(rates['5.63% GS 2026'])       # e.g., "5.6058%"
print(rates['5.15% GS 2025'])       # e.g., "5.4270%"
print(rates['3.96% GS 2022'])       # e.g., "4.1165%"
```

**Treasury Bills (T-Bills)**
- Short-term government debt
- Issued for 91, 182, and 364 days
- Zero-coupon instruments (discounted)

```python
print(rates['91 day T-bills'])      # e.g., "3.3199%"
print(rates['182 day T-bills'])     # e.g., "3.4507%"
print(rates['364 day T-bills'])     # e.g., "3.7200%"
```

### Equity Indices

Current values of major indices:

```python
print(rates['S&P BSE Sensex'])      # e.g., "49765.94"
print(rates['Nifty 50'])            # e.g., "14894.90"
```

## Complete Example

```python
from jugaad_data.rbi import RBI

r = RBI()
rates = r.current_rates()

# Display all monetary policy rates
print("=== MONETARY POLICY RATES ===")
print(f"Policy Repo Rate: {rates['Policy Repo Rate']}")
print(f"Reverse Repo Rate: {rates['Reverse Repo Rate']}")
print(f"MSF Rate: {rates['Marginal Standing Facility Rate']}")
print(f"Bank Rate: {rates['Bank Rate']}")

# Display reserve requirements
print("\n=== RESERVE REQUIREMENTS ===")
print(f"CRR: {rates['CRR']}")
print(f"SLR: {rates['SLR']}")

# Display lending rates
print("\n=== LENDING RATES ===")
print(f"Base Rate: {rates['Base Rate']}")
print(f"MCLR (Overnight): {rates['MCLR (Overnight)']}")

# Display deposit rates
print("\n=== DEPOSIT RATES ===")
print(f"Savings Deposit: {rates['Savings Deposit Rate']}")
print(f"Term Deposit (>1Y): {rates['Term Deposit Rate > 1 Year']}")

# Display money market rates
print("\n=== MONEY MARKET RATES ===")
print(f"Call Rates: {rates['Call Rates']}")
print(f"T-Bill (91 days): {rates['91 day T-bills']}")
print(f"T-Bill (182 days): {rates['182 day T-bills']}")
print(f"T-Bill (364 days): {rates['364 day T-bills']}")

# Display equity benchmarks
print("\n=== EQUITY BENCHMARKS ===")
print(f"BSE Sensex: {rates['S&P BSE Sensex']}")
print(f"Nifty 50: {rates['Nifty 50']}")
```

## Data Types and Parsing

The returned values are strings. Parse them as needed:

```python
from jugaad_data.rbi import RBI

r = RBI()
rates = r.current_rates()

# Extract numeric value from percentage string
def parse_percentage(rate_str):
    """Convert '4.00%' to float 4.00"""
    return float(rate_str.replace('%', ''))

# Single value rates
repo_rate = parse_percentage(rates['Policy Repo Rate'])
print(f"Repo Rate: {repo_rate}")

# Range of rates
def parse_range(rate_str):
    """Convert '7.40% - 8.80%' to tuple (7.40, 8.80)"""
    parts = rate_str.split(' - ')
    return (
        float(parts[0].replace('%', '')),
        float(parts[1].replace('%', ''))
    )

base_rate = parse_range(rates['Base Rate'])
print(f"Base Rate Range: {base_rate}")
print(f"Base Rate Min: {base_rate[0]}, Max: {base_rate[1]}")
```

## Use Cases

### Calculate Bank Lending Rate

```python
from jugaad_data.rbi import RBI

def parse_percentage(s):
    return float(s.replace('%', ''))

def parse_range(s):
    parts = s.split(' - ')
    return (float(parts[0].replace('%', '')), float(parts[1].replace('%', '')))

r = RBI()
rates = r.current_rates()

# Bank's lending rate = Base Rate + Spread
base_rate_min, base_rate_max = parse_range(rates['Base Rate'])
risk_spread = 1.5  # 1.5% credit spread

lending_rate_min = base_rate_min + risk_spread
lending_rate_max = base_rate_max + risk_spread

print(f"Bank Lending Rate Range: {lending_rate_min}% - {lending_rate_max}%")
```

### Analyze Yield Curve

```python
from jugaad_data.rbi import RBI
import re

r = RBI()
rates = r.current_rates()

# Extract G-Sec yields by maturity
gsecs = {}
for key, value in rates.items():
    if 'GS' in key and '%' in value:
        gsecs[key] = float(value.replace('%', ''))

print("Government Securities Yield Curve:")
for security, yield_pct in sorted(gsecs.items()):
    print(f"{security}: {yield_pct}%")
```

### Monitor Monetary Policy

```python
from jugaad_data.rbi import RBI

r = RBI()
rates = r.current_rates()

def parse_percentage(s):
    return float(s.replace('%', ''))

repo = parse_percentage(rates['Policy Repo Rate'])
reverse_repo = parse_percentage(rates['Reverse Repo Rate'])
msf = parse_percentage(rates['Marginal Standing Facility Rate'])

corridor_width = msf - reverse_repo
print(f"RBI Rate Corridor:")
print(f"  Floor (Reverse Repo): {reverse_repo}%")
print(f"  Repo Rate: {repo}%")
print(f"  Ceiling (MSF): {msf}%")
print(f"  Corridor Width: {corridor_width}%")

# Policy stance
if repo > 5:
    print("Monetary Stance: Tight/Restrictive")
elif repo < 4:
    print("Monetary Stance: Loose/Accommodative")
else:
    print("Monetary Stance: Neutral")
```

### Calculate Real Interest Rate

```python
from jugaad_data.rbi import RBI

r = RBI()
rates = r.current_rates()

def parse_percentage(s):
    return float(s.replace('%', ''))

# Note: This is simplified. Real inflation rate would come from other sources
nominal_rate = parse_percentage(rates['Policy Repo Rate'])
inflation_rate = 5.0  # Example: 5% inflation (get from actual sources)

real_rate = nominal_rate - inflation_rate
print(f"Nominal Rate: {nominal_rate}%")
print(f"Inflation Rate: {inflation_rate}%")
print(f"Real Rate: {real_rate}%")

if real_rate > 0:
    print("Economy: Tight monetary conditions")
else:
    print("Economy: Loose monetary conditions")
```

## Limitations

1. **Data Freshness**: Rates are updated when RBI updates them, typically:
   - Monetary policy rates: Changed during RBI policy meetings (quarterly)
   - T-Bills: Updated daily after auctions
   - G-Secs: Updated based on secondary market trading

2. **No Historical Data**: Current implementation only provides latest rates
   - No historical tracking available
   - For historical analysis, maintain your own database

3. **Limited Derivatives**: No options, futures, or swap rates available
   - Check NSE/MCX for derivatives data

4. **Corporate Bonds**: Not included in current implementation
   - Available separately from credit rating agencies

## Related Data Sources

- **NSE**: Stock and derivatives data (use NSELive)
- **BSE**: Equity and derivatives data
- **NSE F&O**: Interest rate futures and options
- **Debt Markets**: Corporate bonds through credit agencies

## Future Enhancements

In pipeline:
- Historical rate tracking
- Additional economic indicators
- Corporate action data
- Financial results

## References

- RBI Website: https://www.rbi.org.in
- Monetary Policy: https://www.rbi.org.in/web/rbi/monetary-policy
- Market Data: https://www.rbi.org.in/web/rbi/financial-markets

## Example: Create Rate Monitor

```python
from jugaad_data.rbi import RBI
from datetime import datetime

class RBIRateMonitor:
    def __init__(self):
        self.rbi = RBI()
    
    def get_rates(self):
        return self.rbi.current_rates()
    
    def print_summary(self):
        rates = self.get_rates()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n{'='*50}")
        print(f"RBI RATES - {timestamp}")
        print(f"{'='*50}")
        print(f"Policy Repo Rate: {rates['Policy Repo Rate']}")
        print(f"Reverse Repo Rate: {rates['Reverse Repo Rate']}")
        print(f"CRR: {rates['CRR']}")
        print(f"SLR: {rates['SLR']}")
        print(f"Call Rates: {rates['Call Rates']}")
        print(f"Sensex: {rates['S&P BSE Sensex']}")
        print(f"Nifty 50: {rates['Nifty 50']}")
        print(f"{'='*50}\n")

# Usage
monitor = RBIRateMonitor()
monitor.print_summary()
```
