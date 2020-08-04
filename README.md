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
| NSE      | Stocks F&O | Planned    |
| NSE      | Index      | Planned    |
| NSE      | Index F&O  | Planned    |

# Installation

`pip install git+https://github.com/jugaad-py/jugaad-data.git`

# Getting started

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


# Documentation

Visit https://marketsetup.in/documentation/jugaad-data/ for detailed documentation.

