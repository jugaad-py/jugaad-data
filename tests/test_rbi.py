import os

import pytest

from jugaad_data.rbi import RBI, RateNotAvailable, parse_rates

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


def _html(name):
    with open(os.path.join(FIXTURES, name)) as f:
        return f.read()


def _rbi(name):
    r = RBI()
    r.current_rates = lambda: parse_rates(_html(name))
    return r


def test_parse_rates():
    rates = parse_rates(_html("rbi_home.html"))
    assert rates["policy_repo_rate"] == 0.055
    assert rates["crr"] == 0.03
    assert rates["base_rate"] == {"min": 0.084, "max": 0.1}
    assert rates["call_rate"] == {"min": 0.0485, "max": 0.059}
    assert rates["savings_deposit_rate"] == 0.025
    assert rates["fx"] == [
        {"currency": "USD", "units": 1, "inr": 94.6986},
        {"currency": "JPY", "units": 100, "inr": 60.25},
    ]
    assert rates["gsec"][0] == {"coupon": 0.062, "maturity_year": 2029, "yield": 0.06947}
    assert rates["tbill"][0] == {"days": 91, "yield": 0.061}
    assert rates["indices"] == {"sensex": 73709.69, "nifty_50": 22811.35}


def test_tbill_not_available_is_none():
    rates = parse_rates(_html("rbi_home_no_tbill.html"))
    assert [t["yield"] for t in rates["tbill"]] == [None, None, None]
    assert rates["policy_repo_rate"] == 0.055  # rest of the page still parsed


def test_tbill_rate():
    assert _rbi("rbi_home.html").tbill_rate(91) == 0.061


def test_tbill_rate_not_available():
    with pytest.raises(RateNotAvailable):
        _rbi("rbi_home_no_tbill.html").tbill_rate(91)
    with pytest.raises(RateNotAvailable):
        _rbi("rbi_home.html").tbill_rate(30)


@pytest.mark.live
def test_current_rates():
    rates = RBI().current_rates()
    assert 0 < rates["policy_repo_rate"] < 0.25
    assert len(rates["gsec"]) > 0
    assert len(rates["tbill"]) == 3
    for t in rates["tbill"]:
        assert t["yield"] is None or 0 < t["yield"] < 0.25
