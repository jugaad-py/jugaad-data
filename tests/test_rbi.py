from jugaad_data.rbi import RBI
import pytest

def test_current_rates():
    r = RBI()
    rates = r.current_rates()
    assert '91 day T-bills' in rates
    assert 'Policy Repo Rate' in rates
    assert 'Savings Deposit Rate' in rates
    # Below should not raise exception
    val = float(rates['91 day T-bills'].replace('%',""))
