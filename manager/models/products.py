#coding:utf8
from manager.settings import dbconn
from datetime import datetime
import web
from helpers.b2c import Item


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


def insertNfitem(nf):
    dbconn.insert("naifenitem",itemid=nf.itemid,name=nf.name,price=nf.price,img=nf.img,market=nf.market,brand=nf.brand)

def getHost(brand=None,market=None,page=None):
    r = web.listget(dbconn.query("select url from mmlisturl where brand=$brand and market=$market",vars=dict(brand=brand,market=market)),0,None)
    return r.url + str(page)

def getNfitemNotProcessed(market=None,brand=None):
    return dbconn.query("select * from naifenitem where processed is null and market = $market and brand = $brand",vars=dict(market=market,brand=brand))

"""
批量插入预产品库,建立对应关系
"""
def batchInsertPreNf(market=None,brand=None):
    dbconn.query("insert into prenaifen (name,duration,weight,spec,brand,series,sellto,age,duan,pack,place,price,img) select name,duration,weight,spec,brand,series,sellto,age,duan,pack,place,price,img from naifenitem where brand = $brand and market = $market",vars=dict(brand=brand,market=market))
    res = dbconn.query(u"select * from prenaifen where brand = $brand",vars=dict(brand=brand))
    for r in res:
        res1  = dbconn.query(u"select * from naifenitem where name = $name and market=$market",vars=dict(name=r.name,market=market))
        item = web.listget(res1,0,None)
        dbconn.insert("formalprmatch",prid=r.ID,itemid=item.itemid,market=market)


def getNfitemNotMatch(brand=None,market=None):
    return dbconn.query(u"select * from naifenitem where brand = $brand and market = $market and itemid not in (select itemid from prmatch where market=$market)",vars=dict(brand=brand,market=market))

def getPreNf(brand=None):
    return dbconn.query(u"select * from prenaifen where brand = $brand",vars=dict(brand=brand))


def deallater(itemid,market):
    dbconn.update("naifenitem",where="itemid=$itemid and market=$market",vars=dict(itemid=itemid,market=market),matchlater=1)


def insertPreNf(itemid,market):
    dbconn.query("insert into prenaifen name, duration, weight, spec, brand, series, sellto, age, duan, pack, place, price, img select from naifenitem name, duration, weight, spec, brand, series, sellto, age, duan, pack, place, price, img where itemid=$itemid and market=$market",vars=dict(itemid=itemid,market=market))
    r = web.listget(dbconn.query("select last_insert_id() as lastid"),0,None)
    return r.lastid


def insertmap(itemid,prid,market):
    dbconn.insert("prmatch",itemid=itemid,prid=prid,market=market)



