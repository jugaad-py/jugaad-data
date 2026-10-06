"""
    Implements functionality to download mutual fund NAV history from the
    AMFI (Association of Mutual Funds in India) website.

    Source: https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx

    The downloaded report is a semicolon separated file with one row per
    scheme per date:

        Scheme Code;NAV Name;Plan;Option;ISIN Div Payout/ISIN Growth;
        ISIN Div Reinvestment;Net Asset Value;Date

    Rows are grouped under two levels of context that are themselves not in
    the data rows:
        - a section header such as
          "Open Ended Schemes ( Equity Scheme - Multi Cap Fund )" which carries
          the scheme type (Open Ended / Close Ended / Interval Fund) and the
          category (e.g. Money Market, Equity Scheme - Large Cap Fund), and
        - an AMC (fund house) line such as "HDFC Mutual Fund".

    This module flattens that hierarchy into a single list of dicts where the
    section and AMC context is carried forward as columns on every row.
"""
import re
import csv
import requests

from jugaad_data import util as ut

try:
    import pandas as pd
except ImportError:
    pd = None

APP_NAME = "amfidata"

# The three top level scheme types AMFI uses in the report.
SCHEME_TYPES = ["Open Ended", "Close Ended", "Interval Fund"]

# Section header lines look like "Open Ended Schemes ( Equity Scheme - Large Cap Fund )".
# Note the category text itself is inconsistent in the source file
# ("Equity Scheme" vs "Equity Schemes", trailing "**", etc.) so it is kept as-is.
_SECTION_RE = re.compile(
    r"^(Open Ended|Close Ended|Interval Fund)\s+Schemes?\s*\(\s*(.*?)\s*\)\s*$"
)

# Output columns shared by the raw dicts, the DataFrame and the CSV.
COLUMNS = [
    "scheme_code",
    "scheme_name",
    "plan",
    "option",
    "isin_growth",
    "isin_reinvest",
    "nav",
    "date",
    "scheme_type",
    "category",
    "amc",
]


def parse_nav_history(text):
    """Parse the raw AMFI NAV history report text into a flat list of dicts.

    Args:
        text (str): Report text as returned by the AMFI endpoint (already
            decoded, ideally with the BOM stripped)

    Returns:
        list[dict]: One dict per scheme/date row. Each dict has the keys in
        ``COLUMNS``; all values are strings exactly as they appear in the
        report.
    """
    rows = []
    scheme_type = ""
    category = ""
    amc = ""
    for line in text.splitlines():
        line = line.strip().lstrip("\ufeff").strip()
        if not line:
            continue
        if line.startswith("Scheme Code"):
            # header row
            continue
        section = _SECTION_RE.match(line)
        if section:
            scheme_type = section.group(1)
            category = section.group(2)
            amc = ""
            continue
        if ";" not in line:
            # AMC (fund house) line
            amc = line
            continue
        parts = line.split(";")
        if len(parts) < 8:
            continue
        rows.append({
            "scheme_code": parts[0].strip(),
            "scheme_name": parts[1].strip(),
            "plan": parts[2].strip(),
            "option": parts[3].strip(),
            "isin_growth": parts[4].strip(),
            "isin_reinvest": parts[5].strip(),
            "nav": parts[6].strip(),
            "date": parts[7].strip(),
            "scheme_type": scheme_type,
            "category": category,
            "amc": amc,
        })
    return rows


class AMFI:
    """Downloads mutual fund NAV history from the AMFI website.

    NAV history for past dates is immutable, so the raw downloaded report is
    cached on disk (see ``jugaad_data.util.cached``) keyed on the date range.
    """
    base_url = "https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx"
    timeout = 60
    scheme_types = SCHEME_TYPES

    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({
            "user-agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/134.0.6998.166 Safari/537.36",
        })

    @ut.cached(APP_NAME)
    def _nav_history(self, mf, from_date, to_date):
        """Download the raw NAV history report text for the given range.

        Args:
            mf (str): AMFI AMC code to filter by, empty string for all AMCs
            from_date (date): Start date
            to_date (date): End date

        Returns:
            str: Raw semicolon separated report text (BOM stripped)

        Raises:
            requests.RequestException: If the download fails
        """
        params = {
            "mf": mf or "",
            "frmdt": from_date.strftime("%d-%b-%Y"),
            "todt": to_date.strftime("%d-%b-%Y"),
        }
        r = self.s.get(self.base_url, params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.content.decode("utf-8-sig")

    def nav_history_raw(self, from_date, to_date, mf=""):
        """Download and parse NAV history for the given date range.

        Args:
            from_date (date): Start date
            to_date (date): End date
            mf (str): AMFI AMC code to restrict the download to a single AMC.
                Empty string (default) downloads all AMCs.

        Returns:
            list[dict]: One dict per scheme/date row, keys as in ``COLUMNS``

        Raises:
            requests.RequestException: If the download fails
        """
        text = self._nav_history(mf, from_date, to_date)
        return parse_nav_history(text)

    def nav_history_df(self, from_date, to_date, mf=""):
        """Download NAV history as a pandas DataFrame.

        Args:
            from_date (date): Start date
            to_date (date): End date
            mf (str): AMFI AMC code filter, empty string for all AMCs

        Returns:
            pandas.DataFrame: Columns as in ``COLUMNS`` with ``nav`` cast to
            float and ``date`` cast to datetime

        Raises:
            ModuleNotFoundError: If pandas is not installed
            requests.RequestException: If the download fails
        """
        if not pd:
            raise ModuleNotFoundError(
                "Please install pandas using \n pip install pandas"
            )
        raw = self.nav_history_raw(from_date, to_date, mf=mf)
        if not raw:
            return pd.DataFrame(columns=COLUMNS)
        df = pd.DataFrame(raw)[COLUMNS]
        df["nav"] = df["nav"].apply(ut.np_float)
        df["date"] = df["date"].apply(ut.np_date)
        return df

    def nav_history_csv(self, from_date, to_date, output="", mf=""):
        """Download NAV history and save it to a CSV file.

        Args:
            from_date (date): Start date
            to_date (date): End date
            output (str): Output file path. Defaults to
                ``amfi-nav-{from_date}-{to_date}.csv``
            mf (str): AMFI AMC code filter, empty string for all AMCs

        Returns:
            str: Path of the written CSV file

        Raises:
            requests.RequestException: If the download fails
        """
        raw = self.nav_history_raw(from_date, to_date, mf=mf)
        if not output:
            output = "amfi-nav-{}-{}.csv".format(from_date, to_date)
        with open(output, "w", newline="") as fp:
            writer = csv.writer(fp)
            writer.writerow(COLUMNS)
            for row in raw:
                writer.writerow([row[c] for c in COLUMNS])
        return output

    def scheme_type_list(self):
        """Return the list of AMFI scheme types.

        Returns:
            list[str]: One of Open Ended, Close Ended, Interval Fund
        """
        return list(self.scheme_types)

    def category_list(self, from_date, to_date, mf=""):
        """Return the distinct scheme categories present in a date range.

        Args:
            from_date (date): Start date
            to_date (date): End date
            mf (str): AMFI AMC code filter, empty string for all AMCs

        Returns:
            list[str]: Sorted distinct category strings (the text inside the
            section header parentheses)
        """
        raw = self.nav_history_raw(from_date, to_date, mf=mf)
        return sorted({r["category"] for r in raw if r["category"]})

    def amc_list(self, from_date, to_date, mf=""):
        """Return the distinct AMCs (fund houses) present in a date range.

        Args:
            from_date (date): Start date
            to_date (date): End date
            mf (str): AMFI AMC code filter, empty string for all AMCs

        Returns:
            list[str]: Sorted distinct AMC names
        """
        raw = self.nav_history_raw(from_date, to_date, mf=mf)
        return sorted({r["amc"] for r in raw if r["amc"]})


a = AMFI()
nav_history_raw = a.nav_history_raw
nav_history_df = a.nav_history_df
nav_history_csv = a.nav_history_csv
scheme_type_list = a.scheme_type_list
category_list = a.category_list
amc_list = a.amc_list