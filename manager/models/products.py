#coding:utf8
from manager.settings import dbconn,mongoconn
from datetime import datetime
import web
from helpers.b2c import Item

class semistatus:
    JUST_INSERT = 0
    JUST_MORE = 1



class Product(dict):
    def __init__(self):
        dict.__init__(self)
        self.name = None
        self.img = None
        self.price = None
    def __setattr__(self,n,v):
        self[n] = v
    def __getattr__(self,n):
        try:
            return self[n]
        except KeyError, k:
            raise AttributeError, k
    

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
        dbconn.update("naifenitem",where="itemid=$itemid and market=$market",vars=dict(itemid=itemid,market=market),
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
def getNfProperty(nvlist):
    nf = Naifen()
    for name,value in nvlist:
        ##print name,value
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

def updateNfitem(nfid,**kwargs):
    dbconn.update("naifenitem",where="id=$nfid",vars=dict(nfid=nfid),**kwargs)


def hasNfitem(nf):
    return web.listget(dbconn.query("select * from naifenitem where itemid=$itemid and market=$market",vars=dict(itemid=nf.itemid,market=nf.market)),0,None)


def insert_semi_item(data):
    return mongoconn.insert("semiitem",data)

def has_semi_item(**kwargs):
    return mongoconn.query_one("semiitem",where=kwargs) 

def get_semi_item(**kwargs):
    return mongoconn.query("semiitem",where=kwargs)

def aggregate_item_temp(pipe,**kwargs):
    return mongoconn.aggregate("item_temp",pipe,**kwargs)

def aggregate(table,pipe,**kwargs):
    return mongoconn.aggregate(table,pipe,**kwargs)

def update_semi_item(mid,nvdict):
    return mongoconn.update("semiitem",{"_id":mid},nvdict)


def insert_item(item):
    return mongoconn.insert("item",item)

def get_item(**kwargs):
    return mongoconn.query("item",where=kwargs)

def has_item(**kwargs):
    return mongoconn.query("item",where=kwargs).count() > 0

def insert_product(pr):
    return mongoconn.insert("product",pr)

def get_product(**kwargs):
    return mongoconn.query("product",where=kwargs)

def get_matched_item_ids(**kwargs):
    matched_item_ids = list()
    for r in mongoconn.query("product",where=kwargs,fields={"match_ids":1}):
        matched_item_ids.extend( r["match_ids"] )
    return matched_item_ids

def add_pr_match(pr=None,item=None):
    if not pr or not item:
        return
    mongoconn.append("product",{"_id":pr["_id"]},{"match_ids":item["_id"]})


def insert_item_temp(semiitem):
    return mongoconn.insert("item_temp",semiitem)

def get_temp_item(**kwargs):
    return mongoconn.query("item_temp",where=kwargs)

def update_item_temp(mid,nvdict):
    return mongoconn.update("item_temp",{"_id":mid},nvdict)

def insertNfitem(nf):
    dbconn.insert("naifenitem",itemid=nf.itemid,name=nf.name,price=nf.price,img=nf.img,market=nf.market,brand=nf.brand)

def getHosts(cat=None,market=None,other=None):
    urls = list()
    r = mongoconn.query("crawl_list_url",where=other.update({"cat":cat,"market":market}) if other else {"cat":cat,"market":market})
    if isinstance(r[0]["url"],list):
        urls.extend(r[0]["url"])
    else:
        urls.append(r[0]["url"])
    return urls

def getHost(url_patten,page=None): 
    url = url_patten.replace(u"${page}",unicode(page))
    return url

def getNfitemNotProcessed(market=None,brand=None):
    return dbconn.query("select * from naifenitem where processed is null "+ ("and market = $market" if market else "") + (" and brand = $brand" if brand else ""),vars=dict(market=market,brand=brand))

"""
批量插入预产品库,建立对应关系
"""
def batchInsertPreNf(market=None,brand=None):
    dbconn.query("insert into prenaifen (name,duration,weight,spec,brand,series,sellto,age,duan,pack,place,price,img) select name,duration,weight,spec,brand,series,sellto,age,duan,pack,place,price,img from naifenitem where brand = $brand and market = $market and yangben = 0",vars=dict(brand=brand,market=market))
    dbconn.query("update naifenitem set yangben = 1 where brand = $brand and market = $market",vars=dict(brand=brand,market=market))
    res = dbconn.query(u"select * from prenaifen where brand = $brand",vars=dict(brand=brand))
    for r in res:
        res1  = dbconn.query(u"select * from naifenitem where name = $name and market=$market",vars=dict(name=r.name,market=market))
        item = web.listget(res1,0,None)
        dbconn.insert("formalprmatch",prid=r.ID,itemid=item.itemid,market=market)


def getNfitemNotMatch(brand=None,market=None):
    return dbconn.query(u"select * from naifenitem where brand = $brand and market = $market and itemid not in (select itemid from formalprmatch where market=$market)",vars=dict(brand=brand,market=market))

def getPreNf(brand=None):
    return dbconn.query(u"select * from prenaifen where brand = $brand",vars=dict(brand=brand))


def deallater(itemid,market):
    dbconn.update("naifenitem",where="itemid=$itemid and market=$market",vars=dict(itemid=itemid,market=market),matchlater=1)


def insertPreNf(itemid,market):
    dbconn.query("insert into prenaifen name, duration, weight, spec, brand, series, sellto, age, duan, pack, place, price, img select from naifenitem name, duration, weight, spec, brand, series, sellto, age, duan, pack, place, price, img where itemid=$itemid and market=$market",vars=dict(itemid=itemid,market=market))
    r = web.listget(dbconn.query("select last_insert_id() as lastid"),0,None)
    return r.lastid


def insertmap(itemid,prid,market):
    dbconn.insert("formalprmatch",itemid=itemid,prid=prid,market=market)



