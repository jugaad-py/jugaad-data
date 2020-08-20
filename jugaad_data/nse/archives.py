from datetime import datetime, date
import os
import io
import csv
import zipfile
import requests

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
    base_url = "https://archives.nseindia.com"
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
    s = requests.Session()
    h = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        "accept-encoding": "gzip, deflate, br",
        "accept":
"""text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9""",
        
}
    s.headers.update(h)
    _routes = {
            "bhavcopy": "/content/historical/EQUITIES/{yyyy}/{MMM}/cm{dd}{MMM}{yyyy}bhav.csv.zip",
            "bhavcopy_full": "/products/content/sec_bhavdata_full_{dd}{mm}{yyyy}.csv",
            "bulk_deals": "/content/equities/bulk.csv",
            "bhavcopy_fo": "/content/historical/DERIVATIVES/{yyyy}/{MMM}/fo{dd}{MMM}{yyyy}bhav.csv.zip"
        }
    
    
    def get(self, rout, **params):
        url = self.base_url + self._routes[rout].format(**params)
        self.r = self.s.get(url, timeout=self.timeout)
        return self.r
    
    @unzip
    def bhavcopy_raw(self, dt):
        """Downloads raw bhavcopy text for a specific date"""
        dd = dt.strftime('%d')
        MMM = dt.strftime('%b').upper()
        yyyy = dt.year
        r = self.get("bhavcopy", yyyy=yyyy, MMM=MMM, dd=dd)
        return r.content
    
    def bhavcopy_save(self, dt, dest, skip_if_present=True):
        """Downloads and saves raw bhavcopy csv file for a specific date"""
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
        r = self.get("bhavcopy_full", yyyy=yyyy, mm=mm, dd=dd)
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
    
    def bhavcopy_fo_save(self, dt, dest, skip_if_present):
        """ Saves Derivatives Bhavcopy to a directory """
        fmt = "fo%d%b%Ybhav.csv"
        fname = os.path.join(dest, dt.strftime(fmt))
        if os.path.isfile(fname) and skip_if_present:
            return fname
        text = self.bhavcopy_fo_raw(dt)
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





if __name__ == "__main__":

    url = "https://archives.nseindia.com/content/historical/EQUITIES/2020/AUG/cm12AUG2020bhav.csv.zip"
    d = requests.get(url, stream=True, timeout=1)
    for chunk in d.iter_content(chunk_size=1024):
        print("Received")
        print(len(chunk))








