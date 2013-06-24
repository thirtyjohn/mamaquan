#coding:utf-8
import tactics,time

"""
在打折列表时进行一次筛选
"""
def filterFromList(item):
    if item.sameItemInfoCount > tactics.MAX_SAMEITEM_COUNT:
        return None
    if item.price - item.currentPrice < tactics.MIN_DISCOUNT_PRICE:
        return None
    if item.currentPrice/item.price > tactics.MIN_DISCOUNT:
        return None
    return item

"""
同款进预库的时候把没有任何信用的踢出，暂时宽进
"""
def filterSameItem(item):
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
    if item.ratesum is None or item.ratesum < tactics.MIN_SAME_RATESUM:
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
        ##print i.currentPrice
        prices.append(i.currentPrice)
    return item.currentPrice <= min(prices)



def average(items):
    sum = 0
    for i in items:
        sum = sum + i.currentPrice
    avg = sum*1.0/len(items)
    return avg

"""
与平均值有一定的差距
"""
def avgfilter(item,items):
    avg = average(items)
    print "avg:" + str(avg)
    diff = (avg-item.currentPrice)*1.0/item.currentPrice
    print "diffrate:" + str(diff)
    print "diff:" + str(avg-item.currentPrice)
    return diff > tactics.CP_DIFF_MIN_RATE and avg-item.currentPrice > tactics.CP_DIFF_MIN





"""
与中位数有一定的差距
"""
def midfilter(item,items):
    mid = median(items)
    print "mid:" + str(mid)
    diff = (mid-item.currentPrice)*1.0/item.currentPrice
    print "diffrate:" + str(diff)
    print "diff:" + str(mid-item.currentPrice)
    return diff > tactics.CP_DIFF_MIN_RATE and mid-item.currentPrice > tactics.CP_DIFF_MIN
    

def median(items):
    n = len(items)
    pricelist = list()
    for i in items:
        pricelist.append(i.currentPrice)
    pricelist.sort()
    mid = (pricelist[n/2-1] + pricelist[n/2])/2 if n%2 == 0 else pricelist[n/2]
    return mid


"""
与可信低价商品的差价在一定范围内
"""
def tinydif(x,y):
    return (x-y)/y < tactics.X_MAX_DIFF_RATE and x-y < tactics.X_MAX_DIFF


def bigdif(x,y):
    a = x if x > y else y
    b = x if x < y else y
    return a*1.0/b > tactics.MAX_SAMPLE_DIFF_RATE


def samplefilter(items):
    itemlist = list()
    avg_med = average(items) if len(items) < 5 else median(items)
    print avg_med
    for item in items:
        print item.itemId
        if item.picked == 1:
            itemlist.append(item)
        else:
            if computeCredit(item) < tactics.CP_MIN_CREDIT:
                print "credit:" + str(computeCredit(item))
                continue
            if bigdif(item.currentPrice,avg_med):
                print "diff:"+str(item.currentPrice)
                continue
            itemlist.append(item)
    return itemlist


"""
取得可信低价商品：首先要可信，价格比原先的低，然后取信用值最高的
"""
def getXpickitem(item,items):
    bestitem  = None
    bestCredit = 0
    for i in items:
        if item.currentPrice > i.currentPrice:
            credit = computeCredit(i)
            if credit > tactics.CP_CREDIT_GOOD and credit > bestCredit:
                bestCredit = credit
                bestitem = i
    return bestitem

"""
在比较同款商品时，过低的信用不进入样本
"""

def compare(pickitem,items):
    print len(items)
    itemlist = samplefilter(items)
    for i in itemlist:
        print i.itemId
    n = len(itemlist)
    """
    当样本不足2个时，则不入库
    """
    if n < 2:
        return 0

    """
    如果pickitem是最低价，则需要于均值（平均数或中位数）有一定的差距，差距太小则不入库
    """
    if islowestprice(pickitem,itemlist):
        if n == 2:
            if avgfilter(pickitem,itemlist):
                return 1 
            return -1
        else:
            if midfilter(pickitem,itemlist):
                return 1 
            return -1
    else:
        xpickeditem = getXpickitem(pickitem,itemlist)
        if n == 2:
            if xpickeditem:
                return -2
            return 1
        elif n < 5:
            if not avgfilter(pickitem,itemlist):
                return -1
            if xpickeditem and not tinydif(pickitem.currentPrice , xpickeditem.currentPrice):
                return -2
            return 1
        else:
            if not midfilter(pickitem,itemlist):
                return -1
            if xpickeditem and not tinydif(pickitem.currentPrice , xpickeditem.currentPrice):
                return -2
            return 1
"""
    else:
        ##如果不是最低价，则试图取出其他可信的低价商品，并对该商品重新进行验证
        
        xpickeditem = getXpickitem(pickitem,itemlist)
        ##print xpickeditem
        if n == 2:
            if xpickeditem:
                return compare(xpickeditem,items)
            ##print "not enough good"
            return None
        elif n < 5:
            ##如果有其他可信商品，且与原先差距不大，而与均值有差距，则可取。否则验证取出的。
            ##如果没有其他可信，则验证原先商品与均值差距，有则取，否则不入库
            if xpickeditem:
                if tinydif(pickitem.currentPrice , xpickeditem.currentPrice) and avgfilter(pickitem,items):
                    return pickitem
                print "verify xitem"
                return compare(xpickeditem,items)
            return pickitem if avgfilter(pickitem,items) else None
        else:
            ##与上面相似，只是把均值改成了中位数
            if xpickeditem:
                if tinydif(pickitem.currentPrice , xpickeditem.currentPrice) and midfilter(pickitem,items):
                    return pickitem
                print "verify xitem"
                return compare(xpickeditem,items)
            return pickitem if midfilter(pickitem,items) else None
"""


def calItemRank(item):
    ##质量分不超过1
    sharenum = item.sharenum if item.sharenum else 0
    favournum = item.favournum if item.favournum else 0
    tradeNum = item.tradeNum if item.tradeNum else 0
    commend = item.commend if item.commend else 0
    browsenum = item.browsenum if item.browsenum else 0
    i_score = (sharenum*250 + favournum*10 + tradeNum*50 + commend*50)/4.0/browsenum
    if i_score > 1:
        i_score = 1
    ##质量分乘以可信度 1000可达0.5
    return i_score*(1-1000.0/(browsenum+1000))


def calChange(currentprice,pricelist):
    prices = list()
    for p in pricelist:
        if p[1] is not None and p[1]/currentprice < tactics.MAX_DIFF_CHANGE_HISTORY: ##价格偏差太大的不要
            prices.append(p)

    if len(prices) == 0:
        return 0

    if len(prices) == 1:
        return 1 - currentprice*1.0/prices[0][1]
    a = None
    b = None
    avg_sum = 0
    preriod_sum = 0
    for price in prices:
        if a == None:
            a = price
            continue
        b = price
        preriod_sum += (b[0] - a[0])
        avg_sum += a[1]*(b[0] - a[0])
        a = price
    unix_now_timestamp = int(time.time())
    preriod_sum += (unix_now_timestamp - a[0])
    avg_sum += a[1]*(unix_now_timestamp - a[0])
    avg_price = avg_sum*1.0/preriod_sum
    return 1-currentprice/avg_price


def isGoodItem(item):
    if item.itemrank < tactics.OUT_GOOD_ITEMRANK:
        return False
    if item.changerank < tactics.OUT_GOOD_CHANGERANK:
        return False
    if item.cprank < tactics.OUT_GOOD_CPRANK:
        return False
    if item.cprank == tactics.IN_GOOD_CPRANK:
        return True
    if item.itemrank > tactics.IN_GOOD_ITEMRANK:
        return True
    if item.changerank > tactics.IN_GOOD_CHANGERANK:
        return True
    if item.itemrank > tactics.INTER_GOOD_ITEMRANK and item.changerank > tactics.INTER_GOOD_CHANGERANK:
        return True
    return False


def computescore(item):
    cprank = item.cprank if item.cprank else 0
    itemrank = item.itemrank if item.itemrank else 0
    changerank = item.changerank if item.changerank else 0
    time_now = int(time.time()) - 1367550132
    score = cprank*1.5 + itemrank + changerank*2 + time_now*0.2/3600
    return score
"""
在取相似产品时，超低价，不可信的就别出了
"""
FAM_MAX_LOW_DIFF = 0.1
FAM_MIN_CREDIT = 0.5

def toolow(x,y):
    return (y-x)/y > FAM_MAX_LOW_DIFF

def getFamitems(items):
    famitems = list()
    for item in samplefilter(items):
        if item.picked == 1:
            continue
        famitems.append(item)
    return sorted(famitems,key=lambda item:computeCredit(item) ,reverse=True)


 
    


