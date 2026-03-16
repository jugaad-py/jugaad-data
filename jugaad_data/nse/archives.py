"""
    Implements functionality to download archival data such as Bhavcopy, bulk
    deals from NSE and NSEIndices website
"""
from datetime import datetime, date, timedelta
import os
import io
import csv
import zipfile
import requests
import pprint
import json


class NSEDailyReports:
    """Handles NSE Daily Reports API (available from Jul 8, 2024 onwards)
    
    This API provides access to the latest daily reports from NSE including
    the new Unified Distilled File Format (UDiff) for bhavcopy.
    
    API supports current day and previous day only. For historical data,
    use NSEArchives.full_bhavcopy_raw() instead.
    """
    
    api_url = "https://www.nseindia.com/api/daily-reports"
    base_url = "https://nsearchives.nseindia.com/"
    timeout = 4
    
    def __init__(self):
        self.s = requests.Session()
        h = {
            "user-agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36",
            "Sec-CH-UA": '"Google Chrome";v="134", "Chromium";v="134", "Not?A_Brand";v="99"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "DNT": "1",
            "accept-encoding": "gzip, deflate",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        }
        self.s.headers.update(h)
        self._cache = {}
    
    def get_daily_reports(self, segment="CM"):
        """Fetch daily reports metadata for a given segment (CM, FO, etc.)
        
        Args:
            segment (str): Market segment - CM (Capital Market), FO (Futures & Options), etc.
        
        Returns:
            dict: Response containing PreviousDay, CurrentDay, FutureDay lists with file metadata
        
        Raises:
            requests.RequestException: If API call fails
        """
        url = f"{self.api_url}?key={segment}"
        try:
            r = self.s.get(url, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                f"Failed to fetch daily reports for segment {segment}: {str(e)}"
            ) from e
    
    def find_file(self, file_key, trading_date=None, segment="CM"):
        """Find a file by its fileKey in daily reports
        
        Args:
            file_key (str): The fileKey to search for (e.g., 'CM-UDIFF-BHAVCOPY-CSV')
            trading_date (date, optional): Specific date to search. If None, searches
                                           current and previous day from API
            segment (str): Market segment
        
        Returns:
            dict: File metadata including fileActlName, filePath, tradingDate
            
        Raises:
            ValueError: If file not found
        """
        try:
            reports = self.get_daily_reports(segment)
        except Exception as e:
            raise ValueError(f"Could not fetch reports: {str(e)}") from e
        
        # Search in both current and previous day
        for day_list in [reports.get('CurrentDay', []), reports.get('PreviousDay', [])]:
            for file_item in day_list:
                if file_item.get('fileKey') == file_key:
                    if trading_date is None:
                        return file_item
                    # Check if trading date matches
                    file_trading_date = datetime.strptime(
                        file_item.get('tradingDate', ''), "%d-%b-%Y"
                    ).date()
                    if file_trading_date == trading_date:
                        return file_item
        
        raise ValueError(f"File {file_key} not found in daily reports")
    
    def download_file(self, file_key, trading_date=None, segment="CM"):
        """Download a file from daily reports
        
        Args:
            file_key (str): The fileKey to download
            trading_date (date, optional): Specific trading date to target
            segment (str): Market segment
        
        Returns:
            bytes: Raw file content
            
        Raises:
            ValueError: If file not found
            requests.RequestException: If download fails
        """
        file_info = self.find_file(file_key, trading_date, segment)
        
        url = f"{file_info['filePath']}{file_info['fileActlName']}"
        try:
            r = self.s.get(url, timeout=self.timeout)
            r.raise_for_status()
            return r.content
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                f"Failed to download {file_key}: {str(e)}"
            ) from e
    
    def list_available_files(self, segment="CM"):
        """List all available file types for a segment
        
        Args:
            segment (str): Market segment
            
        Returns:
            dict: Mapping of fileKey to display names with dates
        """
        try:
            reports = self.get_daily_reports(segment)
        except Exception as e:
            raise ValueError(f"Could not fetch reports: {str(e)}") from e
        
        files = {}
        for day_type in ['CurrentDay', 'PreviousDay']:
            for file_item in reports.get(day_type, []):
                key = file_item.get('fileKey')
                if key not in files:
                    files[key] = {
                        'displayName': file_item.get('displayName'),
                        'dates': []
                    }
                files[key]['dates'].append({
                    'date': file_item.get('tradingDate'),
                    'size': file_item.get('fileSize'),
                    'fileName': file_item.get('fileActlName')
                })
        
        return files


def unzip(function):
    
    def unzipper(*args, **kwargs):
        r = function(*args, **kwargs)
        fp = io.BytesIO(r)
        with zipfile.ZipFile(file=fp) as zf:
            fname = zf.namelist()[0]
            with zf.open(fname) as fp_bh:
                return fp_bh.read().decode('utf-8')
    return unzipper


class NSEArchives:
    base_url = "https://nsearchives.nseindia.com/"
    """Conventions
           d - 1, 12 (without leading zero)
          dd - 01, 21 (day of the month with leading zero)
          mm - 01, 12 (month with leading zero)
           m - 1, 12 (month without leading zero)
         MMM - JAN, DEC
          yy - 19, 20
        yyyy - 2020, 2030
    """
    timeout = 4 
    # Date when NSE switched to UDiff format (Unified Distilled File Format)
    udiff_start_date = date(2024, 7, 8)
       
    def __init__(self):
        self.s = requests.Session()
        h = {
            "user-agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36",
            "Sec-CH-UA": '"Google Chrome";v="134", "Chromium";v="134", "Not?A_Brand";v="99"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "DNT": "1",
            "accept-encoding": "gzip, deflate",
            "accept":
    """text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9""",
          
    }
        self.s.headers.update(h)
        self._routes = {
                "bhavcopy": "/content/historical/EQUITIES/{yyyy}/{MMM}/cm{dd}{MMM}{yyyy}bhav.csv.zip",
                "bhavcopy_full": "/products/content/sec_bhavdata_full_{dd}{mm}{yyyy}.csv",
                "bulk_deals": "/content/equities/bulk.csv",
                "bhavcopy_fo": "/content/historical/DERIVATIVES/{yyyy}/{MMM}/fo{dd}{MMM}{yyyy}bhav.csv.zip"
            }
        self.daily_reports = NSEDailyReports()
        
    def get(self, rout, **params):
        url = self.base_url + self._routes[rout].format(**params)
        self.r = self.s.get(url, timeout=self.timeout)
        return self.r
    
    
    def bhavcopy_raw(self, dt):
        """Downloads raw bhavcopy text for a specific date
        
        Uses hybrid approach:
        - For dates >= Jul 8, 2024: Attempts to fetch UDiff format from daily-reports API
        - For older dates or if API unavailable: Falls back to BHAVDATA-FULL format
        
        Note: UDiff format has different column structure than old format.
        Data is returned as-is without modification.
        
        Args:
            dt (date or datetime): Trading date
            
        Returns:
            str: CSV content with stock market data
            
        Raises:
            requests.RequestException: If download fails and no fallback available
        """
        if isinstance(dt, datetime):
            dt = dt.date()
        
        # For recent dates (>= Jul 8, 2024), try UDiff format from daily-reports API
        if dt >= self.udiff_start_date:
            try:
                file_content = self.daily_reports.download_file(
                    'CM-UDIFF-BHAVCOPY-CSV',
                    trading_date=dt,
                    segment='CM'
                )
                # Extract from ZIP
                fp = io.BytesIO(file_content)
                with zipfile.ZipFile(file=fp) as zf:
                    fname = zf.namelist()[0]
                    with zf.open(fname) as fp_csv:
                        return fp_csv.read().decode('utf-8')
            except (ValueError, requests.RequestException, zipfile.BadZipFile) as e:
                # Fall back to BHAVDATA-FULL
                pass
        
        # Fallback: Use BHAVDATA-FULL (available for all historical dates)
        return self.full_bhavcopy_raw(dt)
    
    
    def bhavcopy_save(self, dt, dest, skip_if_present=True):
        """Downloads and saves raw bhavcopy csv file for a specific date
        
        Args:
            dt (date or datetime): Trading date
            dest (str): Destination directory path
            skip_if_present (bool): Skip download if file already exists
            
        Returns:
            str: Path to saved file
        """
        if isinstance(dt, datetime):
            dt = dt.date()
            
        fmt = "cm%d%b%Ybhav.csv"
        fname = os.path.join(dest, dt.strftime(fmt))
        if os.path.isfile(fname) and skip_if_present:
            return fname
        text = self.bhavcopy_raw(dt)
        with open(fname, 'w') as fp:
            fp.write(text)
            return fname

    def full_bhavcopy_raw(self, dt):
        """Downloads full raw bhavcopy text for a specific date"""
        
        dd = dt.strftime('%d')
        mm = dt.strftime('%m')
        yyyy = dt.year
        try:
            r = self.get("bhavcopy_full", yyyy=yyyy, mm=mm, dd=dd)
        except requests.exceptions.ReadTimeout:
            if dt < date(2020,1,1): # Receiving timeouts for dates before 2020
                raise requests.exceptions.ReadTimeout("""Either request timed
                                                      out or full bhavcopy file is
                                                      not available for given
                                                      date (2019 and prior
                                                      dates)""") 
        return r.text

    def full_bhavcopy_save(self, dt, dest, skip_if_present=True):
        fmt = "sec_bhavdata_full_%d%b%Ybhav.csv"
        fname = os.path.join(dest, dt.strftime(fmt))
        if os.path.isfile(fname) and skip_if_present:
            return fname
        if os.path.isfile(fname):
            return fname
        text = self.full_bhavcopy_raw(dt)
        with open(fname, 'w') as fp:
            fp.write(text)
        return fname

    def bulk_deals_raw(self):
        r = self.get("bulk_deals")
        return r.text
    
    def bulk_deals_save(self, fname):
        text = self.bulk_deals_raw()
        with open(fname, 'w') as fp:
            fp.write(text)

    @unzip
    def bhavcopy_fo_raw(self, dt):
        """Downloads raw bhavcopy text for a specific date"""
        dd = dt.strftime('%d')
        MMM = dt.strftime('%b').upper()
        yyyy = dt.year
        r = self.get("bhavcopy_fo", yyyy=yyyy, MMM=MMM, dd=dd)
        return r.content
    
    def bhavcopy_fo_save(self, dt, dest, skip_if_present=True):
        """ Saves Derivatives Bhavcopy to a directory """
        fmt = "fo%d%b%Ybhav.csv"
        fname = os.path.join(dest, dt.strftime(fmt))
        if os.path.isfile(fname) and skip_if_present:
            return fname
        text = self.bhavcopy_fo_raw(dt)
        with open(fname, 'w') as fp:
            fp.write(text)
        return fname
    
    def download_report(self, file_key, dest, segment='CM', skip_if_present=True):
        """Download a specific report from NSE daily-reports API
        
        Provides access to all available NSE reports (39+ types) from the daily-reports API.
        Downloads files for current day and previous trading day.
        
        Available file keys include:
        - CM-UDIFF-BHAVCOPY-CSV: UDiff Common Bhavcopy (zip)
        - CM-BHAVDATA-FULL: Full Bhavcopy with delivery data (csv)
        - CM-BHAVCOPY-DAT: Bhavcopy in DAT format
        - CM-VOLATILITY: Daily Volatility (csv)
        - CM-BULK-DEAL: Bulk Deals (csv)
        - CM-BLOCK-DEAL: Block Deals (csv)
        - CM-SHORT-SELLING: Short Selling data (csv)
        - CM-CIRCUIT: Circuit breaker updates (csv)
        - And many more...
        
        Args:
            file_key (str): The fileKey identifying the report type
            dest (str): Destination directory path
            segment (str): Market segment (CM, FO, etc.). Default: 'CM'
            skip_if_present (bool): Skip download if file already exists
            
        Returns:
            dict: Downloaded file information including:
                - 'file_path': Path to saved file
                - 'file_name': Actual file name from NSE
                - 'trading_date': Trading date of the report
                - 'size': File size
                
        Raises:
            ValueError: If file_key not found in available reports
            requests.RequestException: If download fails
            
        Examples:
            >>> from jugaad_data.nse import NSEArchives
            >>> nse = NSEArchives()
            >>> info = nse.download_report('CM-VOLATILITY', '/path/to/save')
            >>> print(info['file_path'])
        """
        try:
            file_info = self.daily_reports.find_file(file_key, segment=segment)
        except ValueError as e:
            raise ValueError(
                f"Report '{file_key}' not found. Use list_available_reports() to see options."
            ) from e
        
        # Create destination if needed
        os.makedirs(dest, exist_ok=True)
        
        file_name = file_info['fileActlName']
        file_path = os.path.join(dest, file_name)
        
        if os.path.isfile(file_path) and skip_if_present:
            return {
                'file_path': file_path,
                'file_name': file_name,
                'trading_date': file_info.get('tradingDate'),
                'size': file_info.get('fileSize'),
                'cached': True
            }
        
        # Download the file
        try:
            content = self.daily_reports.download_file(file_key, segment=segment)
            with open(file_path, 'wb') as fp:
                fp.write(content)
        except requests.RequestException as e:
            raise requests.RequestException(
                f"Failed to download {file_key}: {str(e)}"
            ) from e
        
        return {
            'file_path': file_path,
            'file_name': file_name,
            'trading_date': file_info.get('tradingDate'),
            'size': file_info.get('fileSize'),
            'cached': False
        }
    
    def list_available_reports(self, segment='CM'):
        """List all available reports for a market segment
        
        Args:
            segment (str): Market segment (CM, FO, etc.). Default: 'CM'
            
        Returns:
            dict: Available reports with display names and available dates
            
        Examples:
            >>> from jugaad_data.nse import NSEArchives
            >>> nse = NSEArchives()
            >>> reports = nse.list_available_reports()
            >>> for key, info in reports.items():
            ...     print(f"{key}: {info['displayName']}")
        """
        return self.daily_reports.list_available_files(segment)

class NSEIndicesArchives(NSEArchives):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.niftyindices.com"
        self._routes = { 
                "bhavcopy": "/Daily_Snapshot/ind_close_all_{dd}{mm}{yyyy}.csv"
        }
        self.h = {
        "Host": "www.niftyindices.com",
        "Referer": "https://www.nseindia.com",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36",
        "Sec-CH-UA": '"Google Chrome";v="134", "Chromium";v="134", "Not?A_Brand";v="99"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "DNT": "1",
       "Accept": "*/*",
       "Accept-Encoding": "gzip, deflate",
       "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
       "Cache-Control": "no-cache",
       "Connection": "keep-alive",
    }

        self.s.headers.update(self.h)

    def bhavcopy_index_raw(self, dt):
        """Downloads raw index bhavcopy text for a specific date"""
        dd = dt.strftime('%d')
        mm = dt.strftime('%m').upper()
        yyyy = dt.year
        r = self.get("bhavcopy", yyyy=yyyy, mm=mm, dd=dd)
        return r.text
   
    def bhavcopy_index_save(self, dt, dest, skip_if_present=True):
        """Downloads and saves index bhavcopy csv for a specific date"""
        fmt = "ind_close_all_%d%m%Y.csv"
        fname = os.path.join(dest, dt.strftime(fmt))
        if os.path.isfile(fname) and skip_if_present:
            return fname
        text = self.bhavcopy_index_raw(dt)
        with open(fname, 'w') as fp:
            fp.write(text)
        return fname

a = NSEArchives()
bhavcopy_raw = a.bhavcopy_raw
bhavcopy_save = a.bhavcopy_save
full_bhavcopy_raw = a.full_bhavcopy_raw
full_bhavcopy_save = a.full_bhavcopy_save
bhavcopy_fo_raw = a.bhavcopy_fo_raw
bhavcopy_fo_save = a.bhavcopy_fo_save
ia = NSEIndicesArchives()
bhavcopy_index_raw = ia.bhavcopy_index_raw
bhavcopy_index_save = ia.bhavcopy_index_save

def expiry_dates(dt, instrument_type="", symbol="", contracts=0):
    txt = bhavcopy_fo_raw(dt)
    rows = txt.split("\n")
    rows.pop(0) # Remove headers
    if len(rows[-1].split(',')) <= 10:
        rows.pop(-1) # Remove last blank row
    cells = [row.split(',') for row in rows]
    if instrument_type:
        cells = filter(lambda x: x[0]==instrument_type, cells)
    if symbol:
        cells = filter(lambda x: x[1] == symbol, cells)
    
    cells = filter(lambda x: int(x[10])>contracts, cells)
    
    dts_txt = [row[2] for row in cells]
    dts = [datetime.strptime(d, "%d-%b-%Y").date() for d in dts_txt]
    return list(set(dts))



if __name__ == "__main__":

    url = "https://www.niftyindices.com/Daily_Snapshot/ind_close_all_20082020.csv"
    headers = {
        "Host": "www.niftyindices.com",
        "Referer": "https://www.nseindia.com",
       "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36",
        "Sec-CH-UA": '"Google Chrome";v="134", "Chromium";v="134", "Not?A_Brand";v="99"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "DNT": "1",
       "Accept": "*/*",
       "Accept-Encoding": "gzip, deflate",
       "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
       "Cache-Control": "no-cache",
       "Connection": "keep-alive",
       }
    d = requests.get(url, stream=True, timeout=10, headers=headers, verify=False)
    for chunk in d.iter_content(chunk_size=1024):
        print("Received")
        print(len(chunk))


