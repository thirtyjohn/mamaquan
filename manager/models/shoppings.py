#coding:utf-8
from manager.settings import dbconn
import web
from datetime import datetime

def getPickedSps(itemclass):
    return dbconn.query("select * from shoppingitem where itemclass = $itemclass and processed=0 and picked=1",vars=dict(itemclass=itemclass))

def getSpHasSameItem(itemclass):
    return dbconn.query("select * from shoppingitem where sameiteminfocount > 1 and itemclass = $itemclass and processed=0",vars=dict(itemclass=itemclass))


def getPidsToCp(itemclass):
    return dbconn.query("select pid from shoppingitem where processed = 0 and pid is not null and itemclass=$itemclass group by pid having count(*) > 1",vars=dict(itemclass=itemclass))

def getSpItemsByPid(pid):
    return dbconn.query("select * from shoppingitem where pid = $pid and processed=0", vars=dict(pid=pid))

def getOkspitems(itemclass):
    return dbconn.query("""
        select * from shoppingitem s
            join (select pid from shoppingitem where processed = 0 and itemclass = $itemclass group by pid having count(*)>1) t
        on s.pid = t.pid and s.processed = 0
    """,vars=dict(itemclass=itemclass))

def getPrePids(itemclass):
    return dbconn.query("select distinct pid from preshopping where itemclass = $itemclass and processed=0", vars=dict(itemclass=itemclass))




def getFormaltoUpdate(itemclass):
    return dbconn.query("select * from formalshopping where picked = 1 and itemclass = $itemclass and processed=0",vars=dict(itemclass=itemclass))

def getFormaltoShopping(itemclass):
    return dbconn.query("select * from formalshopping where itemclass = $itemclass and processed=0",vars=dict(itemclass=itemclass))


def updateShoppingProcess(itemclass):
    dbconn.update("shoppingitem",where="itemclass=$itemclass and processed=0",vars=dict(itemclass=itemclass),processed=1)
    dbconn.update("preshopping",where="itemclass=$itemclass and processed=0",vars=dict(itemclass=itemclass),processed=1)
    dbconn.update("formalshopping",where="itemclass=$itemclass and processed=0",vars=dict(itemclass=itemclass),processed=1)


def updateFormal(itemid,**values):
    dbconn.update("formalshopping",where="itemid=$itemid",vars=dict(itemid=itemid),**values)


def updateshoppingitem(itemid,**values):
    dbconn.update("shoppingitem",where="itemid=$itemid",vars=dict(itemid=itemid),**values)


def hasShoppingitembyItemid(itemid):
    return web.listget(dbconn.query("select * from shoppingitem where itemid=$itemid",vars=dict(itemid=itemid)),0,None)

class Shoppingitem:
    def __init__(self):
        self.originalImage = None
        self.image = None
        self.tip = None
        self.fullTitle = None
        self.price = None
        self.currentPrice = None
        self.vipPrice = None
        self.ship = None
        self.tradeNum = None
        self.smallNick = None
        self.nick = None
        self.sellerId = None
        self.itemId = None
        self.isLimitPromotion = None
        self.loc = None
        self.storeLink = None
        self.href = None
        self.commend = None
        self.commendHref = None
        self.multipic = None
        self.source = None
        self.sameItemInfoCount = None
        self.sameItemInfoUrl = None
        self.ratesum = None
        self.ratesumImg = None
        self.goodRate = None
        self.dsrScore = None
        self.pid = None
        self.itemclass = None
        self.picked = None

def insertshoppingitem(item):
    dbconn.insert("shoppingitem",
                    originalImage = item.originalImage,
                    image = item.image,
                    tip = item.tip,
                    fullTitle = item.fullTitle,
                    price = item.price,
                    currentPrice = item.currentPrice,
                    vipPrice = item.vipPrice,
                    ship = item.ship,
                    tradeNum = item.tradeNum,
                    smallNick = item.smallNick,
                    nick = item.nick,
                    sellerId = item.sellerId,
                    itemId = item.itemId,
                    isLimitPromotion = item.isLimitPromotion,
                    loc = item.loc,
                    storeLink = item.storeLink,
                    href = item.href,
                    commend = item.commend,
                    commendHref = item.commendHref,
                    multipic = item.multipic,
                    source = item.source,
                    sameItemInfoCount = item.sameItemInfoCount,
                    sameItemInfoUrl = item.sameItemInfoUrl,
                    ratesum = item.ratesum,
                    ratesumImg = item.ratesumImg,
                    goodRate = item.goodRate,
                    dsrScore = item.dsrScore,
                    pid = item.pid,
                    picked = item.picked,
                    itemclass = item.itemclass,
                    wdate = datetime.now()
        )


def insertpreshopping(item):
    dbconn.insert("preshopping",
                    originalImage = item.originalImage,
                    image = item.image,
                    tip = item.tip,
                    fullTitle = item.fullTitle,
                    price = item.price,
                    currentPrice = item.currentPrice,
                    vipPrice = item.vipPrice,
                    ship = item.ship,
                    tradeNum = item.tradeNum,
                    smallNick = item.smallNick,
                    nick = item.nick,
                    sellerId = item.sellerId,
                    itemId = item.itemId,
                    isLimitPromotion = item.isLimitPromotion,
                    loc = item.loc,
                    storeLink = item.storeLink,
                    href = item.href,
                    commend = item.commend,
                    commendHref = item.commendHref,
                    multipic = item.multipic,
                    source = item.source,
                    sameItemInfoCount = item.sameItemInfoCount,
                    sameItemInfoUrl = item.sameItemInfoUrl,
                    ratesum = item.ratesum,
                    ratesumImg = item.ratesumImg,
                    goodRate = item.goodRate,
                    dsrScore = item.dsrScore,
                    itemclass = item.itemclass,
                    pid = item.pid,
                    picked = item.picked,
                    wdate = datetime.now()
        )

def insertformalshopping(item,picked=None):
    dbconn.insert("formalshopping",
                    originalImage = item.originalImage,
                    image = item.image,
                    tip = item.tip,
                    fullTitle = item.fullTitle,
                    price = item.price,
                    currentPrice = item.currentPrice,
                    vipPrice = item.vipPrice,
                    ship = item.ship,
                    tradeNum = item.tradeNum,
                    smallNick = item.smallNick,
                    nick = item.nick,
                    sellerId = item.sellerId,
                    itemId = item.itemId,
                    isLimitPromotion = item.isLimitPromotion,
                    loc = item.loc,
                    storeLink = item.storeLink,
                    href = item.href,
                    commend = item.commend,
                    commendHref = item.commendHref,
                    multipic = item.multipic,
                    source = item.source,
                    sameItemInfoCount = item.sameItemInfoCount,
                    sameItemInfoUrl = item.sameItemInfoUrl,
                    ratesum = item.ratesum,
                    ratesumImg = item.ratesumImg,
                    goodRate = item.goodRate,
                    dsrScore = item.dsrScore,
                    itemclass = item.itemclass,
                    pid = item.pid,
                    picked = item.picked,
                    browsenum = item.browsenum,
                    sharenum = item.sharenum,
                    favournum = item.favournum,
                    promoteTimeLimit = item.promoteTimeLimit,
                    udate = item.udate,
                    wdate = datetime.now()
        )


def insertShopping(item):
    dbconn.insert("shopping",
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
                    score = item.generalscore,
                    itemclass = item.itemclass,
                    picked = item.picked,
                    udate = item.udate,
                    wdate = datetime.now()
    )
