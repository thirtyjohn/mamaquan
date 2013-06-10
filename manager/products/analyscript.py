#coding:utf-8
from settings import localdir,dbconn
from bs4 import BeautifulSoup,SoupStrainer
import re,urllib2,web,json
from datetime import datetime


class Item:
    def __init__(self):
        self.price = None
        self.itemid = None
        self.name = None
        self.market = None
        self.img = None


"""
奶粉属性封装
"""
class Naifen(Item):
    def __init__(self):
        self.duration = None
        self.weight = None
        self.spec = None
        ##self.brand = None
        self.series = None
        self.sellto = None
        self.age = None
        self.duan = None
        self.pack = None
        self.place = None


    def update(self,itemid,market):
        dbconn.update("naifen",where="itemid=$itemid and market=$market",vars=dict(itemid=itemid,market=market),
            duration = self.duration,
            weight = self.weight,
            spec = self.spec,
            ##brand = self.brand,
            series = self.series,
            sellto = self.sellto,
            age = self.age,
            duan = self.duan,
            pack = self.pack,
            place = self.place,
            processed = 1
        )

        

"""
获取奶粉属性
"""
def getItemProperty(nvlist):
    nf = Naifen()
    for name,value in nvlist:
        print name,value
        if name.find(u"厂名") > -1:
            pass
        elif name.find(u"厂址") > -1:
            pass
        elif name.find(u"联系") > -1:
            pass
        elif name.find(u"保质") > -1:
            nf.duration = value.strip()
        elif name.find(u"名称") > -1:
            pass
        elif name.find(u"重量") > -1:
            nf.weight = value.strip()
        ##elif name.find(u"品牌") > -1:
        ##    nf.brand = value.strip()
        elif name.find(u"系列") > -1:
            nf.series = value.strip()
        elif name.find(u"规格") > -1:
            nf.spec = value.strip()
        elif name.find(u"型号") > -1:
            nf.spec = value.strip()
        elif name.find(u"销售") > -1:
            nf.sellto = value.strip()
        elif name.find(u"年龄") > -1:
            nf.age = value.strip()
        elif name.find(u"阶段") > -1:
            nf.duan = value.strip()
        elif name.find(u"包装") > -1:
            nf.pack = value.strip()
        elif name.find(u"产地") > -1:
            nf.place = value.strip()
    return nf

"""
        else:
            f = open(localdir+"test","a")
            f.write(li.string.encode("utf8")+"\n")
"""

def genHost(brand,market):
    r = web.listget(dbconn.query("select url from mmlisturl where brand=$brand and market=$market",vars=dict(brand=brand,market=market)),0,None)
    return r.url if r else None

def genItemUrl(itemid,market):
    if market == "tmall":
        return "http://detail.tmall.com/item.htm?id="+itemid
    elif market == "jd":
        return "http://item.jd.com/"+itemid+".html"
    elif market == "amazon":
        return "http://www.amazon.cn/dp/"+itemid+"/"


class Tmall:
    def __init__(self):
        self.comp_id = re.compile(u"id=(\d+)")
        self.comp_page = re.compile("<span class=\"page-info\">(\d+)/(\d+)</span>")

    def getProperty(self,html):
        ss = SoupStrainer("ul",id="J_AttrUL")
        soup = BeautifulSoup(html,parse_only=ss,from_encoding="gbk")

        lis = soup.find_all("li")
        nvlist = list()
        for li in lis:
            if li.string.find(u"：") > -1:
                name,value = li.string.split(u"：")
            else:
                name,value = li.string.split(u":")
            nvlist.append(name,value)
        nf = getItemProperty(nvlist)
        return nf

    def getItemFromList(self,html):
        ss = SoupStrainer("div",id="J_ShopSearchResult")
        soup = BeautifulSoup(html,parse_only=ss,from_encoding="gbk")
        lis = soup.find("ul","shop-list").find_all("li")
        itemlist = list()

        for li in lis:
            item = Item()
            item.itemid = self.comp_id.search(li.find("div","desc").a["href"]).group(1)
            item.name = li.find("div","desc").a.string.strip()
            item.price = int(float(li.find("div","price").strong.string))
            item.img = li.find("div","pic").img["data-ks-lazyload"]
            itemlist.append(item)
        return itemlist

    def initNf(self,itemid):

        url = "http://detail.tmall.com/item.htm?id="+str(itemid)
        html = urllib2.urlopen(url).read()
        
        nf = self.getProperty(html)
        nf.update(itemid,"tmall")


    """
    批量获取天猫某品牌奶粉数据
    """ 

    def initNfs(self,brand,pagenum=None):
        if not pagenum:
            pagenum = 1
        url = genHost(brand,'tmall')+"search.htm?search=y&viewType=grid&orderType=_hotsell&pageNum="+str(pagenum)
        html = urllib2.urlopen(url).read()
        ##html = open( localdir + "search.htm", "r").read()
        nflist = self.getItemFromList(html)
        for nf in nflist:
            dbconn.insert("naifen",itemid=nf.itemid,name=nf.name,price=nf.price,img=nf.img,market=u'tmall',brand=brand)

        m = self.comp_page.search(html)
        if m:
            currentpage = int(m.group(1))
            allpage = int(m.group(2))
            if currentpage < allpage:
                self.initTmallNfs(pagenum+1)



class Jd:
    def __init__(self):
        self.comp_Price = re.compile("\"p\":\"([0-9.]+)\"")
        self.comp_itemid = re.compile("/(\d+).html")
        self.comp_page = re.compile(u"共(\d+)页")

    def getProperty(self,html):
        ss = SoupStrainer("ul","detail-list")
        soup = BeautifulSoup(html,parse_only=ss,from_encoding="gbk")

        lis = soup.find_all("li")
        nvlist = list()
        for li in lis:
            li_string = li.get_text()
            if not li_string:
                continue
            if li_string.find(u"：") > -1:
                name,value = li_string.split(u"：")
            else:
                name,value = li_string.split(u":")
            nvlist.append((name,value))
        return nvlist

    def getPrice(self,itemid):
        url = "http://p.3.cn/prices/get?skuid=J_"+str(itemid)+"&type=1"
        html = urllib2.urlopen(url).read()
        price = float(self.comp_JdPrice.search(html).group(1))
        return price

    def getItemFromList(self,html):
        ss = SoupStrainer("ul" , "list-h clearfix")
        soup = BeautifulSoup(html,parse_only=ss,from_encoding="gbk")
        lis = soup.find_all("li")
        itemlist = list()
        for li in lis:
            item = Item()
            item.itemid = self.comp_itemid.search(li.find("div","p-name").a["href"]).group(1)
            item.name = li.find("div","p-name").a.get_text().strip()
            item.img = li.find("div","p-img").img["data-lazyload"]
            itemlist.append(item)
        return itemlist

    def initNf(self,itemid):

        url = "http://item.jd.com/"+str(itemid)+".html"
        html = urllib2.urlopen(url).read()
        nvlist = self.getProperty(html)

        for name,value in nvlist:
            if name == u"店铺":
                dbconn.delete("naifen",where="itemid=$itemid",vars=dict(itemid=itemid))
                return

        nf = getItemProperty(nvlist)
        nf.update(itemid,'jd') 
        price = self.getPrice(itemid)
        dbconn.update("naifen",price=price,where="itemid=$itemid and market='jd'",vars=dict(itemid=itemid))



    """
    批量获取京东某品牌奶粉数据,无价格
    """

    def initNfs(self,brand,pagenum=None):
        if not pagenum:
            pagenum = 1
        url = genHost(brand,'jd')+"&wtype=1&area=2&psort=&page="+str(pagenum)+"&vt=1"
        html = urllib2.urlopen(url).read()
        ##html = open( localdir + "search.htm", "r").read()

        nflist = self.getItemFromList(html)
        for nf in nflist:
            dbconn.insert("naifen",itemid=nf.itemid,name=nf.name,market=u"jd",brand=brand,img=nf.img)

        ss = SoupStrainer("div" , id="bottom_pager")
        soup = BeautifulSoup(html,parse_only=ss,from_encoding="gbk")
        page_string = soup.find("span","page-skip").em.string
        pageall = int(self.comp_page.search(page_string).group(1))
        if pagenum < pageall:
            self.initNfs(brand,pagenum+1)



class Amazon:
    def __init__(self):
        self.comp_amazonid = re.compile(u"/dp/(\w+)/")
        self.comp_amazonprice = re.compile(u"([0-9.]+)")

    """
    获取折扣信息
    与原有折扣进行比较，如果有变化则插入
    看生否生效，设置validate和processed字段
    """
    def getAmazonDetail(itemid):
        url = genItemUrl(itemid,"amazon")
        html = urllib2.urlopen(url).read()

        ss = SoupStrainer("div",id="quickPromoBucketContent")
        soup = BeautifulSoup(html,parse_only=ss,from_encoding="utf8")
        for li in soup.find_all("li"):
            if li.find("form"):
                break
            dbconn.insert("itempromo",itemid=itemid,market=u'amazon',longdes=li.get_text(),wdate=datetime.now())


    def getItemFromList(self,html):

        def getitem(txt):
            item = Item()
            item.name = unicode(txt.find("h3","newaps").find("span","lrg").string)
            item.itemid = self.comp_amazonid.search(txt.find("h3","newaps").a["href"]).group(1)
            item.price = float(self.comp_amazonprice.search(txt.find("li","newp").a.span.string).group(1))
            item.img = txt.find("div","image imageContainer").img["src"]
            return item

        htmls = html.split("&&&")

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
        soup = BeautifulSoup(atf_txt,from_encoding="utf8")
        atfResults = soup.find_all("div","fstRowGrid prod")
        for atf in atfResults:
            item = getitem(atf)
            itemlist.append(item)
            
        soup = BeautifulSoup(btf_txt,from_encoding="utf8")
        btfResults = soup.find_all("div","rsltGrid prod")
        for btf in btfResults:
            item = getitem(btf)
            itemlist.append(item)

        return itemlist
 
    def hasNextPage(self,html):
        htmls = html.split("&&&")

        pagination = None
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
    批量获取亚马逊某品牌商品

    """
    def initNfs(self,brand,pagenum=None):
        url = genHost(brand,'amazon') 
        if pagenum:
            url = url + "&page="+str(pagenum)
        print url
        rq = urllib2.Request(url)
        rq.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:20.0) Gecko/20100101 Firefox/20.0")
        ##html = open(localdir+"item.json","r").read()
        html = urllib2.urlopen(rq).read()

        nflist = self.getItemFromList(html)
        for nf in nflist:
            dbconn.insert("naifen",name=nf.name,itemid=nf.itemid,price=nf.price,market=u"amazon",brand=brand,img=nf.img)

        if self.hasNextPage(html): 
            self.initNfs(brand,pagenum+1 if pagenum else 2)

        """
        print "***************" 
        soup = BeautifulSoup(atf_next_txt,from_encoding="utf8")
        print soup
        atfnextResults = soup.find_all("div","fstRowGrid prod")
        for atf in atfnextResults:
            name = atf.find("h3","newaps").find("span","lrg").string
            itemid = atf.find("h3","newaps").a["href"]
            price = atf.find("li","newp").a.span.string
            print name,itemid,price
        """

"""
def hhhgetTmallNaifenId(brand,pagenum=None):
    if not pagenum:
        pagenum = 1
    url = genHost(brand,'tmall')+"search.htm?search=y&viewType=grid&orderType=_hotsell&pageNum="+str(pagenum)
    print url
    html = urllib2.urlopen(url).read()
    ##html = open( localdir + "search.htm", "r").read()
    ss = SoupStrainer("div",id="J_ShopSearchResult")
    soup = BeautifulSoup(html,parse_only=ss,from_encoding="gbk")
    print soup
    lis = soup.find("ul","shop-list").find_all("li")

    for li in lis:
        itemid = comp_id.search(li.find("div","desc").a["href"]).group(1)
        img = li.find("div","pic").img["data-ks-lazyload"]
        dbconn.update("naifen",where="itemid=$itemid and market='tmall'",vars=dict(itemid=itemid),img=img)

    m = comp_page.search(html)
    if m:
        currentpage = int(m.group(1))
        allpage = int(m.group(2))
        if currentpage < allpage:
            hhhgetTmallNaifenId(pagenum+1)
"""

