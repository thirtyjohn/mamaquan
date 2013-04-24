#coding:utf-8

import origindata 
from getdata import getItems,get30sell,getItemBFS,getItemTimeLimit
import analydata 
from settings import localdir,dbconn
import web
from items import insertpreitem,insertformalitem

def collect(itemclass):
    html = origindata.getListHtml(itemclass)


    items = getItems(html)

    for item in items: 
        item = analydata.filter1st(item)
        if item:
            item.itemclass = itemclass
            item.insert()

def insertSameProduct(itemclass):
    res = dbconn.query("select * from shoppingitem where sameiteminfocount > 1 and itemclass = $itemclass",vars=dict(itemclass=itemclass))
    for item in res: 
        html = origindata.getSameHtml(itemclass,item)
        
        ##f = open(localdir+"test","w")
        ##f.write(html)

        items = getItems(html)
        if not items:
            print "wowowo"
            continue
        for sameitem in items:
            if analydata.filter0st(sameitem):
                if sameitem.itemId == item.itemId:
                    insertpreitem(sameitem,pid=item.pid,picked=True,itemclass=item.itemclass)
                else:
                    insertpreitem(sameitem,pid=item.pid,picked=False,itemclass=item.itemclass)


def pickGoodItem(pid):
    items = list()
    res = dbconn.query("select * from preitem where pid = $pid", vars=dict(pid=pid))
    for r in res:
        if r.picked == 1:
            pickitem = r
        items.append(r)

    gooditem = analydata.compare(pickitem,items) 
    if gooditem:
        famitems = analydata.getFamitems(gooditem,items)
        print gooditem
        insertformalitem(gooditem,picked=1)
        for i in famitems:
            insertformalitem(i,picked=0)


def pickGoodItems(itemclass):
    res = dbconn.query("select distinct pid from preitem where itemclass = $itemclass", vars=dict(itemclass=itemclass))
    for r in res:
        pickGoodItem(r.pid)

if __name__ == "__main__":
    res = dbconn.query("select * from formalitem where picked = 1 and tradenum30 is null")
    for item in res:
        pagesource = origindata.getItemHtml(item)
        itemBFSHtml = origindata.getItemBFSHtml(pagesource)
        browsenum,sharenum,storenumun,favournum = getItemBFS(itemBFSHtml)
        promoteTimeLimit = getItemTimeLimit(pagesource)
        tradenum30html = origindata.get30sellhtml(item)
        tradenum30,tradenum30_interval = get30sell(tradenum30html)
        dbconn.update("formalitem",where="itemid=$itemid",vars=dict(itemid=item.itemId),
                        browsenum = browsenum,
                        sharenum = sharenum,
                        storenumun = storenumun,
                        favournum = favournum,
                        promoteTimeLimit = promoteTimeLimit,
                        tradenum30 = tradenum30,
                        tradenum30_interval = tradenum30_interval
        )



