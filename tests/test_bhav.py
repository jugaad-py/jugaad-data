import io
import json
import zipfile
from datetime import date, datetime
from unittest.mock import MagicMock, patch

from jugaad_data.nse import (bhavcopy_raw, full_bhavcopy_raw, bhavcopy_fo_raw,
                             bhavcopy_index_raw, expiry_dates,
                             bhavcopy_old_raw, NSEArchives)
import pytest
import requests

# Old cm bhavcopy format (fetched via NSE reports API), includes ISIN field
OLD_BHAVCOPY_HEADER = ("SYMBOL,SERIES,OPEN,HIGH,LOW,CLOSE,LAST,PREVCLOSE,"
                       "TOTTRDQTY,TOTTRDVAL,TIMESTAMP,TOTALTRADES,ISIN")

def _old_bhavcopy_text():
    return (OLD_BHAVCOPY_HEADER + "\n"
            "SBIN,EQ,355.0,360.0,352.1,358.5,357.0,354.3,100000,35800000.0,"
            "01-JAN-2020,5000,INE062A01020\n")

def _zip_bytes(text):
    fp = io.BytesIO()
    with zipfile.ZipFile(fp, "w") as zf:
        zf.writestr("cm01JAN2020bhav.csv", text)
    return fp.getvalue()

@pytest.mark.live
def test_bhavcopy():
    """Test bhavcopy for a historical date (before UDiff format)

    When UDiff is not available, bhavcopy_raw must fall back to the old
    bhavcopy format (which has the ISIN field) instead of BHAVDATA-FULL.
    """
    r = bhavcopy_raw(date(2020, 1, 1))
    header = r.splitlines()[0]
    assert "RELIANCE" in r or "SBIN" in r  # At least some stock data present
    # Old format header with ISIN field
    assert header.startswith("SYMBOL,SERIES")
    assert "ISIN" in header
    # Must NOT be the full bhavcopy (BHAVDATA-FULL) format
    assert "DELIV_QTY" not in header

@pytest.mark.live
def test_bhavcopy_old_raw():
    """Test direct download of the old-format bhavcopy via reports API"""
    import re
    isin_re = re.compile(r",IN[A-Z0-9]{10},\s*$")  # 12-char ISIN at row end
    r = bhavcopy_old_raw(date(2020, 1, 1))
    header = r.splitlines()[0]
    assert header.startswith(OLD_BHAVCOPY_HEADER[:15])
    assert "ISIN" in header
    assert "RELIANCE" in r or "SBIN" in r
    # Rows must carry an actual ISIN value e.g. INE062A01020 for SBIN
    assert any(isin_re.search(line) for line in r.splitlines()[1:])

@pytest.mark.live
def test_bhavcopy_old_raw_not_available_for_udiff_dates():
    """Old-format file returns 404 for dates after the UDiff switch"""
    nse = NSEArchives()
    with pytest.raises(requests.RequestException):
        nse.bhavcopy_old_raw(date(2024, 7, 10))

@pytest.mark.live
def test_bhavcopy_recent():
    """Test bhavcopy for recent date using UDiff format
    
    For dates >= Jul 8, 2024, should use UDiff format.
    UDiff format has different columns: TradDt,BizDt,Sgmt,Src,FinInstrmTp,...
    Uses a fixed past trading date so the response is cached and reliable.
    """
    r = bhavcopy_raw(date(2024, 7, 10))
    assert len(r) > 0
    header = r.splitlines()[0]
    assert header.startswith("TradDt")
    assert "ISIN" in header


@pytest.mark.live
def test_bhavcopy_historical_udiff():
    """Test bhavcopy for a historical UDiFF-era date

    The daily-reports API only serves current/previous trading day, so older
    UDiFF dates must come from the historical UDiFF archive. Regression test
    for bhavcopy_raw silently returning legacy format for dates >= Jul 8, 2024.
    """
    r = bhavcopy_raw(date(2025, 7, 21))
    header = r.splitlines()[0]
    assert header.startswith("TradDt")
    assert "ISIN" in header
    assert not header.startswith("SYMBOL, SERIES")

# def test_full_bhavcopy():
#     r = full_bhavcopy_raw(date(2020,1,1))
#     header = "SYMBOL, SERIES, DATE1, PREV_CLOSE, OPEN_PRICE, HIGH_PRICE, LOW_PRICE, LAST_PRICE, CLOSE_PRICE, AVG_PRICE, TTL_TRD_QNTY, TURNOVER_LACS, NO_OF_TRADES, DELIV_QTY, DELIV_PER"
#     assert "SBIN" in r
#     assert header in r

#     with pytest.raises(requests.exceptions.ReadTimeout) as e:
#         r = full_bhavcopy_raw(date(2019,1,1))
#     assert '2019' in e.value.args[0]    

@pytest.mark.live
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

@pytest.mark.live
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


@pytest.mark.live
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


@pytest.mark.live
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

# ---------------------------------------------------------------------------
# Offline (mocked) tests - run in CI without network access
# ---------------------------------------------------------------------------

def test_bhavcopy_raw_falls_back_to_old_format_when_udiff_unavailable():
    """When both UDiff sources fail, fall back to old format (with ISIN),
    not to the full bhavcopy (BHAVDATA-FULL) format."""
    n = NSEArchives()
    with patch.object(n, "bhavcopy_udiff_raw",
                      side_effect=zipfile.BadZipFile("not available")), \
         patch.object(n.daily_reports, "download_file",
                      side_effect=ValueError("not found")), \
         patch.object(n, "bhavcopy_old_raw",
                      return_value=_old_bhavcopy_text()) as m_old, \
         patch.object(n, "full_bhavcopy_raw") as m_full:
        out = n.bhavcopy_raw(date(2024, 7, 10))
    assert out == _old_bhavcopy_text()
    m_old.assert_called_once_with(date(2024, 7, 10))
    m_full.assert_not_called()

def test_bhavcopy_raw_skips_udiff_for_pre_udiff_dates():
    """Pre-UDiff dates must go straight to the old-format fallback"""
    n = NSEArchives()
    m_udiff = MagicMock()
    with patch.object(n, "bhavcopy_udiff_raw", m_udiff), \
         patch.object(n, "bhavcopy_old_raw",
                      return_value=_old_bhavcopy_text()) as m_old:
        out = n.bhavcopy_raw(date(2020, 1, 1))
    assert m_udiff.call_count == 0
    m_old.assert_called_once_with(date(2020, 1, 1))
    assert "ISIN" in out.splitlines()[0]

def test_bhavcopy_old_raw_request_and_unzip():
    """bhavcopy_old_raw must hit the NSE reports API with correct params
    and return the unzipped old-format CSV text"""
    n = NSEArchives()
    resp = MagicMock()
    resp.status_code = 200
    resp.content = _zip_bytes(_old_bhavcopy_text())
    with patch.object(n.s, "get", return_value=resp) as m_get:
        text = n.bhavcopy_old_raw(datetime(2020, 1, 1))
    url = m_get.call_args[0][0]
    params = m_get.call_args[1]["params"]
    assert url == "https://www.nseindia.com/api/reports"
    archives = json.loads(params["archives"])
    assert archives[0] == {"name": "CM - Bhavcopy(csv)",
                           "type": "daily-reports",
                           "category": "capital-market",
                           "section": "equities"}
    assert params["date"] == "01-Jan-2020"
    assert params["type"] == "equities"
    assert params["mode"] == "single"
    assert text.splitlines()[0].startswith(OLD_BHAVCOPY_HEADER[:15])
    assert "INE062A01020" in text

def test_bhavcopy_old_raw_raises_when_file_missing():
    """NSE returns 404 when the old-format file does not exist for a date"""
    n = NSEArchives()
    resp = MagicMock()
    resp.status_code = 404
    resp.raise_for_status.side_effect = requests.exceptions.HTTPError("404")
    with patch.object(n.s, "get", return_value=resp):
        with pytest.raises(requests.exceptions.HTTPError):
            n.bhavcopy_old_raw(date(2024, 7, 10))

"""
@pytest.mark.live
def test_bhavcopy_on_holiday():
    r = bhavcopy_raw(date(2020,1,5))
    header = "SYMBOL,SERIES,OPEN,HIGH,LOW,CLOSE,LAST,PREVCLOSE,TOTTRDQTY,TOTTRDVAL,TIMESTAMP,TOTALTRADES,ISIN"
    assert "RELIANCE" in r
    assert header in r

"""
