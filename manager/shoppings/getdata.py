#coding:utf-8

import json,re,time,traceback
from manager.models.shoppings import Shoppingitem
from helpers.loggers import get_logger
from helpers.crawls import failurecount
from datetime import datetime

comp_pid = re.compile("pid=([0-9-]+)")

def getItems(html):
    data = json.loads(html.decode("gbk"))

    if not data.has_key("itemList"):
        if data.has_key("status"):
            get_logger("crawl").debug("crawl spitemlist exp:"+ (str(data["status"]["code"]) + ":" +data["status"]["url"] if data["status"].has_key("code") else html) )
        else:
            get_logger("crawl").debug(html)
        global failurecount
        failurecount += 1
        return None
    if not data["itemList"]:
        get_logger("crawl").debug("itemlist is null")
        return None
        
    itemdatalist = data["itemList"]
    itemlist = list()

    for itemdata in itemdatalist:
        print itemdata
        item = Shoppingitem()
        item.originalImage = itemdata["originalImage"] if itemdata.has_key("originalImage") else None
        item.image = itemdata["image"]
        item.tip = itemdata["tip"]
        item.fullTitle = itemdata["fullTitle"] if itemdata.has_key("fullTitle") else None
        item.price = float(itemdata["price"]) if itemdata["price"] else None
        item.currentPrice = float(itemdata["currentPrice"]) if itemdata["currentPrice"] else None
        item.vipPrice = float(itemdata["vipPrice"]) if itemdata["vipPrice"] else None
        item.ship = float(itemdata["ship"]) if itemdata["ship"] else None
        item.tradeNum = int(itemdata["tradeNum"]) if itemdata["tradeNum"] else None
        item.smallNick = itemdata["smallNick"] if itemdata.has_key("smallNick") else None
        item.nick = itemdata["nick"]
        item.sellerId = int(itemdata["sellerId"]) if itemdata["sellerId"] else None
        item.itemId = int(itemdata["itemId"]) if itemdata["itemId"] else None
        item.isLimitPromotion = int(itemdata["isLimitPromotion"]) if itemdata["isLimitPromotion"] else None
        item.loc = itemdata["loc"]
        item.storeLink = itemdata["storeLink"]
        item.href = itemdata["href"]
        item.commend = int(itemdata["commend"]) if itemdata["commend"] else None
        item.commendHref = itemdata["commendHref"] 
        item.multipic = int(itemdata["multipic"]) if itemdata["multipic"] else None
        item.source = itemdata["source"]
        if itemdata["sameItemInfo"]:
            item.sameItemInfoCount = int(itemdata["sameItemInfo"]["count"]) if itemdata["sameItemInfo"]["count"] else None
            item.sameItemInfoUrl = itemdata["sameItemInfo"]["url"] 
            if item.sameItemInfoUrl:
                m = comp_pid.search(item.sameItemInfoUrl)
                item.pid = int(m.group(1)) if m else None
        item.ratesum = int(itemdata["ratesum"]) if itemdata["ratesum"] else None
        item.ratesumImg = itemdata["ratesumImg"] if itemdata["ratesumImg"] else None
        item.goodRate = float(itemdata["goodRate"].replace("%","")) if itemdata["goodRate"] else None
        item.dsrScore = float(itemdata["dsrScore"]) if itemdata["dsrScore"] else None
        itemlist.append(item)

    return itemlist


comp_30sell = re.compile("quanity: (\d+),")
comp_30sell_interval = re.compile("interval: (\d+)")

def get30sell(html):
    m = comp_30sell.search(html)
    if m:
        m1 = comp_30sell_interval.search(html)
        if m1:
            return int(m.group(1)),int(m1.group(1))
        return int(m.group(1)),None
    return None,None


comp_browsenum = re.compile('\"ICVT_7_\d+\":(\d+)')
comp_sharenum = re.compile('\"DFX_200_1_\d+\":(\d+)')
comp_storenumun = re.compile('\"SCCP_2_\d+\":(\d+)')
comp_favournum = re.compile('\"ICCP_1_\d+\":(\d+)')

def getItemBFS(html):
 
    m = comp_browsenum.search(html)
    browsenum = m.group(1) if m else None

    m = comp_sharenum.search(html)
    sharenum = m.group(1) if m else None

    m = comp_storenumun.search(html)
    storenumun = m.group(1) if m else None

    m = comp_favournum.search(html)
    favournum = m.group(1) if m else None

    return browsenum,sharenum,storenumun,favournum


comp_timelimit_txt = re.compile("valLimitPromInfo: {(.+?)}")
comp_timelimit = re.compile("timeLeft.+?(\d+)")

def getItemTimeLimit(html):
    m = comp_timelimit_txt.search(html)
    if m:
        txt = m.group(1)
        m1 =  comp_timelimit.search(txt)
        if m1:
            return int(m1.group(1))    

"""
抽取price中第一个sku的价格列表并转化为
[(unix_time,price),...]
"""

comp_priceCutData = re.compile("{.+}")
def getItemPriceCutData(html):

    m = comp_priceCutData.search(html)
    html = m.group()
    html = re.sub(r"new Date\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)",r"\1$\2$\3$\4",html)

    html = re.sub(r"{\s*(\w)", r'{"\1', html)
    html = re.sub(r",\s*(\w)", r',"\1', html)
    html = re.sub(r"(\w)\s*:", r'\1":', html)
    html = re.sub(r"(\w)\s*," , r'\1",',html)
    html = re.sub(r"(\w)\s*}" , r'\1"}',html)
    html = re.sub(r":\s*(\w)" , r':"\1',html)
    html = re.sub(r"(\w)\s*]" , r'\1"]',html)

    html = re.sub(r"\'" , '"',html)
    


    data = json.loads(html.decode("gbk"))
    if not data.has_key("price"):
        return None
    if len(data["price"]) == 0:
        return None
    pricelist = list()
    for price in data["price"][0]["data"]:
        y = None
        try:
            y = float(price["y"])
        except:
            get_logger("crawl").debug(traceback.format_exc()) 
        x = None
        try:
            xs = price["x"].split("$")
            x = time.mktime(datetime(int(xs[0]),int(xs[1]),int(xs[2])).timetuple())
        except:
            get_logger("crawl").debug(traceback.format_exc())
        if x is None or y is None:
            continue
        pricelist.append((x,y))

    return pricelist
        ##pricelist.append((price["x"],price["y"]))
        

    
    
