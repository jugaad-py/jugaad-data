"""
    Implements BSE live data fetch functionality
"""
from datetime import datetime
from requests import Session
from ..util import live_cache


class BSELive:
    time_out = 5
    base_url = "https://api.bseindia.com/BseIndiaAPI/api"
    page_url = "https://www.bseindia.com/corporates/ann.html"
    attachment_base_url = "https://www.bseindia.com/xml-data/corpfiling/AttachLive"
    
    _routes = {
        "corporate_announcements": "/AnnSubCategoryGetData/w",
        "scrip_list": "/ListofScripData/w"
    }
    
    def __init__(self):
        self.s = Session()
        h = {
            "Host": "api.bseindia.com",
            "Referer": "https://www.bseindia.com/corporates/ann.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
        self.s.headers.update(h)
        # Note: Skip visiting the main page as it returns 403
        # The API works without this step

    def get(self, route, payload={}):
        url = self.base_url + self._routes[route]
        r = self.s.get(url, params=payload)
        return r.json()

    @live_cache
    def corporate_announcements(self, scrip_code=None, category="Result", subcategory="Financial+Results", 
                              from_date=None, to_date=None, page_no=1, search_type="P", 
                              announcement_type="C"):
        """
        Fetch corporate announcements from BSE
        
        Args:
            scrip_code (int): BSE scrip code (e.g., 532174 for ICICI Bank)
            category (str): Category filter (default: "Result")
            subcategory (str): Subcategory filter (default: "Financial+Results")
            from_date (datetime): Start date for filtering announcements
            to_date (datetime): End date for filtering announcements  
            page_no (int): Page number for pagination (default: 1)
            search_type (str): Search type (default: "P")
            announcement_type (str): Type of announcement (default: "C")
            
        Returns:
            dict: Response containing announcement data with Table and Table1 keys
            
        Example:
            bse = BSELive()
            # Get ICICI Bank announcements
            announcements = bse.corporate_announcements(
                scrip_code=532174,
                from_date=datetime(2025, 9, 16),
                to_date=datetime(2025, 11, 3)
            )
        """
        # Start with required parameters only
        payload = {
            "pageno": page_no,
            "strType": announcement_type,  # Required parameter
            "strSearch": search_type,      # Required parameter
        }
        
        # Add optional filters only if specified
        if category and category != "Result":  # Don't filter by default category
            payload["strCat"] = category
            
        if subcategory and subcategory != "Financial+Results":  # Don't filter by default subcategory
            payload["subcategory"] = subcategory
        
        if scrip_code:
            payload["strScrip"] = scrip_code
            
        if from_date:
            payload["strPrevDate"] = from_date.strftime("%Y%m%d")
            
        if to_date:
            payload["strToDate"] = to_date.strftime("%Y%m%d")
            
        return self.get("corporate_announcements", payload)

    def get_attachment_url(self, attachment_name):
        """
        Construct the full URL for downloading announcement attachments
        
        Args:
            attachment_name (str): The attachment filename from announcement data
            
        Returns:
            str: Full URL for downloading the attachment
            
        Example:
            bse = BSELive()
            announcements = bse.corporate_announcements(scrip_code=532174)
            for announcement in announcements.get("Table", []):
                if announcement.get("ATTACHMENTNAME"):
                    attachment_url = bse.get_attachment_url(announcement["ATTACHMENTNAME"])
                    print(f"Download URL: {attachment_url}")
        """
        if not attachment_name:
            return None
        return f"{self.attachment_base_url}/{attachment_name}"

    def get_announcement_with_urls(self, scrip_code=None, category="Result", 
                                 subcategory="Financial+Results", from_date=None, 
                                 to_date=None, page_no=1, search_type="P", 
                                 announcement_type="C"):
        """
        Fetch corporate announcements with attachment URLs included
        
        This is a convenience method that fetches announcements and automatically
        adds the full attachment URLs to each announcement record.
        
        Returns:
            dict: Response with announcement data including 'attachment_url' field
        """
        result = self.corporate_announcements(
            scrip_code=scrip_code,
            category=category,
            subcategory=subcategory,
            from_date=from_date,
            to_date=to_date,
            page_no=page_no,
            search_type=search_type,
            announcement_type=announcement_type
        )
        
        # Add attachment URLs to each announcement
        if "Table" in result:
            for announcement in result["Table"]:
                attachment_name = announcement.get("ATTACHMENTNAME")
                if attachment_name:
                    announcement["attachment_url"] = self.get_attachment_url(attachment_name)
                    # Calculate file size in human readable format
                    file_size = announcement.get("Fld_Attachsize")
                    if file_size:
                        if file_size > 99999:
                            announcement["file_size_formatted"] = f"{file_size/1048576:.2f} MB"
                        else:
                            announcement["file_size_formatted"] = f"{file_size/1024:.2f} KB"
                else:
                    announcement["attachment_url"] = None
                    announcement["file_size_formatted"] = None
        
        return result

    @live_cache
    def get_scrip_list(self, group=None, segment="Equity", status=None):
        """
        Fetch the list of all scrips (stocks) available on BSE
        
        Args:
            group (str): Group filter (e.g., "A", "B", "X", etc.)
            segment (str): Market segment (default: "Equity")
            status (str): Status filter ("Active", "Delisted", etc.)
            
        Returns:
            list: List of scrip dictionaries containing scrip codes, symbols, and details
            
        Example:
            bse = BSELive()
            all_scrips = bse.get_scrip_list()
            active_scrips = bse.get_scrip_list(status="Active")
            group_a_scrips = bse.get_scrip_list(group="A", status="Active")
        """
        payload = {
            "segment": segment
        }
        
        if group:
            payload["Group"] = group
            
        if status:
            payload["status"] = status
            
        return self.get("scrip_list", payload)

    def symbol_to_scrip_code(self, symbol):
        """
        Convert a BSE symbol (scrip_id) to scrip code
        
        Args:
            symbol (str): BSE symbol/scrip_id (e.g., "ICICIBANK", "TCS", "RELIANCE")
            
        Returns:
            str: BSE scrip code (e.g., "532174" for ICICIBANK)
            None: If symbol not found
            
        Example:
            bse = BSELive()
            scrip_code = bse.symbol_to_scrip_code("ICICIBANK")
            print(scrip_code)  # Output: "532174"
        """
        if not hasattr(self, '_scrip_cache'):
            # Cache the scrip list for faster lookups
            self._scrip_cache = {}
            scrip_list = self.get_scrip_list(status="Active")
            for scrip in scrip_list:
                scrip_id = scrip.get('scrip_id', '').upper()
                scrip_code = scrip.get('SCRIP_CD')
                if scrip_id and scrip_code:
                    self._scrip_cache[scrip_id] = scrip_code
        
        return self._scrip_cache.get(symbol.upper())

    def scrip_code_to_symbol(self, scrip_code):
        """
        Convert a BSE scrip code to symbol (scrip_id)
        
        Args:
            scrip_code (str or int): BSE scrip code (e.g., "532174" or 532174)
            
        Returns:
            str: BSE symbol/scrip_id (e.g., "ICICIBANK")
            None: If scrip code not found
            
        Example:
            bse = BSELive()
            symbol = bse.scrip_code_to_symbol("532174")
            print(symbol)  # Output: "ICICIBANK"
        """
        if not hasattr(self, '_reverse_scrip_cache'):
            # Cache the reverse mapping
            self._reverse_scrip_cache = {}
            scrip_list = self.get_scrip_list(status="Active")
            for scrip in scrip_list:
                scrip_id = scrip.get('scrip_id', '')
                scrip_code_val = scrip.get('SCRIP_CD')
                if scrip_id and scrip_code_val:
                    # Store with original case for scrip_id, but use scrip_code as string
                    self._reverse_scrip_cache[str(scrip_code_val)] = scrip_id.upper()
        
        return self._reverse_scrip_cache.get(str(scrip_code))

    def get_scrip_info(self, symbol_or_code):
        """
        Get detailed information about a scrip by symbol or code
        
        Args:
            symbol_or_code (str): BSE symbol (e.g., "ICICIBANK") or scrip code (e.g., "532174")
            
        Returns:
            dict: Complete scrip information including name, ISIN, market cap, etc.
            None: If not found
            
        Example:
            bse = BSELive()
            info = bse.get_scrip_info("ICICIBANK")
            print(info['Scrip_Name'])  # Output: "ICICI Bank Ltd"
            print(info['ISIN_NUMBER'])  # Output: ISIN number
        """
        scrip_list = self.get_scrip_list(status="Active")
        
        # Try to find by symbol first
        for scrip in scrip_list:
            if scrip.get('scrip_id', '').upper() == symbol_or_code.upper():
                return scrip
                
        # Try to find by scrip code
        for scrip in scrip_list:
            if scrip.get('SCRIP_CD') == str(symbol_or_code):
                return scrip
                
        return None

    def corporate_announcements_by_symbol(self, symbol, category="Result", 
                                        subcategory="Financial+Results", from_date=None, 
                                        to_date=None, page_no=1, search_type="P", 
                                        announcement_type="C"):
        """
        Fetch corporate announcements using BSE symbol instead of scrip code
        
        This is a convenience method that converts the symbol to scrip code automatically
        
        Args:
            symbol (str): BSE symbol/scrip_id (e.g., "ICICIBANK", "TCS", "RELIANCE")
            Other parameters: Same as corporate_announcements method
            
        Returns:
            dict: Response containing announcement data
            
        Example:
            bse = BSELive()
            announcements = bse.corporate_announcements_by_symbol(
                symbol="ICICIBANK",
                from_date=datetime(2024, 10, 1),
                to_date=datetime(2024, 10, 31)
            )
        """
        scrip_code = self.symbol_to_scrip_code(symbol)
        if not scrip_code:
            raise ValueError(f"Symbol '{symbol}' not found in BSE scrip list")
            
        return self.corporate_announcements(
            scrip_code=int(scrip_code),
            category=category,
            subcategory=subcategory,
            from_date=from_date,
            to_date=to_date,
            page_no=page_no,
            search_type=search_type,
            announcement_type=announcement_type
        )


if __name__ == "__main__":
    # Example usage
    from datetime import datetime
    
    bse = BSELive()
    print("BSE Live Corporate Announcements Demo")
    print("=" * 40)
    
    # Test 1: Symbol to scrip code conversion
    print("1. Testing symbol/scrip code conversions:")
    test_symbols = ["ICICIBANK", "TCS", "RELIANCE"]
    for symbol in test_symbols:
        scrip_code = bse.symbol_to_scrip_code(symbol)
        reverse_symbol = bse.scrip_code_to_symbol(scrip_code) if scrip_code else None
        print(f"   {symbol} <-> {scrip_code} <-> {reverse_symbol}")
    
    # Test 2: Get scrip list info
    print("\n2. Testing scrip list functionality:")
    try:
        scrip_list = bse.get_scrip_list(status="Active")
        print(f"   Total active scrips: {len(scrip_list)}")
        
        # Get ICICI info
        icici_info = bse.get_scrip_info("ICICIBANK")
        if icici_info:
            print(f"   ICICI Bank: {icici_info.get('Scrip_Name')} (Group {icici_info.get('GROUP')})")
            print(f"   Market Cap: ₹{icici_info.get('Mktcap', 'N/A')} Cr")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Corporate announcements using symbol
    print("\n3. Testing corporate announcements by symbol:")
    try:
        result = bse.corporate_announcements_by_symbol("ICICIBANK")
        print(f"   ICICIBANK announcements: {len(result.get('Table', []))} records")
        print(f"   Total available: {result.get('Table1', [{}])[0].get('ROWCNT', 'N/A')}")
        
        if result.get('Table') and len(result['Table']) > 0:
            latest = result['Table'][0]
            print(f"   Latest: {latest.get('NEWSSUB', 'N/A')[:60]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Attachment URL generation
    print("\n4. Testing attachment URL generation:")
    sample_attachment = "dfccd0c5-3764-4e4a-8e52-55b6dcc5e7ae.pdf"
    url = bse.get_attachment_url(sample_attachment)
    print(f"   Sample attachment URL: {url}")
    
    # Test 5: Convenience method with URLs
    print("\n5. Testing convenience method with URLs:")
    try:
        result_with_urls = bse.get_announcement_with_urls(scrip_code=532174)
        print(f"   Records with URLs: {len(result_with_urls.get('Table', []))}")
        if result_with_urls.get('Table') and len(result_with_urls['Table']) > 0:
            record = result_with_urls['Table'][0]
            if record.get('attachment_url'):
                print(f"   Sample attachment: {record.get('attachment_url')}")
                print(f"   File size: {record.get('file_size_formatted', 'N/A')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\nDemo completed successfully!")
    print("\nKey Features:")
    print("• Convert between BSE symbols and scrip codes")
    print("• Get detailed company information")
    print("• Fetch corporate announcements by symbol or scrip code")
    print("• Automatic attachment URL generation")
    print("• Built-in caching for performance")