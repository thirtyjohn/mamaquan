#coding:utf8
from manager.settings import dbconn
from helpers.b2c import factory
from datetime import datetime,timedelta
import web,traceback
from helpers.loggers import get_logger

def getNfToUpdate(brands=None,hours=None):
    utime = datetime.now() - timedelta(hours=hours) if hours else None
    return dbconn.query("""
                    select p.* from formalproduct p 
                        join formalnaifen n
                        on p.id = n.id and p.status=1
                    """
                    +(" and n.brand in $brands" if brands else "")
                    + (" and (p.utime < $utime or p.utime is null)" if utime else ""),
            vars=dict(brands=brands,utime=utime))







def updatePrm(prm):
    ## update price,promo
    b2c_item = factory(prm.market)
    b2c_item.itemid = prm.itemid

    price = b2c_item.getPrice()
    ##promo = b2c_item.getPromo()

    dbconn.insert("pricelog",market=prm.market,itemid=prm.itemid,price=price,wdate=datetime.now())

    dbconn.update("formalprmatch",where="market=$market and itemid=$itemid",vars=dict(market=prm.market,itemid=prm.itemid),price=price,utime=datetime.now(),syn=0)


def getMinPrice(prid):
    return web.listget(dbconn.query("select * from formalprmatch where prid = $prid order by price limit 1",vars=dict(prid=prid)),0,None)


def startupdate(prtype,brands=None,market=None,hours=None):
    prs = list()
    if prtype == "naifen":
        prs = getNfToUpdate(brands=brands,hours=hours)
    for pr in prs:
        try:
            prms = dbconn.query("select * from formalprmatch where prid = $prid" + (" and market=$market" if market else ""),vars=dict(prid=pr.ID,market=market))
            for prm in prms:
                updatePrm(prm)
            minprm = getMinPrice(pr.ID)
            dbconn.update("formalproduct",where="id=$prid",vars=dict(prid=pr.ID),market=minprm.market,price=minprm.price,promo=minprm.promo,utime=datetime.now(),syn=0)
        except:
            get_logger("general").debug(traceback.format_exc())




