#coding:utf-8
import re,urllib

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

class Cpslink:
    def __init__(self):
        self.out_url = None
        self.src_url = None

    def encode(self):
        pass
    def decode(self):
        pass

"""
http://click.union.jd.com/JdClick/?unionId=4298&t=4&to=http://sale.jd.com/act/xywdzCHZJeo5.html
"""
class Jdlink(Cpslink):
    def __init__(self):
        Cpslink.__init__(self)
        self.comp = re.compile(u"&to=(.+)")

    def decode(self):
        m = self.comp.search(self.out_url)
        if m:
            self.src_url = m.group(1)
        
    def encode(self):
        self.out_url = None


"""
http://p.yiqifa.com/c?s=58c30fd7&w=426637&c=4330&i=4984&l=0&e=&t=http://item.51buy.com/item-144631.html
"""
class Yqflink(Cpslink):
    def __init__(self):
        Cpslink.__init__(self)
        self.comp = re.compile(u"&t=(.+)")

    def decode(self):
        m = self.comp.search(self.out_url)
        if m:
            self.src_url = m.group(1)
    def encode(self):
        self.out_url = None


"""
http://www.yihaodian.com/item/2139127_1?tracker_u=1037022154
"""
class Yhdlink(Cpslink):
    def __init__(self):
        Cpslink.__init__(self)
        self.comp = re.compile(u"(.+)\?")
    
    def decode(self):
        m = self.comp.search(self.out_url)
        if m:
            self.src_url = m.group(1)

    def encode(self):
        self.out_url = None 


"""
http://www.amazon.com/gp/product/B004FO6U2Y/ref=as_li_ss_tl?ie=UTF8&tag=joyo0102-20&linkCode=as2&camp=217145&creative=399369&creativeASIN=B004FO6U2Y
"""
class Amazonlink(Cpslink):
    def __init__(self):
        Cpslink.__init__(self)
        self.comp = re.compile(u"/product/([0-9A-Z]+)/")
    
    def decode(self):
        m = self.comp.search(self.out_url)
        if m:
            self.src_url = "http://www.amazon.com/gp/product/" +m.group(1)

    def encode(self):
        self.out_url = None


"""
http://www.amazon.cn/mn/detailApp/ref=as_li_ss_tl?_encoding=UTF8&tag=joyo01-23&linkCode=as2&asin=b009gxxdvu&camp=536&creative=3132&creativeASIN=b009gxxdvu
"""
class Zcnlink(Cpslink):
    def __init__(self):
        Cpslink.__init__(self)
        self.comp = re.compile(u"&asin=([a-zA-z0-9]+)")
    
    def decode(self):
        m = self.comp.search(self.out_url)
        if m:
            self.src_url = "http://www.amazon.cn/dp/" +m.group(1)

    def encode(self):
        self.out_url = None


"""
http://union.dangdang.com/transfer.php?from=P-295759&ad_type=10&sys_id=1&backurl=http%3a%2f%2fproduct.dangdang.com%2fproduct.aspx%3fproduct_id%3d60266915
"""
class Danglink(Cpslink):
    def __init__(self):
        Cpslink.__init__(self)
        self.comp = re.compile(u"&backurl=(.+)")
    def decode(self):
        m = self.comp.search(self.out_url)
        if m:
            self.src_url = urllib.unquote(m.group(1))
    def encode(self):
        self.out_url = None


"""
http://s.click.taobao.com/t_js?tu=http%3A%2F%2Fs.click.taobao.com%2Ft_9%3Fp%3Dmm_25282911_0_0%26l%3Dhttp%253a%252f%252fju.taobao.com%252ftg%252fhome.htm%253fitem_id%253d18087424784%26ref%3D%26et%3DjFBC59DBoaE2%252BA%253D%253D
"""
class Tblink(Cpslink):
    def __init__(self):
        Cpslink.__init__(self)
        self.comp1 = re.compile(u"tu=(.+)")
        self.comp2 = re.compile(u"l=(.+)")
    def decode(self):
        m = self.comp1.search(self.out_url)
        if m:
            url1 = urllib.unquote(m.group(1))
            m = self.comp2.search(url1)
            if m:
                self.src_url = urllib.unquote(m.group(1))

    def encode(self):
        self.out_url = None




