#coding:utf-8
import time
from datetime import datetime
from manager.settings import dbconn,syndbconn


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
                    name = item.fullTitle,
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


def main():
    while True:
        time.sleep(60)
        syndp()
        syndpmatch()
