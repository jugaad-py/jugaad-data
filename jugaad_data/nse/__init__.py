import os
import json
import itertools
import csv
from pprint import pprint
from urllib.parse import urljoin
from requests import Session
from bs4 import BeautifulSoup
import click
try:
    import pandas as pd
    import numpy as np
except:
    pd = None

from jugaad_data import util as ut


APP_NAME = "nsehistory"
class NSEHistory:
    headers = {
        "Host": "www.nseindia.com",
        "Referer": "https://www.nseindia.com/get-quotes/equity?symbol=SBIN",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        }
    path_map = {
        "stock_history": "/api/historical/cm/equity",
    }
    base_url = "https://www.nseindia.com"
    cache_dir = ".cache"
    workers = 2
    use_threads = True
    show_progress = False

    def __init__(self):
        self.s = Session()
        self.s.headers.update(self.headers)
        self.ssl_verify = True

    def _get(self, path_name, params):
        path = self.path_map[path_name]
        url = urljoin(self.base_url, path)
        return self.s.get(url, params=params, verify=self.ssl_verify)
    
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

    def stock_raw(self, symbol, from_date, to_date, series="EQ"):
        date_ranges = ut.break_dates(from_date, to_date)
        params = [(symbol, x[0], x[1], series) for x in reversed(date_ranges)]
        chunks = ut.pool(self._stock, params)
            
        return list(itertools.chain.from_iterable(chunks))

    

h = NSEHistory()
stock_raw = h.stock_raw
select_headers = [  "CH_TIMESTAMP", "CH_SERIES", 
                    "CH_OPENING_PRICE", "CH_TRADE_HIGH_PRICE",
                    "CH_TRADE_LOW_PRICE", "CH_PREVIOUS_CLS_PRICE",
                    "CH_LAST_TRADED_PRICE", "CH_CLOSING_PRICE",
                    "VWAP", "CH_52WEEK_HIGH_PRICE", "CH_52WEEK_LOW_PRICE",
                    "CH_TOT_TRADED_QTY", "CH_TOT_TRADED_VAL", "CH_TOTAL_TRADES",
                    "CH_SYMBOL"]
final_headers = [   "DATE", "SERIES",
                    "OPEN", "HIGH",
                    "LOW", "PREV. CLOSE",
                    "LTP", "CLOSE",
                    "VWAP", "52W H", "52W L",
                    "VOLUME", "VALUE", "NO OF TRADES", "SYMBOL"]
def header_to_dtype(header):
    mapping = {"CH_TIMESTMP": ut.np_date}
    
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
            fp.write(",".join(final_headers) + '\n')
            for row in raw:
                row_select = [str(row[x]) for x in select_headers]
                line = ",".join(row_select) + '\n'
                fp.write(line) 
    return output

def stock_df(symbol, from_date, to_date, series="EQ"):
    if not pd:
        raise ModuleNotFoundError("Please install pandas using \n pip install pandas")
    raw = stock_raw(symbol, from_date, to_date, series)
    df = pd.DataFrame(raw)[select_headers]
    df.columns = final_headers
    dtypes = [  ut.np_date,  str,
                ut.np_float, ut.np_float,
                ut.np_float, ut.np_float,
                ut.np_float, ut.np_float,
                ut.np_float, ut.np_float, ut.np_float,
                ut.np_int, ut.np_float, ut.np_int, str]
    for i, h in enumerate(final_headers):
        df[h] = df[h].apply(dtypes[i])
    return df

