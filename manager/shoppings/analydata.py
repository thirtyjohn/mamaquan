#coding:utf-8


"""
在打折列表时进行一次筛选，条件：
同款不超过20
原价与现价的差价大于20，超过8折
"""
def filter1st(item):
    if item.sameItemInfoCount > 20:
        return None
    if item.price - item.currentPrice < 20:
        return None
    if item.currentPrice/item.price > 0.8:
        return None
    return item

"""
同款进预库的时候把没有任何信用的踢出，暂时宽进
"""
def filter0st(item):
    """
    print item.tradeNum
    if item.tradeNum is None or item.tradeNum == 0:
        return None
    print item.ratesum 
    if item.ratesum is None or item.ratesum == 0:
        return None
    print item.commend
    if item.commend is None or item.commend == 0:
        return None
    """
    if item.ratesum is None or item.ratesum == 0:
        return None
    return item


"""
计算初步信用，主要考量销售量、评价数/销售量、店铺信用
"""
def computeCredit(item):
    a = item.tradeNum
    b = item.commend
    if b > a:
        b = a
    if a == 0:
        return 2.0*item.ratesum/20
    return 5.0*a/(a+10) + 3.0*b/a + 2.0*item.ratesum/20


def islowestprice(item,items):
    prices = list()
    for i in items:
        print i.currentPrice
        prices.append(i.currentPrice)
    return item.currentPrice <= min(prices)


"""
与平均值有一定的差距
"""
DIFF_MIN = 5
DIFF_MIN_RATE = 0.1

def avgfilter(item,items):
    sum = 0
    for i in items:
        sum = sum + i.currentPrice
    avg = sum*1.0/len(items)
    print "avg =" + str(avg) 
    diff = (avg-item.currentPrice)*1.0/item.currentPrice
    print "diff = " + str(diff)
    return diff > DIFF_MIN_RATE and avg-item.currentPrice > DIFF_MIN



"""
与中位数有一定的差距
"""
def midfilter(item,items):
    n = len(items)
    pricelist = list()
    for i in items:
        pricelist.append(i.currentPrice)
    pricelist.sort()
    mid = (pricelist[n/2-1] + pricelist[n/2])/2 if n%2 == 0 else pricelist[n/2]
    print "mid =" + str(mid)
    diff = (mid-item.currentPrice)*1.0/item.currentPrice
    print "diff =" + str(diff)
    return diff > DIFF_MIN_RATE and mid-item.currentPrice > DIFF_MIN
    

"""
与可信低价商品的差价在一定范围内
"""
X_MAX_DIFF_RATE = 0.05
X_MAX_DIFF = 100

def tinydif(x,y):
    return (x-y)/y < X_MAX_DIFF_RATE and x-y < X_MAX_DIFF


"""
取得可信低价商品：首先要可信，价格比原先的低，然后取信用值最高的
"""
CREDIT_GOOD = 3

def getXpickitem(item,items):
    bestitem  = None
    bestCredit = 0
    for i in items:
        if item.currentPrice > i.currentPrice:
            credit = computeCredit(i)
            if credit > CREDIT_GOOD and credit > bestCredit:
                bestCredit = credit
                bestitem = i
    return bestitem

"""
在比较同款商品时，过低的信用不进入样本
"""
CREDIT_LOWEST = 1

def compare(pickitem,items):
    itemlist = list()
    for item in items:
        item.credit = computeCredit(item)
        ##print str(item.ID)+":"+str(item.credit)
        if item.credit > CREDIT_LOWEST:
            itemlist.append(item)
  
    n = len(itemlist)
    ##print "count = " + str(n)
    """
    当样本不足2个时，则不入库
    """
    if n < 2:
        print "no enough goods"
        return None

    """
    如果pickitem是最低价，则需要于均值（平均数或中位数）有一定的差距，差距太小则不入库
    """
    if islowestprice(pickitem,items):
        print "it's lowest"
        if n == 2:
            if avgfilter(pickitem,items):
                return pickitem
            print "pirce is not good"
            return None
        else:
            if midfilter(pickitem,items):
                return pickitem
            print "pirce is not good"
            return None
    else:
        """
        如果不是最低价，则试图取出其他可信的低价商品，并对该商品重新进行验证
        """
        xpickeditem = getXpickitem(pickitem,itemlist)
        ##print xpickeditem
        if n == 2:
            if xpickeditem:
                return compare(xpickeditem,items)
            ##print "not enough good"
            return None
        elif n < 5:
            """
            如果有其他可信商品，且与原先差距不大，而与均值有差距，则可取。否则验证取出的。
            如果没有其他可信，则验证原先商品与均值差距，有则取，否则不入库
            """
            if xpickeditem:
                if tinydif(pickitem.currentPrice , xpickeditem.currentPrice) and avgfilter(pickitem,items):
                    return pickitem
                print "verify xitem"
                return compare(xpickeditem,items)
            return pickitem if avgfilter(pickitem,items) else None
        else:
            """
            与上面相似，只是把均值改成了中位数
            """
            if xpickeditem:
                if tinydif(pickitem.currentPrice , xpickeditem.currentPrice) and midfilter(pickitem,items):
                    return pickitem
                print "verify xitem"
                return compare(xpickeditem,items)
            return pickitem if midfilter(pickitem,items) else None



"""
在取相似产品时，超低价，不可信的就别出了
"""
FAM_MAX_LOW_DIFF = 0.1
FAM_MIN_CREDIT = 0.5

def toolow(x,y):
    return (y-x)/y > FAM_MAX_LOW_DIFF

def getFamitems(gooditem,items):
    famitems = list()
    for item in items:
        if item.ID == gooditem.ID:
            continue
        if item.currentPrice < gooditem.currentPrice and toolow(item.currentPrice , gooditem.currentPrice):
            continue
        if computeCredit(item) < FAM_MIN_CREDIT:
            continue
        famitems.append(item)
    return sorted(famitems,key=lambda item:computeCredit(item) ,reverse=True)



    
    


