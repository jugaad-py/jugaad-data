from datetime import date
from jugaad_data.holidays import holidays


def test_holidays():
    # Check for random holiday
    assert date(2018,11,8) in holidays()
    assert date(2020,12,25) in holidays(year=2020)
    assert date(2020,12,25) in holidays(year=2020)
    assert date(2020,11,30) in holidays(year=2020)
    assert date(2018,11,8) not in holidays(year=2020) 
    assert date(2020,12,25) in holidays(year=2020, month=12)
    assert date(2020,11,30) not in holidays(year=2020, month=12)


def test_holidays_2026():
    # Check a few 2026 holidays from the NSE holiday list
    assert date(2026,1,26) in holidays(year=2026)
    assert date(2026,4,3) in holidays(year=2026)
    assert date(2026,10,2) in holidays(year=2026)
    assert date(2026,12,25) in holidays(year=2026)
    assert date(2026,12,25) in holidays(year=2026, month=12)
    assert date(2026,1,26) not in holidays(year=2026, month=12)
    # All 16 holidays from the 2026 NSE list are present
    assert len(holidays(year=2026)) == 16
