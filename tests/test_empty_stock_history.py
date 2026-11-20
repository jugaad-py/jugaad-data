from datetime import date

import pytest

from jugaad_data.nse import history


def fetch_history():
    return history.stock_df("SBIN", date(2026, 1, 1), date(2026, 1, 2))


def test_empty_stock_history_preserves_columns(monkeypatch):
    monkeypatch.setattr(history, "stock_raw", lambda *args: [])

    result = fetch_history()

    assert result.empty
    assert result.columns.tolist() == history.stock_final_headers


def test_nonempty_stock_history_still_converts_fields(monkeypatch):
    raw = dict.fromkeys(history.stock_select_headers, "1")
    raw.update(CH_TIMESTAMP="2026-01-02", CH_SERIES="EQ", CH_SYMBOL="SBIN")
    monkeypatch.setattr(history, "stock_raw", lambda *args: [raw])

    result = fetch_history()

    assert result.columns.tolist() == history.stock_final_headers
    assert len(result) == 1
    assert result.loc[0, "SYMBOL"] == "SBIN"
    assert result.loc[0, "CLOSE"] == 1.0
    assert result.loc[0, "VOLUME"] == 1


def test_malformed_nonempty_history_still_raises(monkeypatch):
    monkeypatch.setattr(history, "stock_raw", lambda *args: [{"CH_SYMBOL": "SBIN"}])

    with pytest.raises(KeyError):
        fetch_history()
