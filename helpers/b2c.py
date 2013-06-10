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

    def getimg(self):
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

    def getItemidFromUrl(self,url):
        pass



class Jd(B2c):
    
    def __init__(self,itemid=None,itemhtml=None,listhtml=None):
        B2c.__init__(self,itemid=None,itemhtml=None,listhtml=None)
        self.market = "jd"
        self.comp_Price = re.compile("\"p\":\"([0-9.]+)\"")
        self.comp_itemid = re.compile("/(\d+).html")
        self.from_encoding = "gbk"

    def getlist(self):
        ss = SoupStrainer("ul" , "list-h clearfix")
        soup = BeautifulSoup(self.listhtml,parse_only=ss,from_encoding=self.from_encoding)
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
        soup = BeautifulSoup(self.itemhtml,parse_only=ss,from_encoding=self.from_encoding)
        img = soup.find("div",id="spec-n1").img["src"]
        return img


    def isZiyin(self):
        if self.itemhtml.find("brand-bar-pop") > -1:
            return False
        else:
            return True


    def getItemUrl(self):
        return "http://item.jd.com/"+str(self.itemid)+".html"

    def getSearchUrl(self,txt):
        return  "http://search.jd.com/Search?keyword="+urllib.quote(txt.encode("utf8"))+"&enc=utf-8"

    def noRightResult(self):
        if self.listhtml.find("intellisense") > -1:
            return True
        return False

    def getItemidFromUrl(self,url):
        m = self.comp_itemid.search(url)
        if m:
            return m.group(1)
        return None


class Zcn(B2c):
    def __init__(self,itemid=None,itemhtml=None,listhtml=None):
        B2c.__init__(self,itemid=None,itemhtml=None,listhtml=None)
        self.market = "zcn"
        self.comp_itemid = re.compile(u"/dp/(\w+)")
        self.comp_price = re.compile(u"([0-9.]+)")
        self.from_encoding = "utf8"

    def getlist(self):

        def getitem(txt):
            item = Item()
            item.market = self.market
            item.name = unicode(txt.find("h3","newaps").find("span","lrg").string)
            item.itemid = self.comp_itemid.search(txt.find("h3","newaps").a["href"]).group(1)
            item.price = float(self.comp_price.search(txt.find("li","newp").a.span.string).group(1))
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
            soup = BeautifulSoup(atf_txt,from_encoding=self.from_encoding)
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
            soup = BeautifulSoup(btf_txt,from_encoding=self.from_encoding)
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

    def getItemUrl(self):
        return "http://www.amazon.cn/dp/"+str(self.itemid)

    def getSearchUrl(self,txt):
        return "http://www.amazon.cn/s/ref=nb_sb_noss?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Daps&field-keywords="+urllib.quote(txt.encode("utf8"))

    def noRightResult(self):
        if self.listhtml.find("noResultsTitle") > -1:
            return True
        return False

    def getItemidFromUrl(self,url):
        m = self.comp_itemid.search(url)
        if m:
            return m.group(1)
        return None

    def getimg(self):
        ss = SoupStrainer("div" , id="main_image_0")
        soup = BeautifulSoup(self.itemhtml,parse_only=ss,from_encoding=self.from_encoding)
        img = soup.img["src"]
        return img


class Dangdang(B2c):
    def __init__(self,itemid=None,itemhtml=None,listhtml=None):
        B2c.__init__(self,itemid=None,itemhtml=None,listhtml=None)
        self.market = "dangdang"
        self.comp_itemid = re.compile(u"product_id=(\d+)")
        self.comp_price = re.compile(u"([0-9.]+)")
        self.from_encoding = "gbk"

    def getItemUrl(self):
        return "http://product.dangdang.com/product.aspx?product_id="+str(self.itemid)

    def getSearchUrl(self,txt):
        return "http://search.dangdang.com/?key=" + urllib.quote(txt.encode("gbk"))

    def getlist(self):
        ss = SoupStrainer("div" , "book_shoplist")
        soup = BeautifulSoup(self.listhtml,parse_only=ss,from_encoding=self.from_encoding)
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

    def getItemidFromUrl(self,url):
        m = self.comp_itemid.search(url)
        if m:
            return m.group(1)
        return None


    def getimg(self):
        ss = SoupStrainer("a" , id="largePicLink")
        soup = BeautifulSoup(self.itemhtml,parse_only=ss,from_encoding=self.from_encoding)
        img = soup.img["wsrc"]
        return img
        

