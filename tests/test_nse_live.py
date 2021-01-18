from jugaad_data.nse.live import NSELive

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
    assert "closePrice" in d
    assert "identifier" in d
    assert "grapthData" in d
    d = n.tick_data("NIFTY 50", True)
    assert "closePrice" in d
    assert "grapthData" in d
    assert "identifier" in d

def test_market_turnover():
    d = n.market_turnover()
    assert "data" in d
    assert len(d['data']) > 1
    assert 'name' in d['data'][0]

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

def test_live_fno():
    d = n.live_fno()
    assert "SECURITIES IN F&O" == d['name']

