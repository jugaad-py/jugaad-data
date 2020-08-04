import os
import json
import csv
from datetime import date, datetime, timedelta
from pprint import pprint
from pyfakefs.fake_filesystem_unittest import TestCase
import numpy as np
import pandas as pd
from appdirs import user_cache_dir
from jugaad_data import nse

h = nse.NSEHistory()


def get_reliance():
    symbol = "RELIANCE"
    from_date = date(2019,1,1)
    to_date = date(2019,1,31)
    sym_count = 2
    series = "EQ"
    params = {
            'symbol': symbol,
            'from': from_date.strftime('%d-%m-%Y'),
            'to': to_date.strftime('%d-%m-%Y'),
            'series': '["{}"]'.format(series),
    }
    return h._get("stock_history", params)

def test__get():
    d = get_reliance()
    j = json.loads(d.text)
    # assert d.request.url == 0
    assert 'data' in j
    assert j['data'][0]["CH_TIMESTAMP"] == "2019-01-31"
    assert j['data'][-1]["CH_TIMESTAMP"] == "2019-01-01"
    

def test__get_http_bin():
    h = nse.NSEHistory()
    h.base_url = "https://httpbin.org"
    h.path_map['bin'] = '/get'
    
    params = {"p1":'1' , "p2": "a"}
    r = h._get("bin", params)
    _params = json.loads(r.text)['args']
    assert params == _params

class TestNSECache(TestCase):
    def setUp(self):
        """
        FakeFS creates a fake file systems and in process looses the CA Certs
        Which fails the test while running stocks
        To fix that CA certificates will be read and then placed back
        """
        import certifi
        self.path = certifi.where()
        with open(self.path) as fp:
            self.certs = fp.read()
        self.setUpPyfakefs()        
        ## Restoring the CA certs
        self.fs.create_file(self.path)
        with open(self.path, "w") as fp:
            fp.write(self.certs)

    def test__stock(self):
        d = h._stock("SBIN", date(2001,1,1), date(2001,1,31))
        assert d[0]["CH_TIMESTAMP"] == "2001-01-31"
        assert d[-1]["CH_TIMESTAMP"] == "2001-01-01"
        # Check if there's no data
        d = h._stock("SBIN", date(2020,7,4), date(2020,7,5))
        assert len(d) == 0
        # Check future date
        from_date = datetime.now().date() + timedelta(days=1)
        to_date = from_date + timedelta(days=10)
        d = h._stock("SBIN", from_date, to_date)
        assert len(d) == 0

    def test_stock_raw(self):
        from_date = date(2001,1,15)
        to_date = date(2002,1,15)
        d = nse.stock_raw("SBIN", from_date, to_date)
        assert len(d) > 240
        assert len(d) < 250
        all_dates = [datetime.strptime(k["CH_TIMESTAMP"], "%Y-%m-%d").date() for k in d]
        assert to_date in all_dates
        assert from_date in all_dates
        assert d[-1]["CH_TIMESTAMP"] == str(from_date)
        assert d[0]["CH_TIMESTAMP"] == str(to_date)
        app_name = nse.APP_NAME + '-stock'
        files = os.listdir(user_cache_dir(app_name, app_name))
        assert len(files) == 13
    
    def test_stock_csv(self):
        from_date = date(2001,1,15)
        to_date = date(2002,1,15)
        raw = nse.stock_raw("SBIN", from_date, to_date)
        output = nse.stock_csv("SBIN", from_date, to_date)
        with open(output) as fp:
            text = fp.read()
            rows = [x.split(',') for x in text.split('\n')]
        headers = [   "DATE", "SERIES",
                        "OPEN", "HIGH",
                        "LOW", "PREV. CLOSE",
                        "LTP", "CLOSE",
                        "VWAP", "52W H", "52W L",
                        "VOLUME", "VALUE", "NO OF TRADES", "SYMBOL"]
        assert headers == rows[0]
        assert raw[0]['CH_TIMESTAMP'] == rows[1][0]
        assert raw[0]['CH_OPENING_PRICE'] == int(rows[1][2])

    def test_stock_df(self):
        from_date = date(2001,1,15)
        to_date = date(2002,1,15)
        raw = nse.stock_raw("SBIN", from_date, to_date)
        df = nse.stock_df("SBIN", from_date, to_date)
        
        assert len(raw) == len(df)
        assert df['DATE'].iloc[0] == np.datetime64("2002-01-15")
        assert df['DATE'].iloc[-1] == np.datetime64("2001-01-15")
        assert df['OPEN'].iloc[0] == 220

        
