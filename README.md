# Documentation

https://marketsetup.in/documentation/jugaad-data/

# Introduction

`jugaad-data` helps you download historical stock data.

[![Build Status](https://travis-ci.org/jugaad-py/jugaad-data.svg?branch=master)](https://travis-ci.org/jugaad-py/jugaad-data)


# Features

* Supports [new NSE website](https://www.nseindia.com/), (All libraries based on old NSE website might stop working)
* Powerful CLI (Command line interface), Even non-coders can use it easily
* Built-in caching mechanism to play nice with NSE. Avoid making un-necessary requests to NSE's website and getting
* blocked
* Optional `pandas` support, You don't have to if you don't want to

**Road map**

| Exchange | Segment    | Supported? |
|----------|------------|------------|
| NSE      | Stocks     | Yes        |
| NSE      | Stocks F&O | Yes        |
| NSE      | Index      | Yes    |
| NSE      | Index F&O  | Yes        |

# Installation

`pip install git+https://github.com/jugaad-py/jugaad-data.git`

# Getting started

## Download historical stock data

```
$ jdata stock --help

Usage: jdata stock [OPTIONS]

  Download historical stock data

  $jdata stock --symbol STOCK1 -f yyyy-mm-dd -t yyyy-mm-dd --o file_name.csv

Options:
  -s, --symbol TEXT  [required]
  -f, --from TEXT    [required]
  -t, --to TEXT      [required]
  -S, --series TEXT  [default: EQ]
  -o, --output TEXT
  --help             Show this message and exit.
```

```
$ jdata stock -s SBIN -f 2020-01-01 -t 2020-01-31 -o SBIN-Jan.csv
SBIN  [####################################]  100%

Saved file to : SBIN-Jan.csv
```

## Download historical derivatives (F&O) data

```
$ jdata deriviatives --help
Usage: cli.py derivatives [OPTIONS]

  Sample usage-

  Download stock futures-

  jdata derivatives -s SBIN -f 2020-01-01 -t 2020-01-30 -e 2020-01-30 -i FUTSTK -o file_name.csv

  Download index futures-

  jdata derivatives -s NIFTY -f 2020-01-01 -t 2020-01-30 -e 2020-01-30 -i FUTIDX -o file_name.csv

  Download stock options-

  jdata derivatives -s SBIN -f 2020-01-01 -t 2020-01-30 -e 2020-01-30 -i OPTSTK -p 330 --ce -o file_name.csv

  Download index options-

  jdata derivatives -s NIFTY -f 2020-01-01 -t 2020-01-30 -e 2020-01-23 -i OPTIDX -p 11000 --pe -o file_name.csv

Options:
  -s, --symbol TEXT  Stock/Index symbol  [required]
  -f, --from TEXT    From date - yyyy-mm-dd  [required]
  -t, --to TEXT      To date - yyyy-mm-dd  [required]
  -e, --expiry TEXT  Expiry date - yyyy-mm-dd  [required]
  -i, --instru TEXT  FUTSTK - Stock futures, FUTIDX - Index Futures, OPTSTK -
                     Stock Options, OPTIDX - Index Options  [required]

  -p, --price TEXT   Strike price (Only for OPTSTK and OPTIDX)
  --ce / --pe        --ce for call and --pe for put (Only for OPTSTK and
                     OPTIDX)

  -o, --output TEXT  Full path of output file
  --help             Show this message and exit.
```


