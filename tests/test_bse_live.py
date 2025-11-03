"""
Tests for BSE Live data functionality
"""
from jugaad_data.bse.live import BSELive
from datetime import date, datetime, timedelta
import pytest

def test_bse_live_initialization():
    """Test that BSELive class initializes properly"""
    bse = BSELive()
    assert bse is not None
    assert hasattr(bse, 'time_out')
    assert hasattr(bse, 'base_url')
    assert hasattr(bse, 'attachment_base_url')
    assert bse.time_out == 5
    assert "bseindia.com" in bse.base_url
    assert "bseindia.com" in bse.attachment_base_url

def test_get_attachment_url():
    """Test attachment URL generation without API calls"""
    bse = BSELive()
    
    # Test with valid attachment name
    attachment_name = "sample-attachment.pdf"
    url = bse.get_attachment_url(attachment_name)
    
    assert url is not None
    assert attachment_name in url
    assert "bseindia.com" in url
    assert "xml-data/corpfiling/AttachLive" in url
    
    # Test with None attachment
    url_none = bse.get_attachment_url(None)
    assert url_none is None
    
    # Test with empty string
    url_empty = bse.get_attachment_url("")
    assert url_empty is None

def test_corporate_announcements_basic():
    """Test basic corporate announcements functionality - single quick API call"""
    bse = BSELive()
    
    # Test with a very small date range to make it faster
    result = bse.corporate_announcements(
        scrip_code=532174,
        from_date=datetime(2024, 10, 1),
        to_date=datetime(2024, 10, 2)  # Just 2 days
    )
    
    # Check response structure
    assert isinstance(result, dict)
    assert "Table" in result
    assert "Table1" in result
    assert isinstance(result["Table"], list)
    assert isinstance(result["Table1"], list)

def test_get_announcement_with_urls():
    """Test convenience method that includes attachment URLs"""
    bse = BSELive()
    
    result = bse.get_announcement_with_urls(
        scrip_code=532174,
        from_date=datetime(2024, 10, 1),
        to_date=datetime(2024, 10, 2)  # Small date range
    )
    
    assert isinstance(result, dict)
    assert "Table" in result
    assert "Table1" in result
    
    # Check if announcements have attachment URLs added
    if result.get("Table") and len(result["Table"]) > 0:
        announcement = result["Table"][0]
        # Should have attachment_url field (even if None)
        assert "attachment_url" in announcement
        assert "file_size_formatted" in announcement

def test_get_scrip_list():
    """Test scrip list functionality"""
    bse = BSELive()
    
    # Test getting all active scrips
    scrip_list = bse.get_scrip_list(status="Active")
    assert isinstance(scrip_list, list)
    assert len(scrip_list) > 1000  # Should have many active scrips
    
    # Check structure of first scrip
    if len(scrip_list) > 0:
        scrip = scrip_list[0]
        assert "SCRIP_CD" in scrip
        assert "scrip_id" in scrip
        assert "Scrip_Name" in scrip

def test_symbol_conversions():
    """Test symbol to scrip code conversion and vice versa"""
    bse = BSELive()
    
    # Test symbol to scrip code
    icici_code = bse.symbol_to_scrip_code("ICICIBANK")
    assert icici_code == "532174"
    
    # Test scrip code to symbol
    icici_symbol = bse.scrip_code_to_symbol("532174")
    assert icici_symbol == "ICICIBANK"
    
    # Test round trip
    tcs_code = bse.symbol_to_scrip_code("TCS")
    assert tcs_code is not None
    tcs_symbol = bse.scrip_code_to_symbol(tcs_code)
    assert tcs_symbol == "TCS"
    
    # Test case insensitivity
    icici_code_lower = bse.symbol_to_scrip_code("icicibank")
    assert icici_code_lower == "532174"
    
    # Test non-existent symbol
    invalid_code = bse.symbol_to_scrip_code("NONEXISTENT")
    assert invalid_code is None

def test_get_scrip_info():
    """Test getting detailed scrip information"""
    bse = BSELive()
    
    # Test with symbol
    icici_info = bse.get_scrip_info("ICICIBANK")
    assert icici_info is not None
    assert icici_info["SCRIP_CD"] == "532174"
    assert "ICICI" in icici_info["Scrip_Name"]
    assert "ISIN_NUMBER" in icici_info
    
    # Test with scrip code
    icici_info_by_code = bse.get_scrip_info("532174")
    assert icici_info_by_code is not None
    assert icici_info_by_code["scrip_id"] == "ICICIBANK"
    
    # Test non-existent
    invalid_info = bse.get_scrip_info("NONEXISTENT")
    assert invalid_info is None

def test_corporate_announcements_by_symbol():
    """Test corporate announcements using symbol instead of scrip code"""
    bse = BSELive()
    
    # Test with valid symbol
    result = bse.corporate_announcements_by_symbol("ICICIBANK")
    assert isinstance(result, dict)
    assert "Table" in result
    assert "Table1" in result
    
    # Test with invalid symbol
    try:
        bse.corporate_announcements_by_symbol("NONEXISTENT")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "not found" in str(e)

if __name__ == "__main__":
    # Run tests individually for debugging
    print("Running BSE Live tests...")
    
    test_bse_live_initialization()
    print("✓ Initialization test passed")
    
    test_get_attachment_url()
    print("✓ Attachment URL test passed")
    
    try:
        test_corporate_announcements_basic()
        print("✓ Basic corporate announcements test passed")
    except Exception as e:
        print(f"✗ Basic corporate announcements test failed: {e}")
    
    try:
        test_get_announcement_with_urls()
        print("✓ Announcements with URLs test passed")
    except Exception as e:
        print(f"✗ Announcements with URLs test failed: {e}")
    
    print("BSE Live tests completed!")