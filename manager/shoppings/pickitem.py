#coding:utf-8

import origindata,getdata,analydata 
from manager.settings import localdir,dbconn
import web
from manager.models import shoppings
from datetime import datetime
from helpers.loggers import get_logger
import traceback

def collect(itemclass):
    newcount = 0
    samecount = 0
    html = origindata.getListHtml(itemclass)

    if not html:
        return

    items = getdata.getItems(html)

    for item in items: 
        item = analydata.filter1st(item) ##第一道过滤
        if item:
            newcount += 1
            item.itemclass = itemclass
            if not shoppings.hasShoppingitembyItemid(item.itemId):
                item.picked=1
                shoppings.insertshoppingitem(item)
            else:
                samecount += 1

    get_logger("tactics").info(itemclass+",list,handle: "+str(newcount)+" same: "+str(samecount))

def insertSameProduct(itemclass):
    samecount = 0
    samitemcount = 0
    sps = shoppings.getSpHasSameItem(itemclass)
    for item in sps: 
        html = origindata.getSameHtml(itemclass,item)
        if not html:
            return 
        ##f = open(localdir+"test","w")
        ##f.write(html)
        items = getdata.getItems(html)
        if not items:
            continue
        
        for sameitem in items:
            if analydata.filter0st(sameitem): ##同款产品第一道过滤
                if sameitem.itemId == item.itemId:
                    pass
                else:
                    samitemcount += 1
                    if not shoppings.hasShoppingitembyItemid(sameitem.itemId):
                        sameitem.pid = item.pid
                        sameitem.picked = 0
                        sameitem.itemclass = item.itemclass
                        shoppings.insertshoppingitem(sameitem)
                    else:
                        samecount += 1

    get_logger("tactics").info(itemclass+",samelist,handle: "+str(samitemcount)+" same: "+str(samecount))


def pickItemtoPre(itemclass):
    sps = shoppings.getOkspitems(itemclass)
    for sp in sps:
        shoppings.insertpreshopping(sp)


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
        if not pagesource:
            continue
        try:
            itemBFSHtml = origindata.getItemBFSHtml(pagesource)
            browsenum,sharenum,storenumun,favournum = getdata.getItemBFS(itemBFSHtml)
            promoteTimeLimit = getdata.getItemTimeLimit(pagesource)
            ##tradenum30html = origindata.get30sellhtml(item)
            ##tradenum30,tradenum30_interval = getdata.get30sell(tradenum30html)
            shoppings.updateFormal(item.itemId,
                            browsenum = browsenum,
                            sharenum = sharenum,
                            storenumun = storenumun,
                            favournum = favournum,
                            promoteTimeLimit = promoteTimeLimit, 
                            udate = datetime.now()
            )
        except:
            get_logger("crawl").debug("%s %s",itemBFSHtml,traceback.format_exc())
    


def formaltoshopping(itemclass):
    items = shoppings.getFormaltoShopping(itemclass)
    for item in items:
        shoppings.insertShopping(item)

def startupdate(itemclass):
    try:
        collect(itemclass)
        insertSameProduct(itemclass)
        pickItemtoPre(itemclass)
        pickPretoformal(itemclass)
        updateFormalDetail(itemclass)
        shoppings.updateGeneralscore(itemclass)
        formaltoshopping(itemclass)
    except:
        get_logger("schedErrJob").debug("%s",traceback.format_exc())
    shoppings.updateShoppingProcess(itemclass)

