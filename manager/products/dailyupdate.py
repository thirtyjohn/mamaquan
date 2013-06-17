#coding:utf8
from manager.settings import dbconn
from helpers.b2c import factory
from datetime import datetime,timedelta
import web

def getPrToUpdate(brand=None,hours=None):
    utime = datetime.now() + timedelta(hours=hours) if hours else None
    return dbconn.query("select * from formalnaifen where status=1" 
                                                     +(" and brand = $brand" if brand else "") 
                                                     + (" and utime < $utime" if utime else ""),
            vars=dict(brand=brand,utime=utime))



def startupdate(brand=None,market=None,hours=None):
    prs = getPrToUpdate(brand=brand,hours=hours)
    for pr in prs:
        prms = dbconn.query("select * from prmatch where prid = $prid" + (" and market=$market" if market else ""),vars=dict(prid=pr.ID,market=market))
        for prm in prms:
            updatePrm(prm)
        minprm = getMinPrice(pr.ID)
        dbconn.update("formalnaifen",where="id=$prid",vars=dict(prid=pr.ID),market=minprm.market,price=minprm.price,promo=minprm.promo,utime=datetime.now())



def updatePrm(prm):
    ## update price,promo
    b2c_item = factory(prm.market)
    b2c_item.itemid = prm.itemid

    price = b2c_item.getPrice()
    ##promo = b2c_item.getPromo()

    dbconn.insert("pricelog",market=prm.market,itemid=prm.itemid,price=price,wdate=datetime.now())

    dbconn.update("prmatch",where="market=$market and itemid=$itemid",vars=dict(market=prm.market,itemid=prm.itemid),price=price,utime=datetime.now())


def getMinPrice(prid):
    return web.listget(dbconn.query("select * from prmatch where prid = $prid order by price limit 1",vars=dict(prid=prid)),0,None)
