import os
import collections
import json
import pickle
import time
from datetime import datetime, timedelta, date
from concurrent.futures import ThreadPoolExecutor
import click
from appdirs import user_cache_dir

import calendar

import math

try:
    import numpy as np
except:
    np = None

def np_exception(function):
    def wrapper(*args, **kwargs):
        if not np:
            raise ModuleNotFoundError("Please install pandas and numpy using \n pip install pandas")
        return function(*args, **kwargs)

    return wrapper

@np_exception
def np_float(num):
    try:
        return np.float64(num)
    except:
        return np.nan

@np_exception
def np_date(dt):
    try:
        return np.datetime64(dt)
    except:
        pass

    try:
        dt = datetime.strptime(dt, "%d-%b-%Y").date()
        return np.datetime64(dt)
    except:
        pass

    try:
        dt = datetime.strptime(dt, "%d %b %Y").date()
        return np.datetime64(dt)
    except:
        pass



    return np.datetime64('nat') 

    
@np_exception
def np_int(num):
    try:
        return np.int64(num)
    except:
        return 0

def break_dates(from_date, to_date):
    if from_date.replace(day=1) == to_date.replace(day=1):
        return [(from_date, to_date)]
    date_ranges = []
    month_start = from_date
    month_end = month_start.replace(day=calendar.monthrange(month_start.year, from_date.month)[1])
    while(month_end < to_date):
        date_ranges.append((month_start, month_end))
        month_start = month_end + timedelta(days=1)
        month_end = month_start.replace(day=calendar.monthrange(month_start.year, month_start.month)[1])
        if month_end >= to_date:
            date_ranges.append((month_start, to_date))
    return date_ranges


def kw_to_fname(**kw):
    name = "-".join([str(kw[k]) for k in sorted(kw) if k != "self"])
    return name



def cached(app_name):
    """
        Note to self:
            This is a russian doll
            wrapper - actual caching mechanism
            _cached - actual decorator
            cached - wrapper around decorator to make 'app_name' dynamic
    """
    def _cached(function):
        def wrapper(*args, **kw):
            kw.update(zip(function.__code__.co_varnames, args))
            env_dir = os.environ.get("J_CACHE_DIR")
            if not env_dir:
                cache_dir = user_cache_dir(app_name, app_name)
            else:
                cache_dir = os.path.join(env_dir, app_name)

            file_name = kw_to_fname(**kw)
            path = os.path.join(cache_dir, file_name)
            if not os.path.isfile(path):    
                if not os.path.exists(cache_dir):
                    os.makedirs(cache_dir)
                j = function(**kw)
                with open(path, 'wb') as fp:
                    pickle.dump(j, fp)        
            else:
                with open(path, 'rb') as fp:
                    j = pickle.load(fp)
            return j
        return wrapper
    return _cached


def pool(function, params, use_threads=True, max_workers=2):
    if use_threads:
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            dfs = ex.map(function, *zip(*params))
    else:
        dfs = []
        for param in params:
            try:
                r = function(*param)
            except:
                raise 
            dfs.append(r)
    return dfs

def live_cache(app_name):
    """Caches the output for time_out specified. This is done in order to
    prevent hitting live quote requests to NSE too frequently. This wrapper
    will fetch the quote/live result first time and return the same result for
    any calls within 'time_out' seconds.

    Logic:
        key = concat of args
        try:
            cached_value = self._cache[key]
            if now - self._cache['tstamp'] < time_out
                return cached_value['value']
        except AttributeError: # _cache attribute has not been created yet
            self._cache = {}
        finally:
            val = fetch-new-value
            new_value = {'tstamp': now, 'value': val}
            self._cache[key] = new_value
            return val

    """
    def wrapper(self, *args, **kwargs):
        """Wrapper function which calls the function only after the timeout,
        otherwise returns value from the cache.

        """
        # Get key by just concating the list of args and kwargs values and hope
        # that it does not break the code :P 
        inputs =  [str(a) for a in args] + [str(kwargs[k]) for k in kwargs]
        key = app_name.__name__ + '-'.join(inputs)
        now = datetime.now()
        time_out = self.time_out
        try:
            cache_obj = self._cache[key]
            if now - cache_obj['timestamp'] < timedelta(seconds=time_out):
                return cache_obj['value']
        except:
            self._cache = {}
        value = app_name(self, *args, **kwargs)
        self._cache[key] = {'value': value, 'timestamp': now}
        return value

    return wrapper 

