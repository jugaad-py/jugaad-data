from datetime import date

import pytest

from jugaad_data import amfi
from jugaad_data.amfi import AMFI, parse_nav_history, COLUMNS


SAMPLE = (
    "\ufeffScheme Code;NAV Name;Plan;Option;ISIN Div Payout/ISIN Growth;"
    "ISIN Div Reinvestment;Net Asset Value;Date\n"
    "\n"
    "Open Ended Schemes ( Equity Scheme - Multi Cap Fund )\n"
    "\n"
    "HDFC Mutual Fund\n"
    "148921;HDFC Multi Cap Fund-Direct Growth;Direct Plan;GROWTH;INF209KB1Y49;;"
    "23.10;01-Sep-2026\n"
    "148920;HDFC Multi Cap Fund-Direct IDCW;Direct Plan;IDCW Payout;INF209KB1Y56;"
    "INF209KB1Y64;19.00;01-Sep-2026\n"
    "\n"
    "Close Ended Schemes ( Income )\n"
    "\n"
    "UTI Mutual Fund\n"
    "100001;UTI Close Ended Fund - Growth;;Growth;;;10.5000;01-Sep-2026\n"
    "\n"
    "Interval Fund Schemes ( Income )\n"
    "\n"
    "Nippon India Mutual Fund\n"
    "105692;NIPPON INDIA QUARTERLY INTERVAL FUND - IDCW Option;Regular Plan;"
    "IDCW Option;INF204K01DO3;INF204K01DP0;13.5648;01-Sep-2026\n"
)


def test_parse_nav_history_flattens_context():
    rows = parse_nav_history(SAMPLE)
    assert len(rows) == 4
    for row in rows:
        assert set(row.keys()) == set(COLUMNS)
    assert rows[0]["scheme_code"] == "148921"
    assert rows[0]["scheme_type"] == "Open Ended"
    assert rows[0]["category"] == "Equity Scheme - Multi Cap Fund"
    assert rows[0]["amc"] == "HDFC Mutual Fund"
    assert rows[0]["nav"] == "23.10"
    assert rows[2]["scheme_type"] == "Close Ended"
    assert rows[2]["category"] == "Income"
    assert rows[3]["scheme_type"] == "Interval Fund"
    assert rows[3]["amc"] == "Nippon India Mutual Fund"


def test_parse_nav_history_handles_blank_fields():
    rows = parse_nav_history(SAMPLE)
    blank = [r for r in rows if r["scheme_code"] == "100001"][0]
    assert blank["plan"] == ""
    assert blank["option"] == "Growth"
    assert blank["isin_growth"] == ""


def test_parse_nav_history_empty():
    assert parse_nav_history("") == []


def test_nav_history_raw_offline(monkeypatch):
    monkeypatch.setattr(AMFI, "_nav_history", lambda self, mf, f, t: SAMPLE)
    rows = amfi.nav_history_raw(date(2026, 9, 1), date(2026, 9, 1))
    assert len(rows) == 4


def test_nav_history_df_offline(monkeypatch):
    monkeypatch.setattr(AMFI, "_nav_history", lambda self, mf, f, t: SAMPLE)
    df = amfi.nav_history_df(date(2026, 9, 1), date(2026, 9, 1))
    assert list(df.columns) == COLUMNS
    assert df["nav"].dtype.kind == "f"
    assert df["scheme_type"].tolist() == [
        "Open Ended", "Open Ended", "Close Ended", "Interval Fund"
    ]
    assert df["nav"].iloc[0] == pytest.approx(23.10)


def test_nav_history_csv_offline(monkeypatch, tmp_path):
    monkeypatch.setattr(AMFI, "_nav_history", lambda self, mf, f, t: SAMPLE)
    out = tmp_path / "nav.csv"
    path = amfi.nav_history_csv(
        date(2026, 9, 1), date(2026, 9, 1), output=str(out)
    )
    assert path == str(out)
    lines = out.read_text().splitlines()
    assert lines[0] == ",".join(COLUMNS)
    assert len(lines) == 5


def test_scheme_type_list():
    assert amfi.scheme_type_list() == ["Open Ended", "Close Ended", "Interval Fund"]


@pytest.mark.live
def test_nav_history_raw_live():
    rows = amfi.nav_history_raw(date(2026, 9, 1), date(2026, 9, 1))
    assert len(rows) > 0
    first = rows[0]
    assert first["scheme_code"]
    assert first["scheme_name"]
    assert first["nav"]
    assert first["scheme_type"] in ["Open Ended", "Close Ended", "Interval Fund"]
