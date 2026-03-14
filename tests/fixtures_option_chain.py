"""
Test fixtures for NSE live option chain data
"""

NIFTY_OPTION_CHAIN_MOCK = {
    "records": {
        "expiryDates": ["23-May-2026", "30-May-2026"],
        "data": [
            {
                "expiryDate": "23-May-2026",
                "pe": {
                    "strikePrice": 22800,
                    "expiryDate": "23-May-2026",
                    "optionType": "PE",
                    "bid": 12.5,
                    "ask": 13.5,
                    "lastPrice": 13.0,
                    "change": 0.5,
                    "pchangeVal": 3.85,
                    "bidQty": 150,
                    "askQty": 200,
                    "openInterest": 1000,
                    "impliedVolatility": 18.5,
                    "greeks": {
                        "vega": 0.02,
                        "theta": -0.08,
                        "rho": 2.5,
                        "gamma": 0.0002,
                        "delta": -0.35
                    }
                },
                "ce": {
                    "strikePrice": 22800,
                    "expiryDate": "23-May-2026",
                    "optionType": "CE",
                    "bid": 450.0,
                    "ask": 455.0,
                    "lastPrice": 452.5,
                    "change": -2.5,
                    "pchangeVal": -0.55,
                    "bidQty": 150,
                    "askQty": 200,
                    "openInterest": 1500,
                    "impliedVolatility": 20.5,
                    "greeks": {
                        "vega": 0.03,
                        "theta": -0.12,
                        "rho": -4.2,
                        "gamma": 0.0003,
                        "delta": 0.65
                    }
                }
            }
        ]
    },
    "filtered": {
        "expiryDate": "23-May-2026"
    }
}

RELIANCE_OPTION_CHAIN_MOCK = {
    "records": {
        "expiryDates": ["20-Mar-2026", "27-Mar-2026"],
        "data": [
            {
                "expiryDate": "20-Mar-2026",
                "pe": {
                    "strikePrice": 2800,
                    "expiryDate": "20-Mar-2026",
                    "optionType": "PE",
                    "bid": 22.5,
                    "ask": 23.5,
                    "lastPrice": 23.0,
                    "change": 1.5,
                    "pchangeVal": 6.98,
                    "bidQty": 50,
                    "askQty": 75,
                    "openInterest": 500,
                    "impliedVolatility": 25.5,
                    "greeks": {
                        "vega": 0.015,
                        "theta": -0.05,
                        "rho": 1.2,
                        "gamma": 0.0005,
                        "delta": -0.45
                    }
                },
                "ce": {
                    "strikePrice": 2800,
                    "expiryDate": "20-Mar-2026",
                    "optionType": "CE",
                    "bid": 78.0,
                    "ask": 82.0,
                    "lastPrice": 80.0,
                    "change": -1.0,
                    "pchangeVal": -1.23,
                    "bidQty": 50,
                    "askQty": 75,
                    "openInterest": 800,
                    "impliedVolatility": 28.5,
                    "greeks": {
                        "vega": 0.02,
                        "theta": -0.09,
                        "rho": -2.1,
                        "gamma": 0.0008,
                        "delta": 0.55
                    }
                }
            }
        ]
    },
    "filtered": {
        "expiryDate": "20-Mar-2026"
    }
}

USDINR_OPTION_CHAIN_MOCK = {
    "records": {
        "expiryDates": ["26-Mar-2026", "23-Apr-2026"],
        "data": [
            {
                "expiryDate": "26-Mar-2026",
                "pe": {
                    "strikePrice": 92.5,
                    "expiryDate": "26-Mar-2026",
                    "optionType": "PE",
                    "bid": 0.45,
                    "ask": 0.50,
                    "lastPrice": 0.48,
                    "change": 0.02,
                    "pchangeVal": 4.35,
                    "bidQty": 1000,
                    "askQty": 1500,
                    "openInterest": 5000,
                    "impliedVolatility": 12.5,
                    "greeks": {
                        "vega": 0.008,
                        "theta": -0.02,
                        "rho": 0.5,
                        "gamma": 0.0003,
                        "delta": -0.35
                    }
                },
                "ce": {
                    "strikePrice": 92.5,
                    "expiryDate": "26-Mar-2026",
                    "optionType": "CE",
                    "bid": 0.60,
                    "ask": 0.65,
                    "lastPrice": 0.62,
                    "change": -0.03,
                    "pchangeVal": -4.62,
                    "bidQty": 1000,
                    "askQty": 1500,
                    "openInterest": 6000,
                    "impliedVolatility": 14.5,
                    "greeks": {
                        "vega": 0.01,
                        "theta": -0.03,
                        "rho": -0.7,
                        "gamma": 0.0004,
                        "delta": 0.65
                    }
                }
            }
        ]
    },
    "filtered": {
        "expiryDate": "26-Mar-2026"
    }
}
