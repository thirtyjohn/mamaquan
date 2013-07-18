#coding:utf-8
import traceback
from datetime import datetime
from manager.settings import dbconn,syndbconn,serverdbconn
from helpers.loggers import get_logger


def syndp():
    res = dbconn.query("select * from formaldanping where syn=0")
    for r in res:
        syndbconn.insert("danping",
                ID = r.ID,
                name = r.name,
                price = r.price,
                currency = r.currency,
                image = r.image,
                market = r.market,
                desp = r.desp,
                itemclass = r.itemclass,
                url = r.url,
                wdate = r.wdate,
                source = r.source,
                status = r.status,
                itemid = r.itemid
        )
        serverdbconn.insert("danping",
                ID = r.ID,
                name = r.name,
                price = r.price,
                currency = r.currency,
                image = r.image,
                market = r.market,
                desp = r.desp,
                itemclass = r.itemclass,
                url = r.url,
                wdate = r.wdate,
                source = r.source,
                status = r.status,
                itemid = r.itemid
        )
        dbconn.update("formaldanping",where="id=$dpid",vars=dict(dpid=r.ID),syn=1)

    res = dbconn.query("select * from formaldanping where syn=2")
    for r in res:
        syndbconn.update("danping",where="id=$dpid",vars=dict(dpid=r.ID),stock=r.stock)
        serverdbconn.update("danping",where="id=$dpid",vars=dict(dpid=r.ID),stock=r.stock)
        dbconn.update("formaldanping",where="id=$dpid",vars=dict(dpid=r.ID),syn=1)


def syndpmatch():
    res = dbconn.query("select * from danpingmatch where syn=0")
    for r in res:
        syndbconn.insert("danpingmatch",
            dpid = r.dpid, 
            market = r.market, 
            price = r.price, 
            currency = r.currency, 
            url = r.url, 
            wdate =r.wdate, 
            img = r.img
        )
        serverdbconn.insert("danpingmatch",
            dpid = r.dpid, 
            market = r.market, 
            price = r.price, 
            currency = r.currency, 
            url = r.url, 
            wdate =r.wdate, 
            img = r.img
        )
        dbconn.update("danpingmatch",where="dpid=$dpid and market=$market", vars=dict(dpid=r.dpid,market=r.market),syn=1)


def synsp():
    res = dbconn.query("select * from formalshopping where syn = 0")
    for item in res:
        syndbconn.insert("shopping",
                    ID = item.ID,
                    itemId = str(item.itemId),
                    pid = str(item.pid),
                    bigimg = item.originalImage,
                    img = item.image,
                    name = item.tip,
                    price = item.currentPrice,
                    pricebefore = item.price,
                    ship = item.ship,
                    promotetype = 1 if item.isLimitPromotion==1 else None,
                    promoteTimeLimit = item.promoteTimeLimit,
                    tradeNum = item.tradeNum,
                    commend = item.commend,
                    sellername = item.nick,
                    sellerid = item.sellerId,
                    sellerloc = item.loc,
                    sellerrank = item.ratesum,
                    score = item.score,
                    itemclass = item.itemclass,
                    picked = item.picked,
                    udate = item.udate,
                    wdate = datetime.now()
        )

        serverdbconn.insert("shopping",
                    ID = item.ID,
                    itemId = str(item.itemId),
                    pid = str(item.pid),
                    bigimg = item.originalImage,
                    img = item.image,
                    name = item.tip,
                    price = item.currentPrice,
                    pricebefore = item.price,
                    ship = item.ship,
                    promotetype = 1 if item.isLimitPromotion==1 else None,
                    promoteTimeLimit = item.promoteTimeLimit,
                    tradeNum = item.tradeNum,
                    commend = item.commend,
                    sellername = item.nick,
                    sellerid = item.sellerId,
                    sellerloc = item.loc,
                    sellerrank = item.ratesum,
                    score = item.score,
                    itemclass = item.itemclass,
                    picked = item.picked,
                    udate = item.udate,
                    wdate = datetime.now()
        )

        dbconn.update("formalshopping",where="id=$spid", vars=dict(spid=item.ID),syn=1)


def synpr():
    res = dbconn.query("select * from formalproduct where syn = 0")
    for r in res:
        syndbconn.update("product",where = "id=$prid",vars=dict(prid=r.ID),price=r.price, market=r.market, promo=r.promo, stock=r.stock )
        serverdbconn.update("product",where = "id=$prid",vars=dict(prid=r.ID),price=r.price, market=r.market, promo=r.promo, stock=r.stock )
        dbconn.update("formalproduct",where="id=$prid", vars=dict(prid=r.ID),syn=1)

    res = dbconn.query("select * from formalprmatch where syn = 0")
    for r in res:
        syndbconn.update("prmatch",where = "prid=$prid and market=$market and itemid=$itemid",vars=dict(prid=r.prid,itemid=r.itemid,market=r.market),price=r.price, market=r.market, promo=r.promo, stock=r.stock, utime=r.utime )
        serverdbconn.update("prmatch",where = "prid=$prid and market=$market and itemid=$itemid",vars=dict(prid=r.prid,itemid=r.itemid,market=r.market),price=r.price, market=r.market, promo=r.promo, stock=r.stock, utime=r.utime )
        dbconn.update("formalprmatch",where = "prid=$prid and market=$market and itemid=$itemid",vars=dict(prid=r.prid,itemid=r.itemid,market=r.market), syn=1)


def main():
    try:
        syndp()
        syndpmatch()
    except:
        get_logger("schedErrJob").debug("%s",traceback.format_exc())
    try:
        synsp()
    except:
        get_logger("schedErrJob").debug("%s",traceback.format_exc())

    try:
        synpr()
    except:
        get_logger("schedErrJob").debug("%s",traceback.format_exc())
