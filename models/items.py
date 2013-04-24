#coding:utf-8
from settings import dbconn

class Item:
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

    def insert(self):
        dbconn.insert("shoppingitem",
                    originalImage = self.originalImage,
                    image = self.image,
                    tip = self.tip,
                    fullTitle = self.fullTitle,
                    price = self.price,
                    currentPrice = self.currentPrice,
                    vipPrice = self.vipPrice,
                    ship = self.ship,
                    tradeNum = self.tradeNum,
                    smallNick = self.smallNick,
                    nick = self.nick,
                    sellerId = self.sellerId,
                    itemId = self.itemId,
                    isLimitPromotion = self.isLimitPromotion,
                    loc = self.loc,
                    storeLink = self.storeLink,
                    href = self.href,
                    commend = self.commend,
                    commendHref = self.commendHref,
                    multipic = self.multipic,
                    source = self.source,
                    sameItemInfoCount = self.sameItemInfoCount,
                    sameItemInfoUrl = self.sameItemInfoUrl,
                    ratesum = self.ratesum,
                    ratesumImg = self.ratesumImg,
                    goodRate = self.goodRate,
                    dsrScore = self.dsrScore,
                    pid = self.pid,
                    itemclass = self.itemclass
        )

def insertpreitem(item,pid=None,picked=None,itemclass=None):
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
                    itemclass = itemclass,
                    pid = pid,
                    picked = picked
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
