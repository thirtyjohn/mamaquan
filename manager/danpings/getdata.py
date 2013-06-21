#coding:utf-8
from helpers.crawls import getUrl
from bs4 import BeautifulSoup
import re,traceback
from manager.models import danpings
from helpers.loggers import get_logger
from helpers.cpslinks import getSrcUrl
from helpers.utils import getMarketFromUrl
from helpers.b2c import factory


def factory(source):
    dpsource = Dpsource()
    if source == "smzdm":
        dpsource = Smzdm()
    return dpsource


class Dpsource:
    def __init__(self):
        self.url = None
        self.html = None
        self.dplist = list()
    def getNewlist(self):
        pass
    def getlist(self):
        pass
    def insert(self):
        print len(self.dplist)
        for dp in self.dplist:
            try:
                danpings.insertDpitem(dp)
            except:
                get_logger("general").debug(traceback.format_exc())


class Smzdm(Dpsource):
    def __init__(self):
        Dpsource.__init__(self)
        self.name = "smzdm"
        self.url = "http://www.smzdm.com/page/1"
        self.from_encoding = "gbk"
        self.comp_price = re.compile(u"(\d+)元")
        self.comp_price_en = re.compile(u"\$([0-9.]+)")
        self.comp_sourceid = re.compile(u"youhui/(\d+)")

    def getNewlist(self):
        resp = getUrl(self.url)
        if not resp:
            return
        self.html = resp.read()

    def getlist(self):
        if not self.html:
            return
        soup = BeautifulSoup(self.html,from_encoding=self.from_encoding)
        divs = soup.find_all("div","perContentBox")
        for div in divs:
            try:
                m = self.comp_sourceid.search(div.find("h2","con_title").find("a")["href"])
                if not m:
                    continue
                dp = danpings.Danping()
                dp.sourceid = m.group(1)
                dp.source = self.name
                if danpings.hasitem(dp.sourceid,dp.source):
                    continue
                title = div.find("h2","con_title").find("a").get_text() 
                pricetxt = div.find("h2","con_title").find("span","red").string if div.find("h2","con_title").find("span","red") else None
                if pricetxt:
                    dp.name = title.replace(pricetxt,"")
                    m = self.comp_price.search(pricetxt)
                    dp.price = float(m.group(1)) if m else None
                    if not dp.price:
                        m = self.comp_price_en.search(pricetxt)
                        if m:
                            dp.price = float(m.group(1))
                            dp.currency = 2
                dp.img = div.find("img","post_thumb_pic_main")["src"] 
                dp.desp = u"<p>"+div.find("p","p_excerpt").get_text()+ u"</p><p>" + div.find("p","p_detail").get_text()+ u"</p>"
                itemclasses = list()
                for cat in div.find("div","leftShowInfo").find_all("a",rel="category tag"):
                    itemclasses.append(cat.string)
                dp.itemclass = "$".join(itemclasses)
                dp.url = div.find("div","zhida").find("a")["href"] if div.find("div","zhida") else None
                if dp.url:
                    resp = getUrl(dp.url)
                    dp.redirecturl = resp.geturl() if resp else None
                if dp.redirecturl:
                    dp.srcurl = getSrcUrl(dp.redirecturl)
                if dp.srcurl:
                    dp.market = getMarketFromUrl(dp.srcurl)
                    b2c_item = factory(dp.market)
                    dp.itemid = b2c_item.getItemidFromUrl(dp.srcurl)
                self.dplist.append(dp)
            except:
                get_logger("general").debug(traceback.format_exc())


