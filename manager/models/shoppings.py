#coding:utf-8
from manager.settings import dbconn


def getSpHasSameItem(itemclass):
    return dbconn.query("select * from shoppingitem where sameiteminfocount > 1 and itemclass = $itemclass and processed=0",vars=dict(itemclass=itemclass))

def getOkspitems(itemclass):
    return dbconn.query("""
        select * from shoppingitem
        where
            process = 0
            and pid in (select pid from shoppingitem where process = 0 group by pid having count(*)>1))
            and itemclass = $itemclass
    """,vars=dict(itemclass=itemclass))

def getPrePids(itemclass):
    return dbconn.query("select distinct pid from preitem where itemclass = $itemclass and process=0", vars=dict(itemclass=itemclass))


def getPreShoppingsByPid(pid):
    return dbconn.query("select * from preitem where pid = $pid and process=0", vars=dict(pid=pid))


def updateprocess(itemclass):
    dbconn.update("shoppingtiem",where="itemclass=$itemclass and process=0",vars=dict(itemclass=itemclass),process=1)
    dbconn.update("preshopping",where="itemclass=$itemclass and process=0",vars=dict(itemclass=itemclass),process=1)


def getFormaltoUpdate(itemclass):
    return dbconn.query("select * from formalitem where picked = 1 and itemclass = $itemclass and processed=0",vars=dict(itemclass=itemclass))

def updateFormal(itemid,**values):
    dbconn.update("formalshopping",where="itemid=$itemid",vars=dict(itemid=itemid),**values)


def updateshoppingitem(itemid,**values):
    dbconn.update("shoppingitem",where="itemid=$itemid",vars=dict(itemid=itemid),**values)



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
                    itemclass = item.itemclass
        )


def insertpreitem(item):
    dbconn.insert("preitem",
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
                    picked = item.picked
        )

def insertformalitem(item,picked=None):
    dbconn.insert("formalitem",
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
                    picked = picked
        )

