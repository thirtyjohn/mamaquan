#coding:utf-8
import re,urllib

def getCpslink(pritem):
    cpslink = cpsFactory(pritem.market,pritem.itemid)
    cpslink.encode()
    return cpslink.out_url

def getSrcUrl(url):
    cpslink = Cpslink()
    if url.find("union.jd.com") > -1:
        cpslink = Jdlink()
    elif url.find("yiqifa.com") > -1:
        cpslink = Yqflink()
    elif url.find("yihaodian.com") > -1:
        cpslink = Yhdlink()
    elif url.find("amazon.com") > -1:
        cpslink = Amazonlink()
    elif url.find("amazon.cn") > -1:
        cpslink = Zcnlink()
    elif url.find("union.dangdang.com") > -1:
        cpslink = Danglink()
    elif url.find("s.click.taobao.com") > -1:
        cpslink = Tblink()

    cpslink.out_url = url
    cpslink.decode()
    return cpslink.src_url


def cpsFactory(market,itemid):
    cpslink = Cpslink()
    if market == "zcn":
        cpslink = Zcnlink(itemid = itemid)
    elif market == "jd":
        cpslink = Jdlink(itemid = itemid)
    elif market == "yihaodian":
        cpslink = Yhdlink(itemid = itemid)
    elif market == "amazon":
        cpslink = Amazonlink(itemid = itemid)
    elif market == "dangdang":
        cpslink = Danglink(itemid = itemid)
    elif market == "taobao":
        cpslink = Tblink(itemid = itemid)
    elif market == "tmall":
        cpslink = Tblink(itemid = itemid)

    return cpslink


class Cpslink:
    def __init__(self):
        self.out_url = None
        self.src_url = None

    def encode(self):
        pass
    def decode(self):
        pass

"""
审核中
http://click.union.jd.com/JdClick/?unionId=4298&t=4&to=http://sale.jd.com/act/xywdzCHZJeo5.html
"""
class Jdlink(Cpslink):
    def __init__(self,itemid = None):
        Cpslink.__init__(self)
        self.comp = re.compile(u"&to=(.+)")
        self.itemid = itemid

    def decode(self):
        m = self.comp.search(self.out_url)
        if m:
            self.src_url = m.group(1)
        
    def encode(self):
        self.out_url = None


"""
审核中
http://p.yiqifa.com/c?s=58c30fd7&w=426637&c=4330&i=4984&l=0&e=&t=http://item.51buy.com/item-144631.html
"""
class Yqflink(Cpslink):
    def __init__(self,itemid = None):
        Cpslink.__init__(self)
        self.comp = re.compile(u"&t=(.+)")
        self.itemid = itemid

    def decode(self):
        m = self.comp.search(self.out_url)
        if m:
            self.src_url = m.group(1)
    def encode(self):
        self.out_url = None


"""
已通过
http://www.yihaodian.com/item/2139127_1?tracker_u=10749189
"""
class Yhdlink(Cpslink):
    def __init__(self,itemid = None):
        Cpslink.__init__(self)
        self.comp = re.compile(u"(.+)\?")
        self.itemid = itemid
    
    def decode(self):
        m = self.comp.search(self.out_url)
        if m:
            self.src_url = m.group(1)

    def encode(self):
        self.out_url = "http://www.yihaodian.com/item/"+self.itemid+"?tracker_u=10749189" 


"""
http://www.amazon.com/gp/product/B004FO6U2Y/ref=as_li_ss_tl?ie=UTF8&tag=joyo0102-20&linkCode=as2&camp=217145&creative=399369&creativeASIN=B004FO6U2Y
"""
class Amazonlink(Cpslink):
    def __init__(self,itemid = None):
        Cpslink.__init__(self)
        self.comp = re.compile(u"/product/([0-9A-Z]+)/")
        self.itemid = itemid
    
    def decode(self):
        m = self.comp.search(self.out_url)
        if m:
            self.src_url = "http://www.amazon.com/gp/product/" +m.group(1)

    def encode(self):
        self.out_url = None


"""
审核中
http://www.amazon.cn/mn/detailApp/ref=as_li_ss_tl?_encoding=UTF8&tag=joyo01-23&linkCode=as2&asin=b009gxxdvu&camp=536&creative=3132&creativeASIN=b009gxxdvu
"""
class Zcnlink(Cpslink):
    def __init__(self,itemid = None):
        Cpslink.__init__(self)
        self.comp = re.compile(u"&asin=([a-zA-z0-9]+)")
        self.itemid = itemid
    
    def decode(self):
        m = self.comp.search(self.out_url)
        if m:
            self.src_url = "http://www.amazon.cn/dp/" +m.group(1)

    def encode(self):
        self.out_url = "http://www.amazon.cn/dp/"+self.itemid+"/?_encoding=UTF8&camp=536&creative=3200&linkCode=ur2&tag=joopin-23"


"""
审核中,收款账号未填写
http://union.dangdang.com/transfer.php?from=P-317615&ad_type=10&sys_id=1&backurl=http%3A%2F%2Fproduct.dangdang.com%2Fproduct.aspx%3Fproduct_id%3D22934896
"""
class Danglink(Cpslink):
    def __init__(self,itemid = None):
        Cpslink.__init__(self)
        self.comp = re.compile(u"&backurl=(.+)")
        self.itemid = itemid

    def decode(self):
        m = self.comp.search(self.out_url)
        if m:
            self.src_url = urllib.unquote(m.group(1))
    def encode(self):
        self.out_url = "http://union.dangdang.com/transfer.php?from=P-317615&ad_type=10&sys_id=1&backurl=http%3A%2F%2Fproduct.dangdang.com%2Fproduct.aspx%3Fproduct_id%3D"+str(self.itemid) 


"""
http://s.click.taobao.com/t_js?tu=http%3A%2F%2Fs.click.taobao.com%2Ft_9%3Fp%3Dmm_25282911_0_0%26l%3Dhttp%253a%252f%252fju.taobao.com%252ftg%252fhome.htm%253fitem_id%253d18087424784%26ref%3D%26et%3DjFBC59DBoaE2%252BA%253D%253D
"""
class Tblink(Cpslink):
    def __init__(self,itemid = None):
        Cpslink.__init__(self)
        self.comp1 = re.compile(u"tu=(.+)")
        self.comp2 = re.compile(u"l=(.+)")
        self.itemid = itemid

    def decode(self):
        m = self.comp1.search(self.out_url)
        if m:
            url1 = urllib.unquote(m.group(1))
            m = self.comp2.search(url1)
            if m:
                self.src_url = urllib.unquote(m.group(1))

    def encode(self):
        self.out_url = "http://item.taobao.com/item.htm?id="+str(self.itemid)




