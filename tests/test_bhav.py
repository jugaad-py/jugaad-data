from datetime import date
from jugaad_data.nse import bhavcopy_raw, full_bhavcopy_raw, bhavcopy_fo_raw, bhavcopy_index_raw, expiry_dates 


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

def test_bhavcopy_index():
    r = bhavcopy_index_raw(date(2020,1,1))
    header = "Index Name,Index Date,Open Index Value,High Index Value,Low Index Value,Closing Index Value,Points Change,Change(%)"
    assert "NIFTY" in r
    assert header in r

def test_expiry_dates():
    dt = date(2020, 9, 28)
    dts = expiry_dates(dt, "OPTIDX", "NIFTY", 10000)
    assert date(2020, 10, 1) in dts
    assert date(2020, 10, 8) in dts
    dts = expiry_dates(dt, "FUTIDX", "NIFTY")
    assert len(dts) == 3
    dts = expiry_dates(dt, "FUTSTK", "RELIANCE")
    assert len(dts) == 3
    dts = expiry_dates(dt, "OPTSTK", "RELIANCE")
    assert date(2020, 10, 29) in dts
    assert date(2020, 11, 26) in dts


"""
def test_bhavcopy_on_holiday():
    r = bhavcopy_raw(date(2020,1,5))
    header = "SYMBOL,SERIES,OPEN,HIGH,LOW,CLOSE,LAST,PREVCLOSE,TOTTRDQTY,TOTTRDVAL,TIMESTAMP,TOTALTRADES,ISIN"
    assert "RELIANCE" in r
    assert header in r

"""
