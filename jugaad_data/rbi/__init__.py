import re

from requests import Session
from bs4 import BeautifulSoup


class RateNotAvailable(Exception):
    """RBI shows no value for the requested rate (e.g. no recent T-bill auction)."""


# RBI label -> output key, for rows holding a single rate or a "min - max" range
_RATE_KEYS = {
    "Policy Repo Rate": "policy_repo_rate",
    "Standing Deposit Facility Rate": "standing_deposit_facility_rate",
    "Marginal Standing Facility Rate": "marginal_standing_facility_rate",
    "Bank Rate": "bank_rate",
    "Fixed Reverse Repo Rate": "fixed_reverse_repo_rate",
    "CRR": "crr",
    "SLR": "slr",
    "Base Rate": "base_rate",
    "MCLR (Overnight)": "mclr_overnight",
    "Savings Deposit Rate": "savings_deposit_rate",
    "Term Deposit Rate > 1 Year": "term_deposit_rate_gt_1y",
    "Call Rates": "call_rate",
}
_INDEX_KEYS = {"S&P BSE Sensex": "sensex", "Nifty 50": "nifty_50"}

_NUM = r"\d+(?:\.\d+)?"


def _fraction(pct):
    """'5.50' -> 0.055"""
    return round(float(pct) / 100, 8)


def _parse_rate(text):
    """'5.50%' -> 0.055, '8.40% - 10.00%' -> {'min': 0.084, 'max': 0.1}, '-%' -> None"""
    m = re.fullmatch(r"(%s)%%\s*-\s*(%s)%%" % (_NUM, _NUM), text)
    if m:
        return {"min": _fraction(m.group(1)), "max": _fraction(m.group(2))}
    m = re.fullmatch(r"(%s)%%" % _NUM, text)
    if m:
        return _fraction(m.group(1))
    return None


def _clean(value):
    """Strip RBI's footnote markers (':', '*', '#') and whitespace."""
    return " ".join(value.replace(":", "").replace("*", "").replace("#", "").split())


def parse_rates(html):
    """Parse the RBI home page into a structured dict (see RBI.current_rates)."""
    rates = {"fx": [], "gsec": [], "tbill": [], "indices": {}}
    bs = BeautifulSoup(html, "html.parser")
    for tr in bs.find_all("tr"):
        tds = tr.find_all(["th", "td"])
        if len(tds) < 2:
            continue
        label = " ".join(tds[0].get_text().split())
        value = _clean(tds[1].get_text())

        if label in _RATE_KEYS:
            rates[_RATE_KEYS[label]] = _parse_rate(value)
        elif label in _INDEX_KEYS:
            rates["indices"][_INDEX_KEYS[label]] = float(value)
        elif (m := re.fullmatch(r"INR / (\d+) (\w+)", label)):
            rates["fx"].append({"currency": m.group(2), "units": int(m.group(1)), "inr": float(value)})
        elif (m := re.fullmatch(r"(%s)%% GS (\d{4})" % _NUM, label)):
            rates["gsec"].append({"coupon": _fraction(m.group(1)),
                                  "maturity_year": int(m.group(2)),
                                  "yield": _parse_rate(value)})
        elif (m := re.fullmatch(r"(\d+) day T-bills", label)):
            rates["tbill"].append({"days": int(m.group(1)), "yield": _parse_rate(value)})
    return rates


class RBI:
    base_url = "https://www.rbi.org.in/"

    def __init__(self):
        self.s = Session()

    def current_rates(self):
        """Current rates shown on the RBI home page.

        Percentages are fractions (5.5% -> 0.055). A range is
        {"min": ..., "max": ...}. A value RBI shows as "-" is None.
        Rows RBI adds that are not listed here are ignored.

            {
              "policy_repo_rate": 0.055,
              "standing_deposit_facility_rate": 0.0525,
              "marginal_standing_facility_rate": 0.0575,
              "bank_rate": 0.0575,
              "fixed_reverse_repo_rate": 0.0335,
              "crr": 0.03, "slr": 0.18,
              "base_rate": {"min": 0.084, "max": 0.1},
              "mclr_overnight": {"min": 0.078, "max": 0.08},
              "savings_deposit_rate": 0.025,
              "term_deposit_rate_gt_1y": {"min": 0.06, "max": 0.0675},
              "call_rate": {"min": 0.0485, "max": 0.059},
              "fx": [{"currency": "USD", "units": 1, "inr": 94.6986}, ...],
              "gsec": [{"coupon": 0.062, "maturity_year": 2029, "yield": 0.06947}, ...],
              "tbill": [{"days": 91, "yield": None}, ...],
              "indices": {"sensex": 73709.69, "nifty_50": 22811.35}
            }
        """
        r = self.s.get(self.base_url)
        return parse_rates(r.text)

    def tbill_rate(self, days):
        """Cut-off yield (fraction) of the 91, 182 or 364 day T-bill.

        Raises RateNotAvailable if RBI shows no value (no recent auction cut-off).
        """
        for t in self.current_rates()["tbill"]:
            if t["days"] == days:
                if t["yield"] is None:
                    raise RateNotAvailable("RBI shows no cut-off for the %d day T-bill" % days)
                return t["yield"]
        raise RateNotAvailable("No %d day T-bill on the RBI page" % days)
