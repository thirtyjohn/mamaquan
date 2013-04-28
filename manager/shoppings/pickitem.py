#coding:utf-8

import origindata,getdata,analydata 
from manager.settings import localdir,dbconn
import web
from manager.models import shoppings
from datetime import datetime

def collect(itemclass):
    html = origindata.getListHtml(itemclass)


    items = getdata.getItems(html)

    for item in items: 
        item = analydata.filter1st(item) ##第一道过滤
        if item:
            item.itemclass = itemclass
            item.insert()

def insertSameProduct(itemclass):
    sps = shoppings.getSpHasSameItem(itemclass)
    for item in sps: 
        html = origindata.getSameHtml(itemclass,item)
        
        ##f = open(localdir+"test","w")
        ##f.write(html)

        items = getdata.getItems(html)
        if not items:
            print "wowowo"
            continue
        for sameitem in items:
            if analydata.filter0st(sameitem): ##同款产品第一道过滤

                if sameitem.itemId == item.itemId:
                    shoppings.updateshoppingitem(sameitem.itemId,picked=1)
                else:
                    sameitem.pid = item.pid
                    sameitem.picked = 0
                    sameitem.itemclass = item.itemclass
                    shoppings.insertshoppingitem(sameitem)


def pickItemtoPre(itemclass):
    sps = shoppings.getOkspitems(itemclass)
    for sp in sps:
        shoppings.insertpreitem(sp)


def pickGoodItem(pid):
    items = list()
    res = shoppings.getPreShoppingsByPid(pid) 
    for r in res:
        if r.picked == 1:
            pickitem = r
        items.append(r)

    gooditem = analydata.compare(pickitem,items) 
    if gooditem:
        famitems = analydata.getFamitems(gooditem,items)
        shoppings.insertformalitem(gooditem,picked=1)
        for i in famitems:
            shoppings.insertformalitem(i,picked=0)


def pickPretoformal(itemclass):
    res = shoppings.getPrePids(itemclass) 
    for r in res:
        pickGoodItem(r.pid)


def updateFormalDetail(itemclass):
    res = shoppings.getFormaltoUpdate(itemclass) 
    for item in res:
        pagesource = origindata.getItemHtml(item)
        itemBFSHtml = origindata.getItemBFSHtml(pagesource)
        browsenum,sharenum,storenumun,favournum = getdata.getItemBFS(itemBFSHtml)
        promoteTimeLimit = getdata.getItemTimeLimit(pagesource)
        tradenum30html = origindata.get30sellhtml(item)
        tradenum30,tradenum30_interval = getdata.get30sell(tradenum30html)
        shoppings.updateFormal(item.itemId,
                        browsenum = browsenum,
                        sharenum = sharenum,
                        storenumun = storenumun,
                        favournum = favournum,
                        promoteTimeLimit = promoteTimeLimit,
                        udate = datetime.now()
        )
    


def startupdate(itemclass):
    collect(itemclass)
    insertSameProduct(itemclass)
    pickItemtoPre(itemclass)
    pickPretoformal(itemclass)
    shoppings.updateprocess(itemclass)
    updateFormalDetail(itemclass)

