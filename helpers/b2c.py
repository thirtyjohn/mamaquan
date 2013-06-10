#coding:utf-8
from bs4 import BeautifulSoup,SoupStrainer
from helpers.crawls import getUrl
import re,urllib,json,bs4

class Item:
    def __init__(self):
        self.itemid = None
        self.name = None
        self.market = None 
        self.img = None
        self.price = None
        self.currency = None

def factory(market):
    b2c = B2c()
    if market == "jd":
        b2c = Jd()
    elif market == "zcn":
        b2c = Zcn()
    elif market == "dangdang":
        b2c = Dangdang()
    return b2c


class B2c:
    def __init__(self,itemid=None,itemhtml=None,listhtml=None):
        self.market = None
        self.itemid = None
        self.itemhtml = None
        self.listhtml = None

    def getlist(self):
        pass

    def getitem(self):
        pass

    def isZiyin(self):
        pass

    def getprize(self):
        pass

    def getSearchUrl(self,txt):
        pass

    def getItemUrl(self):
        pass

    def getSearchHtml(self,txt):
        url = self.getSearchUrl(txt)
        html = getUrl(url).read()
        return html

    def getItemHtml(self):
        url = self.getItemUrl()
        html = getUrl(url).read()
        return html



class Jd(B2c):
    
    def __init__(self,itemid=None,itemhtml=None,listhtml=None):
        B2c.__init__(self,itemid=None,itemhtml=None,listhtml=None)
        self.market = "jd"
        self.comp_Price = re.compile("\"p\":\"([0-9.]+)\"")
        self.comp_itemid = re.compile("/(\d+).html")

    def getlist(self):
        ss = SoupStrainer("ul" , "list-h clearfix")
        soup = BeautifulSoup(self.listhtml,parse_only=ss,from_encoding="gbk")
        lis = soup.find_all("li")
        itemlist = list()
        for li in lis:
            item = Item()
            item.market = self.market
            item.itemid = self.comp_itemid.search(li.find("div","p-name").a["href"]).group(1)
            item.name = li.find("div","p-name").a.get_text().strip()
            item.img = li.find("div","p-img").img["data-lazyload"]
            itemlist.append(item)
        return itemlist

    def getprize(self):
        url = "http://p.3.cn/prices/get?skuid=J_"+str(self.itemid)+"&type=1"
        html = getUrl(url).read()
        price = float(self.comp_Price.search(html).group(1))
        return price

    def getimg(self):
        ss = SoupStrainer("div" , id="preview")
        soup = BeautifulSoup(self.itemhtml,parse_only=ss,from_encoding="gbk")
        img = soup.find("div",id="spec-n1").img.src
        return img


    def isZiyin(self):
        if self.itemhtml.find("brand-bar-pop") > -1:
            return False
        else:
            return True
    """
    http://search.jd.com/Search?keyword=Happybellies%20%E7%A6%A7%E8%B4%9D%20%E5%B9%BC%E5%84%BF%E8%94%AC%E6%9E%9C%E8%BD%AF%E9%A5%B4%20100g&enc=utf-8&area=2
    """

    def getItemUrl(self):
        return "http://item.jd.com/"+str(self.itemid)+".html"

    def getSearchUrl(self,txt):
        return  "http://search.jd.com/Search?keyword="+urllib.quote(txt.encode("utf8"))+"&enc=utf-8"

    def noRightResult(self):
        if self.listhtml.find("intellisense") > -1:
            return True
        return False
        
        
        


class Zcn(B2c):
    def __init__(self,itemid=None,itemhtml=None,listhtml=None):
        B2c.__init__(self,itemid=None,itemhtml=None,listhtml=None)
        self.market = "zcn"
        self.comp_amazonid = re.compile(u"/dp/(\w+)/")
        self.comp_amazonprice = re.compile(u"([0-9.]+)")

    def getlist(self):

        def getitem(txt):
            item = Item()
            item.market = self.market
            item.name = unicode(txt.find("h3","newaps").find("span","lrg").string)
            item.itemid = self.comp_amazonid.search(txt.find("h3","newaps").a["href"]).group(1)
            item.price = float(self.comp_amazonprice.search(txt.find("li","newp").a.span.string).group(1))
            item.img = txt.find("div","image imageContainer").img["src"]
            return item

        htmls = self.listhtml.split("&&&")

        atf_txt,btf_txt = None,None 
        for d in htmls:
            try:
                data = json.loads(d)
            except:
                continue
            if data.has_key("results-atf"):
                atf_txt = data["results-atf"]["data"]["value"]
            if data.has_key("results-btf"):
                btf_txt = data["results-btf"]["data"]["value"] 
            if atf_txt and btf_txt:
                break
            ##if data.has_key("results-atf-next"):
                ##atf_next_txt = data["results-atf-next"]["data"]["value"]

                
        itemlist = list()
        if atf_txt:
            soup = BeautifulSoup(atf_txt,from_encoding="utf8")
            div_atfResults = soup.find("div",id="atfResults")
            ##atfResults = soup.find_all("div","fstRowGrid prod celwidget")
            for atf in div_atfResults.children:
                if not isinstance(atf,bs4.element.Tag):
                    continue
                if atf.name <> "div":
                    continue
                item = getitem(atf)
                itemlist.append(item)
        if btf_txt: 
            soup = BeautifulSoup(btf_txt,from_encoding="utf8")
            div_btfResults = soup.find("div",id="btfResults")
            ##btfResults = soup.find_all("div","rsltGrid prod celwidget")
            for btf in div_btfResults.children:
                item = getitem(btf)
                itemlist.append(item)
                if not isinstance(atf,bs4.element.Tag):
                    continue
                if atf.name <> "div":
                    continue
                item = getitem(btf)
                itemlist.append(item)

        return itemlist

    

    def getSearchUrl(self,txt):
        return "http://www.amazon.cn/mn/search/ajax?rh=i%3Aaps%2Ck%3A%E7%94%B5%E9%A3%8E%E6%89%87&__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&fromHash=&fromRH=i%3Aaps%2Ck%3ACOMVITA+%E5%BA%B7%E7%BB%B4%E4%BB%96+%E9%BA%A6%E5%8D%A2%E5%8D%A1%E8%8A%B1+%E8%9C%82%E8%9C%9C%EF%BC%88UMF5+%E3%80%81500g%EF%BC%89&section=ATF&fromApp=gp%2Fsearch&fromPage=results&version=2&ajp=iss"


    def noRightResult(self):
        if self.listhtml.find("noResultsTitle") > -1:
            return True
        return False


class Dangdang(B2c):
    def __init__(self,itemid=None,itemhtml=None,listhtml=None):
        B2c.__init__(self,itemid=None,itemhtml=None,listhtml=None)
        self.market = "dangdang"
        self.comp_itemid = re.compile(u"product_id=(\d+)")
        self.comp_price = re.compile(u"([0-9.]+)")

    def getSearchUrl(self,txt):
        return "http://search.dangdang.com/?key=" + urllib.quote(txt.encode("gbk"))

    def getlist(self):
        ss = SoupStrainer("div" , "book_shoplist")
        soup = BeautifulSoup(self.listhtml,parse_only=ss,from_encoding="gbk")
        lis = soup.find_all("li")
        itemlist = list()
        for li in lis:
            item = Item()
            item.market = self.market
            item.itemid = self.comp_itemid.search(li.find("p","name").a["href"]).group(1)
            item.name = li.find("p","name").a.get_text().strip()
            item.img = li.find("a","pic").img["src"]
            item.price = self.comp_price.search(li.find("p","price").find("span","price_n").string).group(1)
            itemlist.append(item)
        return itemlist

    def noRightResult(self):
        if self.listhtml.find("top_inforpanel") > -1:
            return True
        return False
        

