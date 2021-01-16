from datetime import datetime
from requests import Session

class NSELive:
    page_url = "https://www.nseindia.com/get-quotes/equity?symbol=LT"
    stock_meta_url = "https://www.nseindia.com/api/equity-meta-info"
    stock_quote_url = "https://www.nseindia.com/api/quote-equity"
    market_status = "https://www.nseindia.com/api/marketStatus"
    
    def __init__(self):
        self.s = Session()
        h = {
            "Host": "www.nseindia.com",
            "Referer": "https://www.nseindia.com/get-quotes/equity?symbol=SBIN",
            "X-Requested-With": "XMLHttpRequest",
            "pragma": "no-cache",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            }
        self.s.headers.update(h)
        self.s.get(self.page_url)

    def stock_quote(self, symbol):
        data = {"symbol": symbol}
        r = self.s.get(self.stock_quote_url, params=data)
        return r.json()


