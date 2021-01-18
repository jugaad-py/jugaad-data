from datetime import datetime
from requests import Session

class NSELive:
    base_url = "https://www.nseindia.com/api"
    page_url = "https://www.nseindia.com/get-quotes/equity?symbol=LT"
    _routes = {
            "stock_meta": "/equity-meta-info",
            "stock_quote": "/quote-equity",
            "stock_derivative_quote": "/quote-derivative",
            "market_status": "/marketStatus",
            "chart_data": "/chart-databyindex",
            "market_turnover": "/market-turnover",
            "equity_derivative_turnover": "/equity-stock",
            "all_indices": "/allIndices",
            "live_index": "/equity-stockIndices",
            "index_option_chain": "/option-chain-indices",
    }
    
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

    def get(self, route, payload={}):
        url = self.base_url + self._routes[route]
        r = self.s.get(url, params=payload)
        return r.json()

    def stock_quote(self, symbol):
        data = {"symbol": symbol}
        return self.get("stock_quote", data) 

    def stock_quote_fno(self, symbol):
        data = {"symbol": symbol}
        return self.get("stock_derivative_quote", data)

    def trade_info(self, symbol):
        data = {"symbol": symbol, "section": "trade_info"}
        return self.get("stock_quote", data) 

    def market_status(self):
        return self.get("market_status", {})

    def chart_data(self, symbol, indices=False):
        data = {"index" : symbol + "EQN"}
        if indices:
            data["index"] = symbol
            data["indices"] = "true"
        return self.get("chart_data", data)
    
    def tick_data(self, symbol, indices=False):
        return self.chart_data(symbol, indices)

    def market_turnover(self):
        return self.get("market_turnover")

    def eq_derivative_turnover(self, type="allcontracts"):
        data = {"index": type}
        return self.get("equity_derivative_turnover", data)
    
    def all_indices(self):
        return self.get("all_indices")

    def live_index(self, symbol="NIFTY 50"):
        data = {"index" : symbol}
        return self.get("live_index", data)
    
    def index_option_chain(self, symbol="NIFTY"):
        data = {"symbol": symbol}
        return self.get("index_option_chain", data)

    def live_fno(self):
        return self.live_index("SECURITIES IN F&O")
