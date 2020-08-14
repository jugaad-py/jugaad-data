import os
import json
import csv
from datetime import date, datetime, timedelta
from pprint import pprint

from pyfakefs.fake_filesystem_unittest import TestCase
import pytest
import numpy as np
import pandas as pd
from appdirs import user_cache_dir
from jugaad_data import nse
import click
import warnings
h = nse.NSEHistory()


def get_data(symbol, from_date, to_date, series):
    params = {
            'symbol': symbol,
            'from': from_date.strftime('%d-%m-%Y'),
            'to': to_date.strftime('%d-%m-%Y'),
            'series': '["{}"]'.format(series),
    }
    return h._get("stock_history", params)

def test__get():
    symbol = "RELIANCE"
    from_date = date(2019,1,1)
    to_date = date(2019,1,31)
    series = "EQ"
    d = get_data(symbol, from_date, to_date, series)
    j = json.loads(d.text)
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

def setup_test(self):
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



class TestNSECache(TestCase):
    def setUp(self):
        setup_test(self)
        """
        FakeFS creates a fake file systems and in process looses the CA Certs
        Which fails the test while running stocks
        To fix that CA certificates will be read and then placed back
        import certifi
        self.path = certifi.where()
        with open(self.path) as fp:
            self.certs = fp.read()
        self.setUpPyfakefs()        
        ## Restoring the CA certs
        self.fs.create_file(self.path)
        with open(self.path, "w") as fp:
            fp.write(self.certs)
        """
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
    
    """
    def test__stock_futures(self):
        from_date = date(2020, 7, 1)
        to_date = date(2020, 7, 30) 
        expiry_date = to_date
        j = h._stock_futures("SBIN", from_date, to_date, expiry_date)
        assert j[0]["FH_TIMESTAMP"] == "30-Jul-2020"
        assert j[-1]["FH_TIMESTAMP"] == "01-Jul-2020"
        for k, v in j[0].items():
            print("{}\t{}".format(k, v))
        print(len(j[0])) 
        assert False
     
    def test_stock_futures_raw(self):
        from_date = date(2020, 6, 1)
        to_date = date(2020, 7, 30) 
        expiry_date = to_date
        j = h.stock_futures_raw("SBIN", from_date, to_date, expiry_date)
        assert j[0]["FH_TIMESTAMP"] == "30-Jul-2020"
        assert j[-1]["FH_TIMESTAMP"] == "01-Jun-2020"
     
        app_name = nse.APP_NAME + '-stock-fut'
        files = os.listdir(user_cache_dir(app_name, app_name))
        assert len(files) == 2
    """

class TestDerivatives(TestCase):
    def setUp(self):
        setup_test(self)
    
    def test__stock_futures(self):
        """ Test stock futures at _derivative level ie without _pool"""
        from_date = date(2020, 6, 1)
        to_date = date(2020, 7, 30) 
        expiry_date = to_date
        instrument = "FUTSTK"
        j = h._derivatives("SBIN", from_date, to_date, expiry_date, instrument_type=instrument)
        assert j[0]['FH_TIMESTAMP'] == to_date.strftime("%d-%b-%Y")
        assert j[-1]['FH_TIMESTAMP'] == from_date.strftime("%d-%b-%Y")
        assert j[0]['FH_INSTRUMENT'] == instrument
        assert j[0]['FH_LAST_TRADED_PRICE'] == '185.95'
    
    def test__stock_options(self):
        from_date = date(2020, 7, 1)
        to_date = date(2020, 7, 30) 
        expiry_date = to_date
        instrument = "OPTSTK"
        strike_price = 190
        j = h._derivatives("SBIN", from_date, to_date, expiry_date, instrument_type=instrument,
                            strike_price=strike_price, option_type="CE")
        """ Warning - NSE's website not giving data for last two days, this function cannot be tested right now """
        # assert j[0]['FH_TIMESTAMP'] == to_date.strftime("%d-%b-%Y")
        assert j[-1]['FH_TIMESTAMP'] == from_date.strftime("%d-%b-%Y")
        assert j[0]['FH_INSTRUMENT'] == instrument
        assert j[0]['FH_LAST_TRADED_PRICE'] == '2.60'
        assert j[0]['FH_OPTION_TYPE'] == "CE"
        warnings.warn("Test is work in progress because NSE's new website does not provide correct Derivatives data")

    def test__index_futures(self):
        """ Test stock futures at _derivative level ie without _pool"""
        from_date = date(2020, 7, 1)
        to_date = date(2020, 7, 30) 
        expiry_date = to_date
        instrument = "FUTIDX"
        j = h._derivatives("NIFTY", from_date, to_date, expiry_date, instrument_type=instrument)
        assert j[0]['FH_TIMESTAMP'] == to_date.strftime("%d-%b-%Y")
        assert j[-1]['FH_TIMESTAMP'] == from_date.strftime("%d-%b-%Y")
        assert j[0]['FH_INSTRUMENT'] == instrument
        assert j[0]['FH_LAST_TRADED_PRICE'] == '11101.35'
    
    
    def test__index_options(self):
        from_date = date(2020, 7, 1)
        to_date = date(2020, 7, 30) 
        expiry_date = to_date
        instrument = "OPTIDX"
        strike_price = 10500
        j = h._derivatives("NIFTY", from_date, to_date, expiry_date, instrument_type=instrument,
                            strike_price=strike_price, option_type="CE")
        assert j[0]['FH_TIMESTAMP'] == to_date.strftime("%d-%b-%Y")
        assert j[-1]['FH_TIMESTAMP'] == from_date.strftime("%d-%b-%Y")
        assert j[0]['FH_INSTRUMENT'] == instrument
        assert j[0]['FH_LAST_TRADED_PRICE'] == '603.35'
        assert j[0]['FH_OPTION_TYPE'] == "CE"
    
    def test_errors(self):
        from_date = date(2020, 7, 1)
        to_date = date(2020, 7, 30) 
        expiry_date = to_date
        instrument = "OPTIDX"
        strike_price = 10500
        with pytest.raises(Exception):
            h._derivatives("NIFTY", from_date, to_date, expiry_date, instrument_type=instrument)
            h._derivatives("NIFTY", from_date, to_date, expiry_date, instrument_type=instrument, strike_price=33)
            h._derivatives("NIFTY", from_date, to_date, expiry_date, instrument_type=instrument, option_type="CE")
    
    def test_derivative_raw(self):
        from_date = date(2020, 6, 1)
        to_date = date(2020, 7, 30) 
        expiry_date = to_date
        instrument = "OPTIDX"
        strike_price = 10500
        j = h.derivatives_raw("NIFTY", from_date, to_date, expiry_date, instrument_type=instrument,
                            strike_price=strike_price, option_type="CE")
        assert j[0]['FH_TIMESTAMP'] == to_date.strftime("%d-%b-%Y")
        assert j[-1]['FH_TIMESTAMP'] == from_date.strftime("%d-%b-%Y")
        assert j[0]['FH_INSTRUMENT'] == instrument
        assert j[0]['FH_LAST_TRADED_PRICE'] == '603.35'
        assert j[0]['FH_OPTION_TYPE'] == "CE"
        app_name = nse.APP_NAME + '-derivatives'
        files = os.listdir(user_cache_dir(app_name, app_name))
        assert len(files) == 2
        assert '2020-07-30-2020-07-01-OPTIDX-CE-10500-NIFTY-2020-07-30' in files
        assert '2020-07-30-2020-06-01-OPTIDX-CE-10500-NIFTY-2020-06-30' in files
    
    def test_futures_csv(self):
        symbol = "NIFTY"
        from_date = date(2020, 6, 1)
        to_date = date(2020, 7, 30) 
        expiry_date = to_date
        instrument = "FUTIDX"
        j = nse.derivatives_csv(symbol , from_date, to_date, expiry_date, instrument_type=instrument, output="/tmp/x.csv")
        with open(j) as fp:
            r = list(csv.reader(fp))
            assert r[0][0] == "DATE" 
            assert r[1][0] == to_date.strftime("%d-%b-%Y")
            assert r[-1][0] == from_date.strftime("%d-%b-%Y")
            assert r[-1][2] == "9626.85"
            assert r[1][2] == "11253.65"

        symbol = "SBIN"
        instrument = "FUTSTK"
        j = nse.derivatives_csv(symbol , from_date, to_date, expiry_date, instrument_type=instrument, output="/tmp/x.csv")
        with open(j) as fp:
            r = list(csv.reader(fp))
            assert r[0][0] == "DATE" 
            assert r[1][0] == to_date.strftime("%d-%b-%Y")
            assert r[-1][0] == from_date.strftime("%d-%b-%Y")
            assert r[-1][2] == "162.65"
            assert r[1][2] == "192.85"
    
    def test_options_csv(self):
        symbol = "NIFTY"
        from_date = date(2020, 6, 1)
        to_date = date(2020, 7, 30) 
        expiry_date = to_date
        instrument = "OPTIDX"
        strike_price = 10000
        option_type = "CE"
        j = nse.derivatives_csv(symbol , from_date, to_date, expiry_date, instrument_type=instrument, 
                                option_type=option_type, strike_price=strike_price, output="/tmp/x.csv")
        with open(j) as fp:
            r = list(csv.reader(fp))
            assert r[0][0] == "DATE" 
            #assert r[1][0] == to_date.strftime("%d-%b-%Y")
            assert r[-1][0] == from_date.strftime("%d-%b-%Y")
            assert r[-1][1] == expiry_date.strftime("%d-%b-%Y")
            assert r[-1][2] == "CE" 
            assert r[-1][3] == "10000.00"
            assert r[-1][4] == "219.90"
            #assert r[1][4] == "469.05"

        symbol = "SBIN"
        instrument = "OPTSTK"
        strike_price = 190
        option_type = "CE"
        j = nse.derivatives_csv(symbol , from_date, to_date, expiry_date, instrument_type=instrument, 
                                option_type=option_type, strike_price=strike_price, output="/tmp/x.csv")
        with open(j) as fp:
            r = list(csv.reader(fp))
            assert r[0][0] == "DATE" 
            #assert r[1][0] == to_date.strftime("%d-%b-%Y")
            assert r[-1][0] == from_date.strftime("%d-%b-%Y")
            assert r[-1][1] == expiry_date.strftime("%d-%b-%Y")
            assert r[-1][2] == "CE" 
            assert r[-1][3] == "190.00"
            assert r[-1][4] == "6.05"
            #assert r[1][4] == "469.05"
        warnings.warn("Test is work in progress because NSE's new website does not provide correct Derivatives data")
    
    def test_futures_df(self):
        symbol = "NIFTY"
        from_date = date(2020, 6, 1)
        to_date = date(2020, 7, 30) 
        expiry_date = to_date
        instrument = "FUTIDX"
        j = nse.derivatives_df(symbol , from_date, to_date, expiry_date, instrument_type=instrument)
        assert j.columns[0] == "DATE" 
        assert j["DATE"].iloc[0] == to_date
        assert j["DATE"].iloc[-1] == from_date
        assert j["OPEN"].iloc[-1] == 9626.85
        assert j["OPEN"].iloc[0] == 11253.65
        symbol = "SBIN"
        instrument = "FUTSTK"
        j = nse.derivatives_df(symbol , from_date, to_date, expiry_date, instrument_type=instrument)
        assert j.columns[0] == "DATE" 
        assert j["DATE"].iloc[0] == to_date
        assert j["DATE"].iloc[-1] == from_date
        assert j["OPEN"].iloc[-1] == 162.65
        assert j["OPEN"].iloc[0] == 192.85
    
    def test_options_df(self):
        symbol = "NIFTY"
        from_date = date(2020, 6, 1)
        to_date = date(2020, 7, 30) 
        expiry_date = to_date
        instrument = "OPTIDX"
        strike_price = 10000.0
        option_type = "CE"
        j = nse.derivatives_df(symbol , from_date, to_date, expiry_date, instrument_type=instrument,
                                strike_price=strike_price, option_type=option_type)
        assert j.columns[0] == "DATE" 
        # assert j["DATE"].iloc[0] == to_date
        assert j["DATE"].iloc[-1] == from_date
        assert j["OPEN"].iloc[-1] == 219.90
        #assert j["OPEN"].iloc[0] == 1250.8
        
        symbol = "SBIN"
        instrument = "OPTSTK"
        strike_price = 190.0
        option_type = "PE"
        j = nse.derivatives_df(symbol , from_date, to_date, expiry_date, instrument_type=instrument,
                                strike_price=strike_price, option_type=option_type)
        print(j.iloc[0])
        assert j.columns[0] == "DATE" 
        assert j["DATE"].iloc[0] == to_date
        assert j["DATE"].iloc[-1] == from_date
        assert j["LTP"].iloc[-1] == 32.95
        assert j["OPEN"].iloc[0] == 0.75 
