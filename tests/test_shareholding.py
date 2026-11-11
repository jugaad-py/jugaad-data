from datetime import date

import pytest

from jugaad_data.nse.live import NSELive


def test_shareholding_pattern_payload():
    n = object.__new__(NSELive)
    n.get = lambda route, payload={}: {"route": route, "payload": payload}

    result = n.shareholding_pattern(
        from_date=date(2026, 8, 11),
        to_date=date(2026, 11, 11),
        symbol="SBIN",
    )
    assert result["route"] == "corporate_share_holdings"
    assert result["payload"] == {
        "index": "equities",
        "from_date": "11-08-2026",
        "to_date": "11-11-2026",
        "symbol": "SBIN",
    }


def test_shareholding_pattern_requires_both_dates():
    n = object.__new__(NSELive)
    with pytest.raises(Exception):
        n.shareholding_pattern(from_date=date(2026, 8, 11))


def test_shareholding_pattern_xml_downloads_entry():
    class Response:
        text = "<xbrli:xbrl/>"

        def raise_for_status(self):
            pass

    class Session:
        def get(self, url, **kwargs):
            assert url == "https://example.com/SHP.xml"
            assert kwargs["headers"] == {"Host": "example.com"}
            return Response()

    n = object.__new__(NSELive)
    n.s = Session()

    assert n.shareholding_pattern_xml({"xbrl": "https://example.com/SHP.xml"}) == "<xbrli:xbrl/>"
    assert n.shareholding_pattern_xml("https://example.com/SHP.xml") == "<xbrli:xbrl/>"


def test_shareholding_pattern_xml_requires_url():
    n = object.__new__(NSELive)
    with pytest.raises(ValueError):
        n.shareholding_pattern_xml({})
