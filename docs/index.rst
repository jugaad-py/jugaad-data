Introduction
============

``jugad-data`` is a library to fetch live as well as historical stock data. The library supports below functionalities-

- Download bhavcopy for stocks, index and derivatives
- Download historical stock data
- Download historical derivatives data
- Fetch live quotes for stocks and derivatives
- Fetch live index and turnover data
- Fetch option chains

Currently the library supports NSE.

Documentation and Resources
===========================

Detailed documentation: https://marketsetup.in/documentation/jugaad-data/

Example usage: https://marketsetup.in/tags/jugaad-data/

Installation
============

``pip install jugaad-data``


Quick Start
===========

.. code-block:: python

        from datetime import date
        from jugaad_data.nse import bhavcopy_save, bhavcopy_fo_save

        # Download bhavcopy
        bhavcopy_save(date(2020,1,1), "/path/to/directory")

        # Download bhavcopy for futures and options
        bhavcopy_fo_save(date(2020,1,1), "/path/to/directory")

        # Download stock data to pandas dataframe
        from jugaad_data.nse import stock_df
        df = stock_df(symbol="SBIN", from_date=date(2020,1,1),
                to_date=date(2020,1,30), series="EQ")
