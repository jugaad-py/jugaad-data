# Jugaad Data Documentation

This directory contains comprehensive API reference documentation for the jugaad-data library.

## Documentation Structure

### Main Documentation
- **[index.md](index.md)** - Main documentation index and overview

### Module Documentation

#### NSE (National Stock Exchange)
- **[nse/index.md](nse/index.md)** - NSE module overview
- **[nse/archives.md](nse/archives.md)** - Historical archive downloads (bhavcopy, bulk deals)
- **[nse/history.md](nse/history.md)** - Time series data (stocks, indices, derivatives)
- **[nse/live.md](nse/live.md)** - Real-time market data and quotes

#### BSE (Bombay Stock Exchange)
- **[bse/index.md](bse/index.md)** - BSE module with corporate announcements

#### RBI (Reserve Bank of India)
- **[rbi/index.md](rbi/index.md)** - Economic data and interest rates

#### Core Utilities
- **[cli.md](cli.md)** - Command line interface documentation
- **[utilities.md](utilities.md)** - Helper functions and decorators
- **[holidays.md](holidays.md)** - Trading holiday calendar

## Quick Navigation

### By Use Case

**Historical Data:**
- [Stock Data](nse/history.md#stock-data-functions)
- [Index Data](nse/history.md#index-data-functions)
- [Derivatives Data](nse/history.md#derivatives-data-functions)
- [Archive Downloads](nse/archives.md)

**Live Data:**
- [Stock Quotes](nse/live.md#stock_quotesymbol)
- [Option Chains](nse/live.md#index_option_chainsymbolnifty)
- [Market Status](nse/live.md#market_status)

**Corporate Data:**
- [BSE Announcements](bse/index.md#corporate_announcements)
- [NSE Announcements](nse/live.md#corporate_announcements)

**Command Line:**
- [Stock Downloads](cli.md#jdata-stock)
- [Bhavcopy Downloads](cli.md#jdata-bhavcopy)
- [Derivatives Downloads](cli.md#jdata-derivatives)

### By Data Source

| Source | Module | Documentation |
|--------|--------|---------------|
| NSE Equity | nse.history | [History Docs](nse/history.md) |
| NSE Live | nse.live | [Live Docs](nse/live.md) |
| NSE Archives | nse.archives | [Archives Docs](nse/archives.md) |
| BSE | bse | [BSE Docs](bse/index.md) |
| RBI | rbi | [RBI Docs](rbi/index.md) |

## Documentation Features

### Code Examples
Every function and class includes practical code examples showing real usage patterns.

### Complete API Reference
- Full parameter descriptions
- Return value documentation
- Error handling examples
- Best practices

### Integration Examples
Examples showing how to combine different modules for comprehensive analysis.

### Command Line Reference
Complete CLI documentation with examples for all commands and options.

## Getting Started

1. **New Users**: Start with the [main index](index.md) for an overview
2. **API Users**: Browse module-specific documentation
3. **CLI Users**: Check the [CLI documentation](cli.md)
4. **Advanced Users**: Review [utilities](utilities.md) for optimization

## Contributing to Documentation

The documentation is written in Markdown and should be:
- **Clear and Concise**: Easy to understand examples
- **Complete**: Cover all parameters and return values
- **Practical**: Focus on real-world usage patterns
- **Up-to-date**: Reflect current API behavior

## Documentation Standards

- **Code Examples**: Include complete, runnable examples
- **Error Handling**: Show common error scenarios and solutions
- **Performance Notes**: Include caching and optimization tips
- **Integration**: Show how modules work together