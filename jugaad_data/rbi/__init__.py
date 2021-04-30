from requests import Session
from bs4 import BeautifulSoup



def tr_to_json(wrapper):
    trs = wrapper.find_all("tr")
    op = {}
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds) >= 2:
            key = tds[0].text.strip()
            val = tds[1].text.replace(':', '').replace('*','').replace('#', '').strip()
            
            op[key] = val
    return op



class RBI:
    base_url = "https://www.rbi.org.in/"

    def __init__(self):
        self.s = Session()
    
    def current_rates(self):
        r = self.s.get(self.base_url)
        
        bs = BeautifulSoup(r.text, "html.parser")
        wrapper = bs.find('div', {"id": "wrapper"})
        trs = wrapper.find_all('tr')
        return tr_to_json(wrapper)


