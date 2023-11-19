"""
    Implements functionality to download historical stock, index and
    derivatives data from NSE and
    NSEIndices website
"""
import os
import json
import itertools
import csv
from pprint import pprint
from urllib.parse import urljoin
from requests import Session
#from bs4 import BeautifulSoup
import click
try:
    import pandas as pd
    import numpy as np
except:
    pd = None

from jugaad_data import util as ut
from .archives import (bhavcopy_raw, bhavcopy_save, 
                        full_bhavcopy_raw, full_bhavcopy_save,
                        bhavcopy_fo_raw, bhavcopy_fo_save,
                        bhavcopy_index_raw, bhavcopy_index_save, expiry_dates)

APP_NAME = "nsehistory"
class NSEHistory:
    def __init__(self):
        
        self.headers = {
            "Host": "www.nseindia.com",
            "Referer": "https://www.nseindia.com/get-quotes/equity?symbol=SBIN",
            "X-Requested-With": "XMLHttpRequest",
            "pragma": "no-cache",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            }
        self.path_map = {
            "stock_history": "/api/historical/cm/equity",
            "derivatives": "/api/historical/fo/derivatives",
            "equity_quote_page": "/get-quotes/equity",
        }
        self.base_url = "https://www.nseindia.com"
        self.cache_dir = ".cache"
        self.workers = 2
        self.use_threads = True
        self.show_progress = False

        self.s = Session()
        self.s.headers.update(self.headers)
        self.ssl_verify = True

    def _get(self, path_name, params):
        if "nseappid" not in self.s.cookies:
            path = self.path_map["equity_quote_page"]
            url = urljoin(self.base_url, path)
            self.s.get(url, verify=self.ssl_verify)
        path = self.path_map[path_name]
        url = urljoin(self.base_url, path)
        self.r = self.s.get(url, params=params, verify=self.ssl_verify)
        return self.r
    
    @ut.cached(APP_NAME + '-stock')
    def _stock(self, symbol, from_date, to_date, series="EQ"):
        params = {
            'symbol': symbol,
            'from': from_date.strftime('%d-%m-%Y'),
            'to': to_date.strftime('%d-%m-%Y'),
            'series': '["{}"]'.format(series),
        }
        self.r = self._get("stock_history", params)
        j = self.r.json()
        return j['data']
    
    
    @ut.cached(APP_NAME + '-derivatives')
    def _derivatives(self, symbol, from_date, to_date, expiry_date, instrument_type, strike_price=None, option_type=None):
        valid_instrument_types = ["OPTIDX", "OPTSTK", "FUTIDX", "FUTSTK"]
        if instrument_type not in valid_instrument_types:
            raise Exception("Invalid instrument_type, should be one of {}".format(", ".join(valid_instrument_types)))

        params = {
            'symbol': symbol,
            'from': from_date.strftime('%d-%m-%Y'),
            'to': to_date.strftime('%d-%m-%Y'),
            'expiryDate': expiry_date.strftime('%d-%b-%Y').upper(),
            'instrumentType': instrument_type
            }
        if "OPT" in instrument_type:
            if not(strike_price and option_type):
                raise Exception("Missing argument for OPTIDX or OPTSTK, require both strike_price and option_type")
                
            params['strikePrice'] = "{:.2f}".format(strike_price)
            params['optionType'] = option_type
        
        self.r = self._get("derivatives", params)
        j = self.r.json()
        return j['data']
    
    def stock_raw(self, symbol, from_date, to_date, series="EQ"):
        date_ranges = ut.break_dates(from_date, to_date)
        params = [(symbol, x[0], x[1], series) for x in reversed(date_ranges)]
        chunks = ut.pool(self._stock, params, max_workers=self.workers)
            
        return list(itertools.chain.from_iterable(chunks))

    def derivatives_raw(self, symbol, from_date, to_date, expiry_date, instrument_type, strike_price, option_type):
        date_ranges = ut.break_dates(from_date, to_date)
        params = [(symbol, x[0], x[1], expiry_date, instrument_type, strike_price, option_type) for x in reversed(date_ranges)]
        chunks = ut.pool(self._derivatives, params, max_workers=self.workers)
        return list(itertools.chain.from_iterable(chunks))

       

h = NSEHistory()
stock_raw = h.stock_raw
derivatives_raw = h.derivatives_raw
stock_select_headers = [  "CH_TIMESTAMP", "CH_SERIES", 
                    "CH_OPENING_PRICE", "CH_TRADE_HIGH_PRICE",
                    "CH_TRADE_LOW_PRICE", "CH_PREVIOUS_CLS_PRICE",
                    "CH_LAST_TRADED_PRICE", "CH_CLOSING_PRICE",
                    "VWAP", "CH_52WEEK_HIGH_PRICE", "CH_52WEEK_LOW_PRICE",
                    "CH_TOT_TRADED_QTY", "CH_TOT_TRADED_VAL", "CH_TOTAL_TRADES",
                    "CH_SYMBOL"]
stock_final_headers = [   "DATE", "SERIES",
                    "OPEN", "HIGH",
                    "LOW", "PREV. CLOSE",
                    "LTP", "CLOSE",
                    "VWAP", "52W H", "52W L",
                    "VOLUME", "VALUE", "NO OF TRADES", "SYMBOL"]
stock_dtypes = [  ut.np_date,  str,
            ut.np_float, ut.np_float,
            ut.np_float, ut.np_float,
            ut.np_float, ut.np_float,
            ut.np_float, ut.np_float, ut.np_float,
            ut.np_int, ut.np_float, ut.np_int, str]
   
def stock_csv(symbol, from_date, to_date, series="EQ", output="", show_progress=True):
    if show_progress:
        h = NSEHistory()
        h.show_progress = show_progress
        date_ranges = ut.break_dates(from_date, to_date)
        params = [(symbol, x[0], x[1], series) for x in reversed(date_ranges)]
        with click.progressbar(params, label=symbol) as ps:
            chunks = []
            for p in ps:
                r = h.stock_raw(*p)
                chunks.append(r)
            raw = list(itertools.chain.from_iterable(chunks))
    else:
        raw = stock_raw(symbol, from_date, to_date, series)

    if not output:
        output = "{}-{}-{}-{}.csv".format(symbol, from_date, to_date, series)
    if raw:
        with open(output, 'w') as fp:
            fp.write(",".join(stock_final_headers) + '\n')
            for row in raw:
                row_select = [str(row[x]) for x in stock_select_headers]
                line = ",".join(row_select) + '\n'
                fp.write(line) 
    return output

def stock_df(symbol, from_date, to_date, series="EQ"):
    if not pd:
        raise ModuleNotFoundError("Please install pandas using \n pip install pandas")
    raw = stock_raw(symbol, from_date, to_date, series)
    df = pd.DataFrame(raw)[stock_select_headers]
    df.columns = stock_final_headers
    for i, h in enumerate(stock_final_headers):
        df[h] = df[h].apply(stock_dtypes[i])
    return df

futures_select_headers = [  "FH_TIMESTAMP", "FH_EXPIRY_DT", 
                    "FH_OPENING_PRICE", "FH_TRADE_HIGH_PRICE",
                    "FH_TRADE_LOW_PRICE", "FH_CLOSING_PRICE",
                    "FH_LAST_TRADED_PRICE", "FH_SETTLE_PRICE", "FH_TOT_TRADED_QTY", "FH_MARKET_LOT",
                    "FH_TOT_TRADED_VAL", "FH_OPEN_INT", "FH_CHANGE_IN_OI", 
                    "FH_SYMBOL"]
futures_final_headers = [   "DATE", "EXPIRY",
                    "OPEN", "HIGH",
                    "LOW", "CLOSE",
                    "LTP", "SETTLE PRICE", "TOTAL TRADED QUANTITY", "MARKET LOT",
                    "PREMIUM VALUE", "OPEN INTEREST", "CHANGE IN OI",
                     "SYMBOL"]


options_select_headers = [  "FH_TIMESTAMP", "FH_EXPIRY_DT", "FH_OPTION_TYPE", "FH_STRIKE_PRICE",
                    "FH_OPENING_PRICE", "FH_TRADE_HIGH_PRICE",
                    "FH_TRADE_LOW_PRICE", "FH_CLOSING_PRICE",
                    "FH_LAST_TRADED_PRICE", "FH_SETTLE_PRICE", "FH_TOT_TRADED_QTY", "FH_MARKET_LOT",
                    "FH_TOT_TRADED_VAL", "FH_OPEN_INT", "FH_CHANGE_IN_OI", 
                    "FH_SYMBOL"]
options_final_headers = [   "DATE", "EXPIRY", "OPTION TYPE", "STRIKE PRICE",
                    "OPEN", "HIGH",
                    "LOW", "CLOSE",
                    "LTP", "SETTLE PRICE", "TOTAL TRADED QUANTITY", "MARKET LOT",
                    "PREMIUM VALUE", "OPEN INTEREST", "CHANGE IN OI",
                     "SYMBOL"]

def derivatives_csv(symbol, from_date, to_date, expiry_date, instrument_type, strike_price=None, option_type=None, output="", show_progress=False):
    if show_progress:
        h = NSEHistory()
        h.show_progress = show_progress
        date_ranges = ut.break_dates(from_date, to_date)
        params = [(symbol, x[0], x[1], expiry_date, instrument_type, strike_price, option_type) for x in reversed(date_ranges)]
        with click.progressbar(params, label=symbol) as ps:
            chunks = []
            for p in ps:
                r = h.derivatives_raw(*p)
                chunks.append(r)
            raw = list(itertools.chain.from_iterable(chunks))
    else:
        raw = derivatives_raw(symbol, from_date, to_date, expiry_date, instrument_type, strike_price, option_type)
    if not output:
        output = "{}-{}-{}-{}.csv".format(symbol, from_date, to_date, series)
    if "FUT" in instrument_type:
        final_headers = futures_final_headers
        select_headers = futures_select_headers
    if "OPT" in instrument_type:
        final_headers = options_final_headers
        select_headers = options_select_headers
    if raw:
        with open(output, 'w') as fp:
            fp.write(",".join(final_headers) + '\n')
            for row in raw:
                row_select = [str(row[x]) for x in select_headers]
                line = ",".join(row_select) + '\n'
                fp.write(line) 
    return output

def derivatives_df(symbol, from_date, to_date, expiry_date, instrument_type, strike_price=None, option_type=None):
    if not pd:
        raise ModuleNotFoundError("Please install pandas using \n pip install pandas")
    raw = derivatives_raw(symbol, from_date, to_date, expiry_date, instrument_type, 
                            strike_price=strike_price, option_type=option_type)
    futures_dtype = [  ut.np_date, ut.np_date, 
                ut.np_float, ut.np_float,
                ut.np_float, ut.np_float,
                ut.np_float, ut.np_float,
                ut.np_int, ut.np_int,
                ut.np_float, ut.np_float, ut.np_float,
                str]
    
    options_dtype = [  ut.np_date, ut.np_date, str, ut.np_float,
                ut.np_float, ut.np_float,
                ut.np_float, ut.np_float,
                ut.np_float, ut.np_float,
                ut.np_int, ut.np_int,
                ut.np_float, ut.np_float, ut.np_float,
                str]

    if "FUT" in instrument_type:
        final_headers = futures_final_headers
        select_headers = futures_select_headers
        dtypes = futures_dtype
    if "OPT" in instrument_type:
        final_headers = options_final_headers
        select_headers = options_select_headers
        dtypes = options_dtype
    df = pd.DataFrame(raw)[select_headers]
    df.columns = final_headers
    for i, h in enumerate(final_headers):
        df[h] = df[h].apply(dtypes[i])
    return df

class NSEIndexHistory(NSEHistory):
    def __init__(self):
        super().__init__()
        self.headers = {
            "Host": "niftyindices.com",
            "Referer": "niftyindices.com",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "Origin": "https://niftyindices.com",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json; charset=UTF-8"
            }
        self.path_map = {
            "index_history": "/Backpage.aspx/getHistoricaldatatabletoString",
            "index_pe_history": "/Backpage.aspx/getpepbHistoricaldataDBtoString"
        }
        self.base_url = "https://niftyindices.com"
        self.s = Session()
        self.s.headers.update(self.headers)
        self.ssl_verify = True

    def _post_json(self, path_name, params):
        path = self.path_map[path_name]
        url = urljoin(self.base_url, path)
        self.r = self.s.post(url, json=params, verify=self.ssl_verify)
        return self.r
    
    @ut.cached(APP_NAME + '-index')
    def _index(self, symbol, from_date, to_date): 
        params = {'name': symbol,
                'startDate': from_date.strftime("%d-%b-%Y"),
                'endDate': to_date.strftime("%d-%b-%Y")
        }
        r = self._post_json("index_history", params=params)
        return json.loads(self.r.json()['d'])
    
    def index_raw(self, symbol, from_date, to_date):
        date_ranges = ut.break_dates(from_date, to_date)
        params = [(symbol, x[0], x[1]) for x in reversed(date_ranges)]
        chunks = ut.pool(self._index, params, max_workers=self.workers)
        return list(itertools.chain.from_iterable(chunks))
    
    @ut.cached(APP_NAME + '-index_pe')
    def _index_pe(self, symbol, from_date, to_date):
        params = {'name': symbol,
                'startDate': from_date.strftime("%d-%b-%Y"),
                'endDate': to_date.strftime("%d-%b-%Y")
        }
        r = self._post_json("index_pe_history", params=params)
        return json.loads(self.r.json()['d'])

    def index_pe_raw(self, symbol, from_date, to_date):
        date_ranges = ut.break_dates(from_date, to_date)
        params = [(symbol, x[0], x[1]) for x in reversed(date_ranges)]
        chunks = ut.pool(self._index_pe, params, max_workers=self.workers)
        return list(itertools.chain.from_iterable(chunks))


ih = NSEIndexHistory()
index_raw = ih.index_raw
index_pe_raw = ih.index_pe_raw

def index_csv(symbol, from_date, to_date, output="", show_progress=False):
    if show_progress:
        h = NSEIndexHistory()
        date_ranges = ut.break_dates(from_date, to_date)
        params = [(symbol, x[0], x[1]) for x in reversed(date_ranges)]
        with click.progressbar(params, label=symbol) as ps:
            chunks = []
            for p in ps:
                r = h._index(*p)
                chunks.append(r)
            raw = list(itertools.chain.from_iterable(chunks))
    else:
        raw = index_raw(symbol, from_date, to_date)
    
    if not output:
        output = "{}-{}-{}.csv".format(symbol, from_date, to_date)
    
    if raw:
        with open(output, 'w') as fp:
            fieldnames = ["INDEX_NAME", "HistoricalDate", "OPEN", "HIGH", "LOW", "CLOSE"]
            writer = csv.DictWriter(fp, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(raw)
    return output

def index_df(symbol, from_date, to_date):
    if not pd:
        raise ModuleNotFoundError("Please install pandas using \n pip install pandas")
    raw = index_raw(symbol, from_date, to_date)
    df = pd.DataFrame(raw)
    index_dtypes = {'OPEN': ut.np_float, 'HIGH': ut.np_float, 'LOW': ut.np_float, 'CLOSE': ut.np_float,
                    'Index Name': str, 'INDEX_NAME': str, 'HistoricalDate': ut.np_date}
    for col, dtype in index_dtypes.items():
        df[col] = df[col].apply(dtype)
    return df

def index_pe_df(symbol, from_date, to_date):
    if not pd:
        raise ModuleNotFoundError("Please install pandas using \n pip install pandas")
    raw = index_pe_raw(symbol, from_date, to_date)
    df = pd.DataFrame(raw)
    index_dtypes = {'pe': ut.np_float, 'pb': ut.np_float, 'divYield': ut.np_float,
                    'Index Name': str, 'DATE': ut.np_date}
    for col, dtype in index_dtypes.items():
        df[col] = df[col].apply(dtype)
    return df

