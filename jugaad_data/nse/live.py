"""
    Implements live data fetch functionality
"""
from datetime import datetime
from requests import Session
from ..util import live_cache
class NSELive:
    time_out = 5
    base_url = "https://www.nseindia.com/api"
    nextapi_url = "https://www.nseindia.com/api/NextApi/apiClient/GetQuoteApi"
    page_url = "https://www.nseindia.com/get-quotes/equity?symbol=LT"
    _routes = {
            "stock_meta": "/equity-meta-info",
            "stock_quote": "/quote-equity",
            "stock_derivative_quote": "/quote-derivative",
            "stock_derivatives_data": "/NextApi/apiClient/GetQuoteApi",
            "market_status": "/marketStatus",
            "chart_data": "/chart-databyindex",
            "market_turnover": "/market-turnover",
            "equity_derivative_turnover": "/equity-stock",
            "all_indices": "/allIndices",
            "live_index": "/equity-stock-indices",
            "option_chain_v3": "/option-chain-v3",
            "option_chain_contract_info": "/option-chain-contract-info",
            "currency_option_chain": "/option-chain-currency",
            "pre_open_market": "/market-data-pre-open",
            "holiday_list": "/holiday-master?type=trading",
            "corporate_announcements": "/corporate-announcements",
            "integrated_filing": "/integrated-filing-results"
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
            "User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36",
            "Sec-CH-UA": '"Google Chrome";v="134", "Chromium";v="134", "Not?A_Brand";v="99"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
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

    def _get_nextapi(self, function_name, **params):
        """Call NextApi endpoint with functionName and additional parameters.
        
        Args:
            function_name: The functionName parameter for NextApi
            **params: Additional query parameters
        
        Returns:
            Parsed JSON response from NextApi
        """
        query_params = {"functionName": function_name}
        query_params.update(params)
        r = self.s.get(self.nextapi_url, params=query_params)
        return r.json()

    @live_cache
    def stock_quote(self, symbol, market_type="N", series="EQ"):
        """Fetch live quote for an equity symbol.

        Args:
            symbol:      NSE stock symbol e.g. 'HDFCBANK'
            market_type: Market type code (default 'N' = Normal market)
            series:      Trading series (default 'EQ' = Equity)

        Returns:
            Dict with keys: metaData, priceInfo, tradeInfo, secInfo, orderBook, lastUpdateTime
        """
        r = self._get_nextapi("getSymbolData", marketType=market_type, series=series, symbol=symbol)
        return r["equityResponse"][0]

    @live_cache
    def stock_quote_fno(self, symbol):
        """Fetch live derivatives (futures & options) data for a symbol.
        
        Args:
            symbol: Stock/Index symbol (e.g., 'HDFC', 'NIFTY')
        
        Returns:
            Dictionary with derivatives data:
            {
                "data": [
                    {
                        "identifier": "OPTSTKHDFC30-Mar-2026CE2500.00",
                        "instrumentType": "OPTSTK",  # OPTSTK or FUTSTK
                        "underlying": "HDFC",
                        "expiryDate": "30-Mar-2026",
                        "optionType": "CE",  # CE, PE, or XX for futures
                        "strikePrice": "2500.00",
                        "lastPrice": 125.5,
                        "openInterest": 1234,
                        "totalTradedVolume": 5000,
                        "openPrice": 120.0,
                        "highPrice": 130.0,
                        "lowPrice": 119.5,
                        "changeInOpenInterest": 100,
                        ...more fields
                    },
                    ...more contracts
                ],
                "timestamp": "..."
            }
        
        Note: This uses the NSE NextApi endpoint (getSymbolDerivativesData).
        Returns all available contracts for the given symbol.
        """
        return self._get_nextapi("getSymbolDerivativesData", symbol=symbol)

    @live_cache
    def trade_info(self, symbol, market_type="N", series="EQ"):
        """Fetch trade info (order book depth, traded volumes) for an equity symbol.

        Args:
            symbol:      NSE stock symbol e.g. 'HDFCBANK'
            market_type: Market type code (default 'N' = Normal market)
            series:      Trading series (default 'EQ' = Equity)

        Returns:
            Dict with keys: metaData, priceInfo, tradeInfo, secInfo, orderBook, lastUpdateTime
        """
        r = self._get_nextapi("getSymbolData", marketType=market_type, series=series, symbol=symbol)
        return r["equityResponse"][0]

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
    def option_chain_contract_info(self, symbol):
        """Get available expiry dates and strike prices for an option chain symbol."""
        data = {"symbol": symbol}
        return self.get("option_chain_contract_info", data)

    @live_cache
    def index_option_chain(self, symbol="NIFTY", expiry=None):
        """Fetch option chain data for index.
        
        Args:
            symbol: Index symbol (e.g., 'NIFTY', 'BANKNIFTY')
            expiry: Optional expiry date in format 'DD-MMM-YYYY' (e.g., '30-Mar-2026')
                   If not provided, fetches contract info to get the nearest expiry
        """
        # If expiry is not provided, get the nearest one
        if not expiry:
            contract_info = self.option_chain_contract_info(symbol)
            if contract_info.get("expiryDates"):
                expiry = contract_info["expiryDates"][0]
        
        # Fetch option chain data
        data = {"type": "Indices", "symbol": symbol}
        if expiry:
            data["expiry"] = expiry
        
        return self.get("option_chain_v3", data)

    @live_cache
    def equities_option_chain(self, symbol, expiry=None):
        """Fetch option chain data for equity.
        
        Args:
            symbol: Stock symbol (e.g., 'RELIANCE', 'INFY')
            expiry: Optional expiry date in format 'DD-MMM-YYYY' (e.g., '27-Mar-2026')
                   If not provided, fetches contract info to get the nearest expiry
        """
        # If expiry is not provided, get the nearest one
        if not expiry:
            contract_info = self.option_chain_contract_info(symbol)
            if contract_info.get("expiryDates"):
                expiry = contract_info["expiryDates"][0]
        
        # Fetch option chain data
        data = {"type": "Equity", "symbol": symbol}
        if expiry:
            data["expiry"] = expiry
        
        return self.get("option_chain_v3", data)

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

    def corporate_integrated_filing(self, index=None, symbol=None, issuer=None,
                                     period_ended=None, from_date=None, to_date=None,
                                     filing_type="Integrated Filing- Financials",
                                     page=1, size=20):
        """
        Returns corporate integrated filing results from NSE.
        (https://www.nseindia.com/companies-listing/corporate-filings-integrated-filing)

        Args:
            index:       Market segment - 'equities', 'sme', etc. (optional)
            symbol:      Stock symbol e.g. 'DIXON' (optional)
            issuer:      Full company name e.g. 'Dixon Technologies (India) Limited' (optional)
            period_ended: Period filter e.g. 'all' or a specific period string (optional)
            from_date:   datetime.date - start date filter (optional, requires to_date)
            to_date:     datetime.date - end date filter (optional, requires from_date)
            filing_type: Type of filing (default: 'Integrated Filing- Financials')
            page:        Page number for pagination (default: 1)
            size:        Number of results per page (default: 20)
        """
        payload = {"type": filing_type, "page": page, "size": size}

        if index:
            payload["index"] = index
        if symbol:
            payload["symbol"] = symbol
        if issuer:
            payload["issuer"] = issuer
        if period_ended:
            payload["period_ended"] = period_ended
        if from_date and to_date:
            payload["from_date"] = from_date.strftime("%d-%m-%Y")
            payload["to_date"] = to_date.strftime("%d-%m-%Y")
        elif from_date or to_date:
            raise Exception("Please provide both from_date and to_date")

        return self.get("integrated_filing", payload)

    @live_cache
    def symbol_meta(self, symbol):
        """Fetch metadata for a symbol (FNO eligibility, delisting status, market type, etc.).

        Args:
            symbol: NSE stock symbol e.g. 'HDFCBANK'

        Returns:
            Dict with keys: symbol, companyName, activeSeries, isFNOSec, isCASec,
                            isSLBSec, isDebtSec, isETFSec, isDelisted, isin, marketType, etc.
        """
        return self._get_nextapi("getMetaData", symbol=symbol)

    @live_cache
    def symbol_name(self, symbol):
        """Fetch company name for a symbol.

        Args:
            symbol: NSE stock symbol e.g. 'HDFCBANK'

        Returns:
            Dict with keys: symbol, companyName
        """
        return self._get_nextapi("getSymbolName", symbol=symbol)

    @live_cache
    def top_stocks(self):
        """Fetch top gainers, losers, most active stocks by value/volume, 52-week highs/lows.

        Returns:
            Dict with keys: topGainers, topLoosers, mostActiveValue, mostActiveVolume,
                            volumeSpurtsValue, etfWatchValue, fiftyTwoWeekHigh, fiftyTwoWeekLow, timestamp
        """
        return self._get_nextapi("getTopTenStock")

    @live_cache
    def block_deal_session(self):
        """Fetch current block deal session status and deals.

        Returns:
            Dict with key: data (list of block deals)
        """
        return self._get_nextapi("getBlockDealSession")

    @live_cache
    def reg_details(self, symbol):
        """Fetch regulatory/compliance details for a symbol.

        Args:
            symbol: NSE stock symbol e.g. 'HDFCBANK'

        Returns:
            List of regulatory detail records
        """
        return self._get_nextapi("getRegDetails", symbol=symbol)

    @live_cache
    def symbol_chart_data(self, symbol, series="EQ", days="1D"):
        """Fetch intraday or historical chart data for a symbol.

        Args:
            symbol: NSE stock symbol e.g. 'HDFCBANK'
            series: Trading series (default 'EQ'). Appended as suffix to form the chart identifier.
            days:   Time period for chart data (default '1D')

        Returns:
            Dict with keys: identifier, name, grapthData, closePrice
        """
        return self._get_nextapi("getSymbolChartData", symbol=symbol + series + "N", days=days)

    @live_cache
    def yearwise_data(self, symbol, series="EQ"):
        """Fetch year-wise price/volume summary for a symbol.

        Args:
            symbol: NSE stock symbol e.g. 'HDFCBANK'
            series: Trading series (default 'EQ'). Appended as suffix to form the identifier.

        Returns:
            List of year-wise data records
        """
        return self._get_nextapi("getYearwiseData", symbol=symbol + series + "N")

    @live_cache
    def index_list(self, symbol):
        """Fetch list of indices the symbol is a constituent of.

        Args:
            symbol: NSE stock symbol e.g. 'HDFCBANK'

        Returns:
            List of index names
        """
        return self._get_nextapi("getIndexList", symbol=symbol)

    @live_cache
    def quote_index_data(self):
        """Fetch live quote data for all major indices.

        Returns:
            List of index quote records
        """
        return self._get_nextapi("getQuoteIndexData")

    def corporate_announcements(self, segment='equities', from_date=None, to_date=None, symbol=None):
        """
            This function returns the corporate annoucements 
            (https://www.nseindia.com/companies-listing/corporate-filings-announcements)
        """

        #from_date: 02-12-2024
        #to_date: 06-12-2024
        #symbol: 
        payload = {"index": segment}

        if from_date and to_date:
            payload['from_date'] = from_date.strftime("%d-%m-%Y")
            payload['to_date']   = to_date.strftime("%d-%m-%Y")
        elif from_date or to_date:
            raise Exception("Please provide both from_date and to_date")
        if symbol:
            payload['symbol'] = symbol
        return self.get("corporate_announcements", payload)

