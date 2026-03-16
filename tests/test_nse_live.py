from jugaad_data.nse.live import NSELive
from datetime import date, datetime
n = NSELive()
def test_stock_quote():
    r = n.stock_quote("HDFC")
    assert r['info']['symbol'] == 'HDFC'

def test_stock_quote_fno():
    r = n.stock_quote_fno("HDFC")
    assert 'strikePrices' in r
    assert 'info' in r
    assert 'stocks' in r

def test_trade_info():
    r = n.trade_info("HDFC")
    assert "bulkBlockDeals" in r
    assert "marketDeptOrderBook" in r

def test_market_status():
    r = n.market_status()
    assert "marketState" in r

def test_tick_data():
    d = n.tick_data("HDFC")
    assert "grapthData" in d
    d = n.tick_data("NIFTY 50", True)
    assert "grapthData" in d
"""
def test_market_turnover():
    d = n.market_turnover()
    assert "data" in d
    assert len(d['data']) > 1
    assert 'name' in d['data'][0]
"""
def test_eq_derivative_turnover():
    d = n.eq_derivative_turnover()
    assert "value" in d
    assert "volume" in d
    assert len(d['value']) > 1
    assert len(d['volume']) > 1

    d = n.eq_derivative_turnover(type="fu_nifty50")
    assert "value" in d
    assert "volume" in d
    assert len(d['value']) > 1
    assert len(d['volume']) > 1

def test_all_indices():
    d = n.all_indices()
    assert "advances" in d
    assert "declines" in d
    assert len(d['data']) > 1

def test_live_index():
    d = n.live_index("NIFTY 50")
    assert "advance" in d
    assert len(d['data']) == 51

def test_index_option_chain():
    d = n.index_option_chain("NIFTY")
    assert "filtered" in d
    assert "records" in d

def test_equities_option_chain():
    d = n.equities_option_chain("RELIANCE")
    assert "filtered" in d
    assert "records" in d
    assert "data" in d["records"]

def test_currency_option_chain():
    d = n.currency_option_chain("USDINR")
    assert "filtered" in d
    assert "records" in d
    assert "data" in d["records"]

def test_live_fno():
    d = n.live_fno()
    assert "SECURITIES IN F&O" == d['name']

def test_pre_open_market():
    d = n.pre_open_market("NIFTY")
    assert "declines" in d
    assert "unchanged" in d
    assert "advances" in d

def test_corporate_announcements():
    d = n.corporate_announcements()
    assert type(d) == list
    if len(d) > 0:
        row = d[0]
        assert 'symbol' in row.keys()
    
    from_date = date(2024,1,1)
    to_date = date(2024,1,2)
    d = n.corporate_announcements(from_date=from_date, to_date=to_date)
    assert len(d) > 0
    for x in d:
        print(x['symbol'])
    if len(d) > 0:
        assert 'symbol' in d[0].keys()
    d = n.corporate_announcements(from_date=from_date, to_date=to_date, symbol='NESCO')
    
    assert d[0]['symbol'] == 'NESCO'