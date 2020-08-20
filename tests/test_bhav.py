from datetime import date
from jugaad_data.nse import bhavcopy_raw, full_bhavcopy_raw, bhavcopy_fo_raw


def test_bhavcopy():
    r = bhavcopy_raw(date(2020,1,1))
    header = "SYMBOL,SERIES,OPEN,HIGH,LOW,CLOSE,LAST,PREVCLOSE,TOTTRDQTY,TOTTRDVAL,TIMESTAMP,TOTALTRADES,ISIN"
    assert "RELIANCE" in r
    assert header in r

def test_full_bhavcopy():
    r = full_bhavcopy_raw(date(2020,1,1))
    header = "SYMBOL, SERIES, DATE1, PREV_CLOSE, OPEN_PRICE, HIGH_PRICE, LOW_PRICE, LAST_PRICE, CLOSE_PRICE, AVG_PRICE, TTL_TRD_QNTY, TURNOVER_LACS, NO_OF_TRADES, DELIV_QTY, DELIV_PER"
    assert "SBIN" in r
    assert header in r

def test_bhavcopy_fo():
    r = bhavcopy_fo_raw(date(2020,1,1))
    header = "INSTRUMENT,SYMBOL,EXPIRY_DT,STRIKE_PR,OPTION_TYP,OPEN,HIGH,LOW,CLOSE,SETTLE_PR,CONTRACTS,VAL_INLAKH,OPEN_INT,CHG_IN_O"
    assert "SBIN" in r
    assert header in r


"""
def test_bhavcopy_on_holiday():
    r = bhavcopy_raw(date(2020,1,5))
    header = "SYMBOL,SERIES,OPEN,HIGH,LOW,CLOSE,LAST,PREVCLOSE,TOTTRDQTY,TOTTRDVAL,TIMESTAMP,TOTALTRADES,ISIN"
    assert "RELIANCE" in r
    assert header in r

"""
