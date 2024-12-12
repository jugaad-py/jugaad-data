"""
    Implements live data fetch functionality
"""
from datetime import datetime
import httpx
from ..util import live_cache
class NSELive:
    time_out = 5
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
            "equity_option_chain": "/option-chain-equities",
            "currency_option_chain": "/option-chain-currency",
            "pre_open_market": "/market-data-pre-open",
            "holiday_list": "/holiday-master?type=trading"
    }

    def __init__(self):
        headers = {
            "host": "www.nseindia.com",
            "cache-control": "no-cache",
            "dnt": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "sec-fetch-user": "?1",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "accept-language": "en-US,en;q=0.9,hi;q=0.8",
            "accept-encoding": "gzip, deflate, br",
        }
        
        self.client = httpx.Client(http2=True, timeout=self.time_out, headers=headers)
        self.client.headers.update(headers)
        self.client.get(self.page_url)

    def get(self, route, payload={}):
        url = self.base_url + self._routes[route]
        response = self.client.get(url, params=payload)
        response.raise_for_status()  # To ensure we catch HTTP errors
        return response.json()

    @live_cache
    def stock_quote(self, symbol):
        data = {"symbol": symbol}
        return self.get("stock_quote", data)

    @live_cache
    def stock_quote_fno(self, symbol):
        data = {"symbol": symbol}
        return self.get("stock_derivative_quote", data)

    @live_cache
    def trade_info(self, symbol):
        data = {"symbol": symbol, "section": "trade_info"}
        return self.get("stock_quote", data)

    @live_cache
    def market_status(self):
        return self.get("market_status", {})

    @live_cache
    def chart_data(self, symbol, indices=False):
        data = {"index" : symbol + "EQN"}
        if indices:
            data["index"] = symbol
            data["indices"] = "true"
        return self.get("chart_data", data)

    @live_cache
    def tick_data(self, symbol, indices=False):
        return self.chart_data(symbol, indices)

    @live_cache
    def market_turnover(self):
        return self.get("market_turnover")

    @live_cache
    def eq_derivative_turnover(self, type="allcontracts"):
        data = {"index": type}
        return self.get("equity_derivative_turnover", data)

    @live_cache
    def all_indices(self):
        return self.get("all_indices")

    def live_index(self, symbol="NIFTY 50"):
        data = {"index" : symbol}
        return self.get("live_index", data)

    @live_cache
    def index_option_chain(self, symbol="NIFTY"):
        data = {"symbol": symbol}
        return self.get("index_option_chain", data)

    @live_cache
    def equities_option_chain(self, symbol):
        data = {"symbol": symbol}
        return self.get("equity_option_chain", data)

    @live_cache
    def currency_option_chain(self, symbol="USDINR"):
        data = {"symbol": symbol}
        return self.get("currency_option_chain", data)

    @live_cache
    def live_fno(self):
        return self.live_index("SECURITIES IN F&O")

    @live_cache
    def pre_open_market(self, key="NIFTY"):
        data = {"key": key}
        return self.get("pre_open_market", data)

    @live_cache
    def holiday_list(self):
        return self.get("holiday_list", {})
