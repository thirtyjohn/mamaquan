#coding:utf8
import re
from manager.settings import dbconn
from helpers.utils import analyname,analyname_duan,analyname_series,analyname_weight,comp_weight
from helpers.b2c import factory
from manager.models import products

def insertmmlisturl(brand=None,market=None,url=None):
    dbconn.insert("mmlisturl",brand=brand,market=market,url=url)

"""
插入调度入口
"""
def getlistandinsert(brand=None,market=None):
    b2c_list = factory(market)
    nextpage = 1
    while True:
        if nextpage:
            url = products.getHost(brand=brand,market=market,page=nextpage)
            print url
            b2c_list.listurl = url
            b2c_list.listhtml = b2c_list.getListHtml()
            nflist = b2c_list.getlist()
            for nf in nflist:
                nf.market = market
                nf.brand = brand
                if not products.hasNfitem(nf):
                    products.insertNfitem(nf)

            nextpage = nextpage+1 if b2c_list.nextPage() else None
        else:
            break


"""
更新调度入口
"""
def updatenafens(brand=None,market=None):
    if not market:
        return
    b2c_test = factory(market)
    if not hasattr(b2c_test,"getProperty"):
        return
    nfs = products.getNfitemNotProcessed(market=market,brand=brand)
    for nf in nfs:
        b2c_item = factory(market)
        b2c_item.itemid = nf.itemid
        b2c_item.itemhtml = b2c_item.getItemHtml()
        nvlist = b2c_item.getProperty()
        nfitem = products.getNfProperty(nvlist)
        nfitem.update(nf.itemid,market)

"""
调整系列名称
"""
def updateSeries(brand=None):
    series = [u"冠军宝贝",u"金爱+",u"爱+",u"金装贝因美"]
    nfs = products.getNfitemNotProcessed(brand=brand)
    for nf in nfs:
        if nf.series:
            newseries = getSeries(nf.series,series)
            if newseries:
                print nf.series + ":" + newseries
                #update(nf)
            else:
                print nf.series
        ##if newseries: update(nf) else:print id

def getSeries(oldname,serieslist):
        serieslist = sorted(serieslist,key= lambda x: len(x) ,revers=True)
        for sname in serieslist:
            if oldname.find(sname) > -1:
                return sname
    
"""
以某渠道作为样本进入预产品库，同时建立对应关系
"""
def yangben(brand,market):
    products.batchInsertPreNf(brand=brand,market=market) 




"""
比较算法，目前还比较简陋，主要通过名称匹配
"""
def isSameNf(nf,product):
    price_diff = nf.price*1.0/product.price if nf.price > product.price else product.price*1.0/nf.price
    ##print price_diff
    ##print "pr======"
    ##print analyname(product.name)
    ##print "nf======"
    ##print analyname(nf.name)
    if analyname(product.name) == analyname(nf.name) and  price_diff < 1.2:
        return True
    return False

"""
匹配某渠道某品牌奶粉
"""
def testmatch(brand=None,market=None):
    nf_list = list()
    res = products.getNfitemNotMatch(brand=brand,market=market) 
    for r in res:
        nf_list.append(r)
    res = products.getPreNf(brand=brand) 
    for r in res:
        for nf in nf_list:
            if isSameNf(nf,r):
                dbconn.insert("formalprmatch",prid=r.ID,itemid=nf.itemid,market=market)


"""
寻找相似用于人工比对
"""

def isFamiliar(nf,product):
    nfduan,nfseries,nfweight = analyname(nf.name)
    prduan,prseries,prweight = analyname(product.name)
    ##print nfduan,prduan
    if nfduan and prduan and nfduan <> prduan:
        return False
    ##print nfseries,prseries
    if nfseries and prseries and nfseries <> prseries:
        return False
    return True

def findfamiliar(extra,prenaifens):
    fams = list() 
    for r in prenaifens:
        if isFamiliar(extra,r):
            fams.append(r)
    return fams

"""
获得没又被匹配到的奶粉及其相似的产品
"""
def getExtra(brand,market):
    extralist = list()
    res = dbconn.query("""

        select * from naifenitem
        where brand = $brand and market = $market and (matchlater is null or matchlater <> 1)
        and itemid not in (select itemid from formalprmatch where market = $market)
        
                """,vars=dict(brand=brand,market=market)
    )
    for r in res:
        extralist.append(r)


    famlist = list()
    prenaifens = list()
    res = dbconn.query("select * from prenaifen where brand = $brand",vars=dict(brand=brand))
    for r in res:
        prenaifens.append(r)
    for extra in extralist:
        fams = findfamiliar(extra,prenaifens)
        famlist.append((extra,fams))
    return famlist


def insertformalproduct(brand):
    """
    同品牌下,同系列，段数
    每克的价格基本能确定是否同产品。
    所以：
    取得最准段数，取得最准系列。
    取得最准重量。
    段数/系列 == 重量/价格 互为校验,
    把数据弄到最准，然后关联表都不用就能建立关联啦。
    """
    res = dbconn.query("select * from prenaifen where status = 0 and brand = $brand",vars=dict(brand=brand))
    for r in res:
        
        weight = None
        if r.weight:
            m = re.match(u"\d+",r.weight)
            if m:
                weight = int(m.group())
            else:
                m = comp_weight.search(r.weight)
                if m:
                    weight = int(m.group(1))
        if not weight:
            weight = analyname_weight(r.name)

        duan = None
        if r.duan:
            m = re.match(u"\d+",r.duan)
            if m:
                duan = int(m.group())
            else:
                duan = analyname_duan(r.duan)
        if not duan:
            duan = analyname_duan(r.name)

        series = None
        if r.series:
            series = analyname_series(r.series)
        if not series:
            series = analyname_series(r.name)

        
        dbconn.insert("formalnaifen",ID=r.ID,name=r.name,weight=weight,duan=duan,series=series,brand=r.brand,pack=r.pack,place=r.place,price=r.price,img=r.img)
        dbconn.update("prenaifen",status=1,where="id=$prid",vars=dict(prid=r.ID))


"""
通过重量，价格校验段数和系列
"""

def getjiaoyan():
    res_list = list()
    res = dbconn.query("""
        select s.*,s.price/s.weight as sppg,t.ppg as tppg from formalnaifen s
        join(
        select duan,series,avg(price/weight) as ppg from formalnaifen
        where weight is not null and series is not null and duan is not null
        group by duan,series)t
        on s.duan = t.duan and s.series = t.series and s.checked <> 1
        where (s.price/s.weight)/t.ppg > 1.2 or t.ppg/(s.price/s.weight) > 1.2
        order by s.series,s.duan      
    """
    )
    for r in res:
        res1 = dbconn.query("""
        select * from formalnaifen f
        join (select series,duan from formalnaifen where id = $naifenid) t
        on f.series = t.series and f.duan = t.duan
    """,vars=dict(naifenid=r.ID))
        famlist = list()
        for r1 in res1:
            famlist.append(r1)
        res_list.append((r,famlist))
    return res_list


"""
找到属性缺失的,通过其他属性计算给出可能相似的东西
"""
def getqueshi():
    res_list = list()
    res = dbconn.query("""
        select * from formalnaifen where series is null or duan is null or weight is null      
    """
    )
    for r in res:
        if r.weight:
            ppg = r.price*1.0/r.weight
            res1 = dbconn.query("select * from formalnaifen where brand=$brand and price/weight > $min and price/weight < $max",vars=dict(min=ppg*0.9,max=ppg*1.1,brand=r.brand))
        else:

            res1 = dbconn.query("""
                select * from formalnaifen 
                where brand = $brand and (duan=$duan or series=series)
            """,vars=dict(brand=r.brand,duan=r.duan,series=r.series))
        famlist = list()
        for r1 in res1:
            famlist.append(r1)
        res_list.append((r,famlist))
    return res_list

