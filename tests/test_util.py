import os
import math
import pickle
import pytest
from jugaad_data import util as ut
from datetime import date, datetime

from pyfakefs.fake_filesystem_unittest import TestCase
from appdirs import user_cache_dir

def test_break_dates():
    from_date = date(2000, 12, 14)
    to_date = date(2005, 1, 20)
    dates = ut.break_dates(from_date, to_date)
    assert from_date== dates[0][0]
    assert to_date == dates[-1][1]
    assert len(dates) ==  50

    from_date = date(2019, 1, 1)
    to_date = date(2020, 1, 31)
    dates = ut.break_dates(from_date, to_date)
    assert from_date == dates[0][0]
    assert to_date == dates[-1][1]
    assert len(dates) == 13

def test_np_float():
    assert 3.3 == pytest.approx(ut.np_float("3.3"))
    assert math.isnan(ut.np_float("-"))
    

def test_np_int():
    assert 3 == ut.np_int('3')
    assert 0 == ut.np_int('-')

def test_np_date():
    assert date(2020,1,1) == ut.np_date("2020-01-01")
    assert date(2020,7,30) == datetime.strptime("30-Jul-2020", "%d-%b-%Y").date()
    assert date(2020,7,30) == ut.np_date("30-Jul-2020")

def test_kw_to_fname():
    x = ut.kw_to_fname(self=[0], z='last', a='first')
    assert x == 'first-last'
    x = ut.kw_to_fname(z='last', a='first', self=[0])
    assert x == 'first-last'
    x = ut.kw_to_fname(self=[], symbol="SBIN", from_date=date(2020,1,1), to_date=date(2020,1,31))
    assert x == "2020-01-01-SBIN-2020-01-31"

def demo_for_pool(a, b):
    return (a + b)**2

class DemoForPool:
    def demo_for_pool(self, a, b):
        return (a + b)**2

    def pooled(self, params, use_threds):
        return ut.pool(self.demo_for_pool, params, use_threds)

def test_pool():
    for use_threads in [True, False]:
        params = [ (0, 1),
                    (1, 2),
                    (2, 3)]
        expected = [1, 9, 25]
        actual = ut.pool(demo_for_pool, params, use_threads)
        assert expected == list(actual)
        d = DemoForPool()
        actual = d.pooled(params, use_threads)
        assert expected == list(actual)




@ut.cached("testapp")
def demo_function(self, x, y):
    return {'x': x, 'y': y}

class DemoClass:
    @ut.cached("testapp")
    def demo_method(self, x, y):
        return {'x': x, 'y': y} 

@ut.cached("testapp")
def demo_crash(a, b):
    raise Exception("Terrible")

class TestCache(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_demo_function(self):
        # Check if function reeturns correct value
        x = demo_function([0], 'v1', 'v2')
        self.assertEqual(x, {'x': 'v1', 'y': 'v2'})
        # Check if path exists
        path = os.path.join(user_cache_dir("testapp"), 'v1-v2')
        self.assertTrue(os.path.isfile(path))
        # Next time it should read from cache, let us see if cache reading works
        # update the file with new values
        j = {'x': 'x1', 'y': 'y1'}
        with open(path, 'wb') as fp:
            pickle.dump(j, fp)
        # run the function
        x = demo_function([0], 'v1', 'v2')
        self.assertEqual(x, j)
    
    def test_demo_method(self):
        d = DemoClass()
        x = d.demo_method('v1', 'v2')
        self.assertEqual(x, {'x': 'v1', 'y': 'v2'})
        # Check if path exists
        path = os.path.join(user_cache_dir("testapp"), 'v1-v2')
        self.assertTrue(os.path.isfile(path))
        # Next time it should read from cache, let us see if cache reading works
        # update the file with new values
        j = {'x': 'x1', 'y': 'y1'}
        with open(path, 'wb') as fp:
            pickle.dump(j, fp)
        # run the function
        x = d.demo_method('v1', 'v2')
        self.assertEqual(x, j)
        
    def test_demo_crashed(self):
        with pytest.raises(Exception):
            demo_crashed('fiz', 'buzz')        
        demo_function([0], 'lorem', 'ipsem') 
        path = os.path.join(user_cache_dir("testapp"), 'lorem-ipsem')
        assert os.path.isfile(path)
        try:
            demo_crashed('buzz', 'fizz')
        except:
            pass
        path = os.path.join(user_cache_dir("testapp"), 'buzz-fizz')
        assert not os.path.isfile(path)
