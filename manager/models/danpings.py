#coding:utf-8
from manager.settings import dbconn
from datetime import datetime
import web


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
        self.itemid = None
        self.source = None
        self.redirecturl = None


def insertDpitem(dp):
    print type(dp.name)
    print type(dp.desp)
    print type(dp.market)
    dbconn.insert("danpingitem",
        name = dp.name, 
        price = dp.price,
        img = dp.img,
        market = dp.market,
        desp = dp.desp,
        url = dp.url,
        itemclass = dp.itemclass,
        currency = dp.currency,
        itemid = dp.itemid,
        source = dp.source,
        redirecturl = dp.redirecturl,
        wdate = datetime.now()
    )

def hasitem(itemid,source):
    return web.listget(dbconn.query("select * from danpingitem where source=$source and itemid=$itemid",vars=dict(itemid=itemid,source=source)),0,None)
