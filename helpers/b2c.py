#coding:utf-8
from bs4 import BeautifulSoup,SoupStrainer
from helpers.crawls import getUrl
import re,urllib,json,bs4,traceback
from helpers.loggers import get_logger

class Item(dict):
    def __init__(self):
        dict.__init__(self)
        self.itemid = None
        self.name = None
        self.market = None 
        self.img = None
        self.price = None
        self.currency = None
        self.status = 0
    def __setattr__(self,n,v):
        self[n] = v
    def __getattr__(self,n):
        try:
            return self[n]
        except KeyError, k:
            raise AttributeError, k


def factory(market):
    b2c = B2c()
    if market == "jd":
        b2c = Jd()
    elif market == "zcn":
        b2c = Zcn()
    elif market == "dangdang":
        b2c = Dangdang()
    elif market == "tmall":
        b2c = Tmall()
    return b2c

def getItemUrl(itemid,market):
    b = factory(market)
    b.itemid = itemid
    return b.getItemUrl()

def getItemid(url,market):
    b = factory(market)
    return b.getItemidFromUrl(url)


class B2c:
    def __init__(self,itemid=None,itemhtml=None,listhtml=None):
        self.market = None
        self.itemid = None
        self.itemhtml = None
        self.listhtml = None
        self.listurl = None

    def getlist(self):
        pass

    def getitem(self):
        pass

    def getimg(self):
        pass

    def isZiyin(self):
        pass

    def getPrice(self):
        pass

    def getPromo(self):
        pass

    def getSearchUrl(self,txt):
        pass

    def getItemUrl(self):
        pass

    def getListHtml(self):
        html = getUrl(self.listurl)
        return html

    def getSearchHtml(self,txt):
        url = self.getSearchUrl(txt)
        html = getUrl(url)
        return html

    def getItemHtml(self):
        if self.itemhtml:
            return self.itemhtml
        url = self.getItemUrl()
        html = getUrl(url)
        self.itemhtml = html
        return html

    def getItemidFromUrl(self,url):
        pass

    def getStock(self):
        return 1



class Jd(B2c):
    
    def __init__(self,itemid=None,itemhtml=None,listhtml=None):
        B2c.__init__(self,itemid=None,itemhtml=None,listhtml=None)
        self.market = "jd"
        self.comp_Price = re.compile("\"p\":\"([0-9.-]+)\"")
        self.comp_itemid = re.compile("/(\d+).html")
        self.from_encoding = "gbk"

    def getProperty(self):
        self.itemhtml = self.getItemHtml()
        ss = SoupStrainer("ul","detail-list")
        soup = BeautifulSoup(self.itemhtml,parse_only=ss,from_encoding=self.from_encoding)
        lis = soup.find_all("li")
        nvdict = dict()
        for li in lis:
            ii_text = li.get_text()
            name,value = None,None
            if ii_text.find(u"：") > -1:
                name,value = ii_text.split(u"：")
            if name and value:
                nvdict.update({name:value})
        return nvdict

    def getlist(self):
        self.listhtml = self.getListHtml()
        ss = SoupStrainer("ul" , "list-h")
        soup = BeautifulSoup(self.listhtml,parse_only=ss,from_encoding=self.from_encoding)
        lis = soup.find_all("li")
        itemlist = list()
        for li in lis:
            item = Item()
            item.market = self.market
            item.itemid = self.comp_itemid.search(li.find("div","p-name").a["href"]).group(1)
            item.name = li.find("div","p-name").a.get_text().strip()
            img = li.find("div","p-img").a.img 
            item.img = img["src"] if img.has_key("src") else img["data-lazyload"]
            itemlist.append(item)
        return itemlist

    def getPrice(self):
        url = "http://p.3.cn/prices/get?skuid=J_"+str(self.itemid)+"&type=1"
        html = getUrl(url)
        m = self.comp_Price.search(html)
        if not m:
            get_logger("general").debug("jd price: "+html)
            return None
        price = float(m.group(1))
        if price < 0:
            return 0
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

    def nextPage(self):
        self.listhtml = self.getListHtml()
        ss = SoupStrainer("div","pagin pagin-m")
        soup = BeautifulSoup(self.listhtml,parse_only=ss,from_encoding=self.from_encoding)
        if soup.find("span","next-disabled"):
            return False
        return True

    def getPromo(self):
        url = "http://jprice.360buy.com/pageadword/"+str(self.itemid)+"-1-1.html?callback=Promotions.set"
        html = getUrl(url)
        m = re.search("Promotions.set\((.+)\)",html)
        data = json.loads(m.group(1))
        promotionInfoList = data["promotionInfoList"]
        if len(promotionInfoList) == 0:
            return "no"
        needMondey = float(promotionInfoList[0]["needMondey"]) if promotionInfoList[0]["needMondey"] else None
        reward = float(promotionInfoList[0]["reward"]) if promotionInfoList[0]["reward"] else None
        if needMondey > 0.0 and reward > 0.0:
            return u"满"+str(needMondey)+u"减"+str(reward)
        else:
            return "no"
    
    def getStock(self):
        if self.getPrice() == 0:
            return 0
        return 1



class Zcn(B2c):
    def __init__(self,itemid=None,itemhtml=None,listhtml=None):
        B2c.__init__(self,itemid=None,itemhtml=None,listhtml=None)
        self.market = "zcn"
        self.comp_itemid = re.compile(u"/dp/(\w+)")
        self.comp_price = re.compile(u"([0-9.,]+)")
        self.from_encoding = "utf8"
        self.comp_page = re.compile(u"(\d+)-(\d+).+?(\d+)")

    def getlist(self):

        def getitem(txt):
            item = Item()
            item.market = self.market
            item.name = unicode(txt.find("h3","newaps").find("span","lrg").string)
            item.itemid = self.comp_itemid.search(txt.find("h3","newaps").a["href"]).group(1)
            item.price = float(self.comp_price.search(txt.find("li","newp").a.span.string).group(1))
            item.img = txt.find("div","image imageContainer").img["src"]
            return item

        self.listhtml = self.getListHtml()
        htmls = self.listhtml.split("&&&")

        atf_txt,btf_txt = None,None 
        for d in htmls:
            try:
                data = json.loads(d)
            except:
                continue
            if data.has_key("center"):
                atf_txt = data["center"]["data"]["value"]
            if data.has_key("centerBelow"):
                btf_txt = data["centerBelow"]["data"]["value"] 
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
                if not atf.find("h3","newaps"):
                    continue
                item = getitem(atf)
                itemlist.append(item)

        if btf_txt: 
            soup = BeautifulSoup(btf_txt,from_encoding=self.from_encoding)
            div_btfResults = soup.find("div",id="btfResults")
            if div_btfResults:
            ##btfResults = soup.find_all("div","rsltGrid prod celwidget")
                for btf in div_btfResults.children:
                    if not isinstance(btf,bs4.element.Tag):
                        continue
                    if btf.name <> "div":
                        continue
                    if not btf.find("h3","newaps"):
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
        self.itemhtml = self.getItemHtml()
        ss = SoupStrainer("div" , id="main_image_0")
        soup = BeautifulSoup(self.itemhtml,parse_only=ss,from_encoding=self.from_encoding)
        img = soup.img["src"]
        return img

    def nextPage(self):
        htmls = self.listhtml.split("&&&")

        centerhtml = None

        for d in htmls:
            try:
                data = json.loads(d)
            except:
                continue
            if data.has_key("center"):
                centerhtml = data["center"]["data"]["value"]
        

        soup = BeautifulSoup(centerhtml,from_encoding=self.from_encoding)
        pagehtml = soup.find("h2",id="resultCount")
        if not pagehtml:
            print "pagehtml not found"
            return False
        pagetxt = pagehtml.span.get_text().strip()
        ##1-24条， 共26条
        m = self.comp_page.search(pagetxt)
        if not m:
            print "pagehtml not found"
            return False
        print m.group(2)
        print m.group(3)
        if int(m.group(2)) == int(m.group(3)):
            return False
        return True



        """
        for d in htmls:
            try:
                data = json.loads(d)
            except:
                continue
            if data.has_key("pagination"):
                pagination = data["pagination"]["data"]["value"]
            if  pagination:
                break


        soup = BeautifulSoup(pagination,from_encoding="utf8")
        if soup.find("span","pagnRA"):
            return True
        return False
        """

    def getPrice(self):
        self.itemhtml = self.getItemHtml()
        ss = SoupStrainer("span" , id="actualPriceValue")
        soup = BeautifulSoup(self.itemhtml,parse_only=ss,from_encoding=self.from_encoding)
        if not soup.find("b"):
            return 0
        price_txt = soup.find("b").string
        return float(self.comp_price.search(price_txt).group(1).replace(",",""))
    

    def getPromo(self):
        self.itemhtml = self.getItemHtml()
        ss = SoupStrainer("div",id="quickPromoBucketContent")
        soup = BeautifulSoup(self.itemhtml,parse_only=ss,from_encoding=self.from_encoding)
        lis = soup.find_all("li")
        if len(lis) == 0:
            return "no"
        if lis[0].find("form"):
            return "no"
        if lis[0].get_text().find(u"促销优惠单张订单仅享受1次") > -1:
            return "no"
        return lis[0].get_text()

    def getStock(self):
        self.itemhtml = self.getItemHtml()
        ss = SoupStrainer("div","buying",style="padding-bottom: 0.75em;")
        soup = BeautifulSoup(self.itemhtml,parse_only=ss,from_encoding=self.from_encoding)
        if soup.get_text().find(u"由亚马逊直接销售和发货") > -1:
            return 1
        return 0


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
        self.listhtml = self.getListHtml()
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

    def getPrice(self):
        price = None
        html = self.getItemHtml()

        #取抢购价
        ss = SoupStrainer("div" , "show_info")
        soup = BeautifulSoup(html,parse_only=ss,from_encoding=self.from_encoding)
        promos = soup.find_all("div","event")
        if promos and len(promos) > 0:
            for p in promos:
                if p.find("span","icon_bg").get_text().strip() == u"抢 购": 
                    price = float(self.comp_price.search(p.find("i",id="promo_price").get_text()).group(1)) if p.find("i",id="promo_price") else None
        if price:
            return price
        return float(self.comp_price.search(soup.find("span",id="salePriceTag").get_text()).group(1))
    

    def getPromo(self):
        html = self.getItemHtml()
        ss = SoupStrainer("div" , "show_info")
        soup = BeautifulSoup(html,parse_only=ss,from_encoding=self.from_encoding)
        promos = soup.find_all("div","event")
        if promos and len(promos) > 0:
            for p in promos:
                if p.find("span","icon_bg").get_text().strip() == u"满额减":
                    promo_txt = u""
                    for c in p.find("div","rule").children:
                        if isinstance(c,bs4.element.NavigableString):
                            promo_txt += c
                        else:
                            if c.name == "br":
                                break
                            promo_txt += c.get_text()
                    return promo_txt if promo_txt.strip()<>"" else "no"
        return "no"

    def getStock(self):
        html = self.getItemHtml()
        ss = SoupStrainer("div" , "show_info")
        soup = BeautifulSoup(html,parse_only=ss,from_encoding=self.from_encoding)
        if soup.find("a",id="sign_no_stock"):
            return 0
        return 1

    def isZiyin(self):
        html = self.getItemHtml()
        ss = SoupStrainer("div" , "show_info")
        soup = BeautifulSoup(html,parse_only=ss,from_encoding=self.from_encoding)
        if soup.find("div","legend l_dang"):
            return True
        return False


class Tmall(B2c):
    def __init__(self,itemid=None,itemhtml=None,listhtml=None):
        B2c.__init__(self,itemid=None,itemhtml=None,listhtml=None)
        self.market = "tmall"
        self.comp_id = re.compile(u"id=(\d+)")
        self.comp_price = re.compile(u"[0-9.]+")
        self.comp_page = re.compile("<span class=\"page-info\">(\d+)/(\d+)</span>")
        self.comp_initApi = re.compile(u"\"initApi\" : \"(\S+?)\"")
        self.from_encoding = "gbk"

    def getProperty(self):
        self.itemhtml = self.getItemHtml()
        ss = SoupStrainer("ul",id="J_AttrUL")
        soup = BeautifulSoup(self.itemhtml,parse_only=ss,from_encoding=self.from_encoding)

        lis = soup.find_all("li")
        nvdict = dict()
        for li in lis:
            name,value = None,None
            if li.string.find(u"：") > -1:
                i = li.string.find(u"：")
                name,value = li.string[:i].strip(),li.string[i+1:].strip()
            elif li.string.find(u":") > -1:
                i = li.string.find(u":")
                name,value = li.string[:i].strip(),li.string[i+1:].strip()
            if name and value:
                nvdict.update({name:value})

        ss = SoupStrainer("a","sn-simple-logo-shop")
        soup = BeautifulSoup(self.itemhtml,parse_only=ss,from_encoding=self.from_encoding)
        try:
            nvdict.update({"maijia":soup.a.string})
        except:
            pass
        return nvdict

    def getlist(self):
        """
        ss = SoupStrainer("div",id="J_ShopSearchResult")
        soup = BeautifulSoup(self.listhtml,parse_only=ss,from_encoding=self.from_encoding)
        lis = soup.find("ul","shop-list").find_all("li")
        itemlist = list()

        for li in lis:
            item = Item()
            item.itemid = self.comp_id.search(li.find("div","desc").a["href"]).group(1)
            item.name = li.find("div","desc").a.string.strip()
            item.price = int(float(li.find("div","price").strong.string))
            item.img = li.find("div","pic").img["data-ks-lazyload"]
            itemlist.append(item)
        """
        self.listhtml = self.getListHtml()
        ss = SoupStrainer("div",id="J_ItemList")
        soup = BeautifulSoup(self.listhtml,parse_only=ss,from_encoding=self.from_encoding)
        lis = soup.find_all("div","product")
        itemlist = list()

        for li in lis:
            item = Item()
            item.itemid = self.comp_id.search(li.find("p","productTitle").a["href"]).group(1)
            item.name = li.find("p","productTitle").a.string.strip()
            item.price = float(self.comp_price.search(li.find("p","productPrice").em.string).group())
            item.img = li.find("div","productImg-wrap").img["data-ks-lazyload"]
            itemlist.append(item)
        return itemlist

    def getItemUrl(self):
        return "http://detail.tmall.com/item.htm?id="+str(self.itemid)

    
    def nextPage(self):
        return True
        """
        m = self.comp_page.search(self.listhtml)
        if m:
            currentpage = int(m.group(1))
            allpage = int(m.group(2))
            if currentpage < allpage:
                return currentpage+1
            return None
        return None
        """

    def getPrice(self):
        self.itemhtml = self.getItemHtml() 
        price_url = self.comp_initApi.search(self.itemhtml).group(1)
        html = getUrl(price_url,header={"Referer":self.getItemUrl()})
        data = None
        try:
            data = json.loads(html.decode(self.from_encoding))
        except:
            get_logger("general").debug("tmall price: " + html)
            get_logger("general").debug("tmall price: " + traceback.format_exc())
        if not data:
            return None
        if not data["defaultModel"]["itemPriceResultDO"]["priceInfo"].has_key("def"):
            return 0
        data_def = data["defaultModel"]["itemPriceResultDO"]["priceInfo"]["def"]
        price = float(data_def["price"])
        if data_def.has_key("promotionList") and data_def["promotionList"]:
            if len(data_def["promotionList"]) > 0:
                for promo in data_def["promotionList"]:
                    if not promo.has_key("promo"):
                        get_logger("general").debug(promo)
                        continue
                    if float(promo["promo"]) < price:
                        price = float(promo["promo"])

        return price


    def getPromo(self):
        return "no"
    
    def getStock(self):
        if self.getPrice() == 0:
            return 0
        return 1




