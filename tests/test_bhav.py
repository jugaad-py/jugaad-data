from datetime import date
from jugaad_data.nse import bhavcopy_raw, full_bhavcopy_raw, bhavcopy_fo_raw, bhavcopy_index_raw, expiry_dates 
import pytest
import requests

def test_bhavcopy():
    """Test bhavcopy for a historical date (before UDiff format)
    
    For dates before Jul 8, 2024, uses BHAVDATA-FULL format.
    For recent dates, uses UDiff format with different column structure.
    """
    r = bhavcopy_raw(date(2020, 1, 1))
    # BHAVDATA-FULL format header (used for historical dates)
    header = "SYMBOL, SERIES, DATE1, PREV_CLOSE, OPEN_PRICE, HIGH_PRICE, LOW_PRICE, LAST_PRICE, CLOSE_PRICE, AVG_PRICE, TTL_TRD_QNTY, TURNOVER_LACS, NO_OF_TRADES, DELIV_QTY, DELIV_PER"
    assert "RELIANCE" in r or "SBIN" in r  # At least some stock data present
    assert header in r

def test_bhavcopy_recent():
    """Test bhavcopy for recent date using UDiff format
    
    For dates >= Jul 8, 2024, should use UDiff format from daily-reports API.
    UDiff format has different columns: TradDt,BizDt,Sgmt,Src,FinInstrmTp,...
    """
    from datetime import datetime, timedelta
    # Get a recent trading date
    today = date.today()
    # Skip if today is not a trading day (simplified check)
    try:
        r = bhavcopy_raw(today)
        # Check that we got data (either format)
        assert len(r) > 0
        # Should have ISIN field in both formats
        assert "ISIN" in r
    except requests.RequestException:
        # API may not have data for weekend/holiday
        pytest.skip("No data available for today")

# def test_full_bhavcopy():
#     r = full_bhavcopy_raw(date(2020,1,1))
#     header = "SYMBOL, SERIES, DATE1, PREV_CLOSE, OPEN_PRICE, HIGH_PRICE, LOW_PRICE, LAST_PRICE, CLOSE_PRICE, AVG_PRICE, TTL_TRD_QNTY, TURNOVER_LACS, NO_OF_TRADES, DELIV_QTY, DELIV_PER"
#     assert "SBIN" in r
#     assert header in r

#     with pytest.raises(requests.exceptions.ReadTimeout) as e:
#         r = full_bhavcopy_raw(date(2019,1,1))
#     assert '2019' in e.value.args[0]    

def test_bhavcopy_fo():
    r = bhavcopy_fo_raw(date(2020,1,1))
    header = "INSTRUMENT,SYMBOL,EXPIRY_DT,STRIKE_PR,OPTION_TYP,OPEN,HIGH,LOW,CLOSE,SETTLE_PR,CONTRACTS,VAL_INLAKH,OPEN_INT,CHG_IN_O"
    assert "SBIN" in r
    assert header in r

# def test_bhavcopy_index():
#     r = bhavcopy_index_raw(date(2020,1,1))
#     header = "Index Name,Index Date,Open Index Value,High Index Value,Low Index Value,Closing Index Value,Points Change,Change(%)"
#     assert "NIFTY" in r
#     assert header in r

def test_expiry_dates():
    dt = date(2020, 9, 28)
    dts = expiry_dates(dt)
    assert date(2020, 10, 1) in dts
    assert date(2020, 10, 8) in dts
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


def test_list_available_reports():
    """Test listing available reports from daily-reports API"""
    from jugaad_data.nse import NSEArchives
    nse = NSEArchives()
    try:
        reports = nse.list_available_reports()
        # Should have at least the UDiff bhavcopy
        assert 'CM-UDIFF-BHAVCOPY-CSV' in reports
        assert 'displayName' in reports['CM-UDIFF-BHAVCOPY-CSV']
        assert 'dates' in reports['CM-UDIFF-BHAVCOPY-CSV']
    except requests.RequestException:
        pytest.skip("API not available")


def test_download_report(tmp_path):
    """Test downloading a report via download_report method"""
    from jugaad_data.nse import NSEArchives
    nse = NSEArchives()
    try:
        # Try to download a report from previous day
        info = nse.download_report('CM-VOLATILITY', str(tmp_path))
        assert 'file_path' in info
        assert 'file_name' in info
        assert 'trading_date' in info
        # Check file was created
        import os
        assert os.path.exists(info['file_path']) or info.get('cached')
    except ValueError as e:
        # Some reports might not be available
        pytest.skip(f"Report not available: {str(e)}")
    except requests.RequestException:
        pytest.skip("API not available")

"""
def test_bhavcopy_on_holiday():
    r = bhavcopy_raw(date(2020,1,5))
    header = "SYMBOL,SERIES,OPEN,HIGH,LOW,CLOSE,LAST,PREVCLOSE,TOTTRDQTY,TOTTRDVAL,TIMESTAMP,TOTALTRADES,ISIN"
    assert "RELIANCE" in r
    assert header in r

"""
