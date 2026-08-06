import pytest
from jugaad_data.nse.live import NSELive
from datetime import date, datetime
n = NSELive()

@pytest.mark.live
def test_stock_quote():
    r = n.stock_quote("HDFCBANK")
    assert r['metaData']['symbol'] == 'HDFCBANK'

@pytest.mark.live
def test_stock_quote_fno():
    # Use a symbol with active derivatives (NIFTY or RELIANCE)
    r = n.stock_quote_fno("RELIANCE")
    # Validate response structure
    assert 'data' in r, "Response should have 'data' key"
    assert 'timestamp' in r, "Response should have 'timestamp' key"
    # Validate data is not empty
    assert len(r['data']) > 0, "Derivatives data should not be empty"
    
    # Validate first contract structure
    contract = r['data'][0]
    assert 'identifier' in contract
    assert 'instrumentType' in contract
    assert 'underlying' in contract
    assert contract['underlying'] == 'RELIANCE', "Underlying symbol should match requested symbol"
    assert 'expiryDate' in contract
    assert 'lastPrice' in contract or contract.get('lastPrice') is not None

@pytest.mark.live
def test_trade_info():
    r = n.trade_info("HDFCBANK")
    assert "orderBook" in r
    assert "tradeInfo" in r

@pytest.mark.live
def test_market_status():
    r = n.market_status()
    assert "marketState" in r

@pytest.mark.live
def test_tick_data():
    d = n.tick_data("HDFC")
    assert "grapthData" in d
    d = n.tick_data("NIFTY 50", True)
    assert "grapthData" in d
"""
@pytest.mark.live
def test_market_turnover():
    d = n.market_turnover()
    assert "data" in d
    assert len(d['data']) > 1
    assert 'name' in d['data'][0]
"""
@pytest.mark.live
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

@pytest.mark.live
def test_all_indices():
    d = n.all_indices()
    assert "advances" in d
    assert "declines" in d
    assert len(d['data']) > 1

@pytest.mark.live
def test_live_index():
    fresh = NSELive()
    d = fresh.live_index("NIFTY 50")
    assert "data" in d
    assert len(d['data']) >= 1

@pytest.mark.live
def test_index_option_chain():
    d = n.index_option_chain("NIFTY")
    assert "filtered" in d
    assert "records" in d

@pytest.mark.live
def test_equities_option_chain():
    d = n.equities_option_chain("RELIANCE")
    assert "filtered" in d
    assert "records" in d
    assert "data" in d["records"]

@pytest.mark.live
def test_currency_option_chain():
    d = n.currency_option_chain("USDINR")
    assert "filtered" in d
    assert "records" in d
    assert "data" in d["records"]

@pytest.mark.live
def test_live_fno():
    fresh = NSELive()
    d = fresh.live_fno()
    assert "data" in d
    assert "marketStatus" in d

@pytest.mark.live
def test_pre_open_market():
    d = n.pre_open_market("NIFTY")
    assert "declines" in d
    assert "unchanged" in d
    assert "advances" in d

@pytest.mark.live
def test_corporate_integrated_filing():
    # All filings (no filters)
    d = n.corporate_integrated_filing()
    assert isinstance(d, dict) or isinstance(d, list)

    # Filter by index
    d = n.corporate_integrated_filing(index="equities")
    assert isinstance(d, dict) or isinstance(d, list)

    # Filter by index=sme
    d = n.corporate_integrated_filing(index="sme")
    assert isinstance(d, dict) or isinstance(d, list)

    # Filter by symbol and issuer
    d = n.corporate_integrated_filing(
        index="equities",
        symbol="DIXON",
        issuer="Dixon Technologies (India) Limited",
        period_ended="all"
    )
    assert isinstance(d, dict) or isinstance(d, list)

    # Filter with date range
    from datetime import date
    d = n.corporate_integrated_filing(
        index="equities",
        symbol="DIXON",
        issuer="Dixon Technologies (India) Limited",
        period_ended="all",
        from_date=date(2026, 1, 1),
        to_date=date(2026, 6, 30)
    )
    assert isinstance(d, dict) or isinstance(d, list)

    # Ensure partial date raises exception
    import pytest
    with pytest.raises(Exception):
        n.corporate_integrated_filing(from_date=date(2026, 1, 1))

@pytest.mark.live
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