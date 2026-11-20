from datetime import date

import pytest

from jugaad_data.nse import history

D1, D2 = date(2026, 1, 1), date(2026, 1, 2)


def test_empty_derivatives_futures_preserves_columns(monkeypatch):
    monkeypatch.setattr(history, "derivatives_raw", lambda *a, **k: [])
    result = history.derivatives_df("SBIN", D1, D2, date(2026, 1, 29), "FUTSTK")
    assert result.empty
    assert result.columns.tolist() == history.futures_final_headers


def test_empty_derivatives_options_preserves_columns(monkeypatch):
    monkeypatch.setattr(history, "derivatives_raw", lambda *a, **k: [])
    result = history.derivatives_df(
        "SBIN", D1, D2, date(2026, 1, 29), "OPTSTK", strike_price=500, option_type="CE"
    )
    assert result.empty
    assert result.columns.tolist() == history.options_final_headers


def test_empty_index_df(monkeypatch):
    monkeypatch.setattr(history, "index_raw", lambda *a, **k: [])
    result = history.index_df("NIFTY 50", D1, D2)
    assert result.empty
    assert "HistoricalDate" in result.columns and "CLOSE" in result.columns


def test_empty_index_pe_df(monkeypatch):
    monkeypatch.setattr(history, "index_pe_raw", lambda *a, **k: [])
    result = history.index_pe_df("NIFTY 50", D1, D2)
    assert result.empty
    assert "pe" in result.columns and "DATE" in result.columns


def test_malformed_derivatives_still_raises(monkeypatch):
    monkeypatch.setattr(history, "derivatives_raw", lambda *a, **k: [{"FH_SYMBOL": "SBIN"}])
    with pytest.raises(KeyError):
        history.derivatives_df("SBIN", D1, D2, date(2026, 1, 29), "FUTSTK")
