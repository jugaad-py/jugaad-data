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
