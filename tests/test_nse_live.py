from jugaad_data.nse.live import NSELive

def test_quote():
    n = NSELive()
    r = n.stock_quote("HDFC")
    assert r['info']['symbol'] == 'HDFC'

