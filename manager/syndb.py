#coding:utf-8

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

