#coding:utf-8

import origindata,getdata,analydata 
import traceback
from manager.models import shoppings
from datetime import datetime
from helpers.loggers import get_logger
from tactics import pagetocrawl
from helpers.prices import getRuyiHtml,getRuyiPrice

def collectpage(itemclass,page):
    newcount = 0
    samecount = 0
    html = origindata.getListHtml(itemclass,page)

    if not html:
        return

    items = getdata.getItems(html)
    if not items:
        return

    for item in items: 
        item = analydata.filterFromList(item) ##第一道过滤
        if item:
            newcount += 1
            item.itemclass = itemclass
            if not shoppings.hasShoppingitembyItemid(item.itemId):
                item.picked=1
                shoppings.insertshoppingitem(item)
            else:
                samecount += 1

    get_logger("tactics").info(itemclass+",list,page:"+str(page)+",handle: "+str(newcount)+" same: "+str(samecount))

def collect(itemclass):
    for page in pagetocrawl[itemclass]:
        try:
            collectpage(itemclass,page=page)
        except:
            get_logger("schedErrJob").debug("%s",traceback.format_exc())

def insertSameProduct(itemclass):
    samecount = 0
    samitemcount = 0
    sps = shoppings.getSpHasSameItem(itemclass)
    for item in sps:
        try:
            html = origindata.getSameHtml(itemclass,item)
            if not html:
                return 
            ##f = open(localdir+"test","w")
            ##f.write(html)
            items = getdata.getItems(html)
            if not items:
                continue
            
            for sameitem in items:
                if analydata.filterSameItem(sameitem): ##同款产品第一道过滤
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
        except:
            get_logger("schedErrJob").debug("%s",traceback.format_exc())

    get_logger("tactics").info(itemclass+",samelist,handle: "+str(samitemcount)+" same: "+str(samecount))



def calCpRank(itemclass):
    p_res = shoppings.getPidsToCp(itemclass)
    for p in p_res:
        try:
            items = list()
            res = shoppings.getSpItemsByPid(p.pid) 
            for r in res:
                if r.picked == 1:
                    pickitem = r
                items.append(r)
            cprank = analydata.compare(pickitem,items)
            shoppings.updateshoppingitem(pickitem.itemId,cprank=cprank)
        except:
            get_logger("schedErrJob").debug("%s",traceback.format_exc())



def updateItemRank(itemclass): 
    sps = shoppings.getPickedSps(itemclass)
    for sp in sps:
        try:
            shoppings.updateshoppingitem(sp.itemId,itemrank=analydata.calItemRank(sp) )
        except:
            get_logger("schedErrJob").debug("%s",traceback.format_exc())



def updateItemDetail(itemclass):
    items = shoppings.getPickedSps(itemclass)
    for item in items:
        try:
            pagesource = origindata.getItemHtml(item)
            if not pagesource:
                continue
            itemBFSHtml = origindata.getItemBFSHtml(pagesource)
            browsenum,sharenum,storenumun,favournum = getdata.getItemBFS(itemBFSHtml)
            promoteTimeLimit = getdata.getItemTimeLimit(pagesource)
            ##tradenum30html = origindata.get30sellhtml(item)
            ##tradenum30,tradenum30_interval = getdata.get30sell(tradenum30html)
            shoppings.updateshoppingitem(item.itemId,
                            browsenum = browsenum,
                            sharenum = sharenum,
                            favournum = favournum,
                            promoteTimeLimit = promoteTimeLimit, 
                            udate = datetime.now()
            )
        except:
            get_logger("schedErrJob").debug("%s %s",itemBFSHtml,traceback.format_exc())


def updateItemChange(itemclass):
    items = shoppings.getPickedSps(itemclass)
    for item in items:
        try:
            html = origindata.getItemPriceCutHtml(item)
            prices = getdata.getItemPriceCutData(html) if html else None
            if not prices:
                html = getRuyiHtml(item.href)
                prices = getRuyiPrice(html) if html else None
            if not prices:
                continue
            changerank = analydata.calChange(item.currentPrice,prices)
            shoppings.updateshoppingitem(item.itemId,changerank=changerank)
        except:
            get_logger("schedErrJob").debug("%s",traceback.format_exc())


def pickGoodItems(itemclass):
    sps = shoppings.getPickedSps(itemclass)
    for sp in sps:
        try:
            if analydata.isGoodItem(sp):
                score = analydata.computescore(sp)
                shoppings.insertformalshopping(sp,score=score)
                if not sp.pid:
                    continue
                res = shoppings.getSpItemsByPid(sp.pid)
                items = list()
                for r in res:
                    items.append(r)
                for famitem in analydata.getFamitems(items):
                    shoppings.insertformalshopping(famitem)
        except:
            get_logger("schedErrJob").debug("%s",traceback.format_exc())

"""        
def formaltoshopping(itemclass):
    items = shoppings.getFormaltoShopping(itemclass)
    for item in items:
        shoppings.insertShopping(item)
"""

def startupdate(itemclass):
    try:
        collect(itemclass)
        insertSameProduct(itemclass)
        calCpRank(itemclass)
        updateItemDetail(itemclass)
        updateItemRank(itemclass)
        updateItemChange(itemclass)
        pickGoodItems(itemclass)
        ##formaltoshopping(itemclass)
    except:
        get_logger("schedErrJob").debug("%s",traceback.format_exc())
    shoppings.updateShoppingProcess(itemclass)


##pickItemtoPre(itemclass)
        ##pickPretoformal(itemclass)
        ##updateFormalDetail(itemclass)
        ##shoppings.updateGeneralscore(itemclass)
