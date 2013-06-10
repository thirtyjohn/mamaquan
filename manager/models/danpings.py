#coding:utf-8
from manager.settings import dbconn
from datetime import datetime
import web
from helpers.utils import price


class Danping:
    def __init__(self):
        self.name = None
        self.price = None
        self.img = None
        self.market = None
        self.desp = None
        self.url = None
        self.itemclass = None
        self.currency = 1
        self.sourceid = None
        self.source = None
        self.redirecturl = None
        self.srcurl = None
        self.itemid = None


def insertDpitem(dp):
    dbconn.insert("danpingitem",
        name = dp.name, 
        price = dp.price,
        img = dp.img,
        market = dp.market,
        desp = dp.desp,
        url = dp.url,
        itemclass = dp.itemclass,
        currency = dp.currency,
        sourceid = dp.sourceid,
        source = dp.source,
        redirecturl = dp.redirecturl,
        srcurl = dp.srcurl,
        wdate = datetime.now(),
        itemid = dp.itemid
    )

def hasitem(sourceid,source):
    return web.listget(dbconn.query("select * from danpingitem where source=$source and sourceid=$sourceid",vars=dict(sourceid=sourceid,source=source)),0,None)

def findstatus(status):
    return dbconn.query("select * from danpingitem where status = $status",vars=dict(status=status))

def updatestatus(dpid,status):
    dbconn.update("danpingitem",where="id=$dpid",vars=dict(dpid=dpid),status=status)

def insertmatch(dpid,d):
    dbconn.insert("danpingmatch",
                dpid = dpid,
                market = d.market,
                price = d.price,
                currency = d.currency,
                url = d.url,
                wdate = datetime.now()
    )

def getmatch_min(dpid):
    pricelist = list()
    res = dbconn.query("select min(price) as minprice,currency from danpingmatch where dpid = $dpid group by currency",vars=dict(dpid=dpid))
    for r in res:
        pricelist.append(price(r.minprice,r.currency))
    if len(pricelist) > 0:
        return min(pricelist)
    return None

def insert_formal(dp):
    dbconn.insert("formaldanping",
                    ID = dp.ID,
                    name = dp.name,
                    price = dp.price,
                    currency = dp.currency,
                    image = dp.image,
                    market = dp.market,
                    desp = dp.desp,
                    itemclass = dp.itemclass,
                    url = dp.srcurl,
                    source = dp.source,
                    itemid = dp.itemid,
                    wdate = datetime.now()
    )


def update(dpid,**values):
    dbconn.update("danpingitem",where="id=$dpid",vars=dict(dpid=dpid),**values)
    
