#coding:utf8
import web,re
from settings import dbconn
from utils import analyname,analyname_duan,analyname_series,analyname_weight,comp_weight
"""
比较算法，目前还比较简陋，主要通过名称匹配
"""
def isSameNf(nf,product):
    price_diff = nf.price*1.0/product.price if nf.price > product.price else product.price*1.0/nf.price
    if analyname(product.name) == analyname(nf.name) and  price_diff < 1.2:
        return True
    return False


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

"""
匹配某渠道某品牌奶粉
"""
def testmatch(brand,market):
    nf_list = list()
    res = dbconn.query(u"select * from naifen where brand = $brand and market = $market and itemid not in (select itemid from naifenmatch where market=$market)",vars=dict(brand=brand,market=market))
    for r in res:
        nf_list.append(r)
    res = dbconn.query(u"select * from prenaifen where brand = $brand",vars=dict(brand=brand))
    for r in res:
        for nf in nf_list:
            if isSameNf(nf,r):
                dbconn.insert("naifenmatch",naifenid=r.ID,itemid=nf.itemid,market=market)





"""
以某渠道作为样本进入预产品库，同时建立对应关系
"""
def yangben(brand,market):
##批量插入预产品库
    dbconn.query("insert into prenaifen (name,duration,weight,spec,brand,series,sellto,age,duan,pack,place,price,img) select name,duration,weight,spec,brand,series,sellto,age,duan,pack,place,price,img from naifen where brand = $brand and market = $market",vars=dict(brand=brand,market=market))
##建立对应关系
    res = dbconn.query(u"select * from prenaifen where brand = $brand",vars=dict(brand=brand))
    for r in res:
        res1  = dbconn.query(u"select * from naifen where name = $name and market=$market",vars=dict(name=r.name,market=market))
        item = web.listget(res1,0,None)
        dbconn.insert("naifenmatch",naifenid=r.ID,itemid=item.itemid,market=market)


def findfamiliar(extra,prenaifens):
    fams = list() 
    for r in prenaifens:
        if isFamiliar(extra,r):
            fams.append(r)
    return fams


def getExtra(brand,market):
    extralist = list()
    res = dbconn.query("""

        select * from naifen
        where brand = $brand and market = $market and (matchlater is null or matchlater <> 1)
        and itemid not in (select itemid from naifenmatch where market = $market)
        
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


def insertformalproduct():
    """
    同品牌下,同系列，段数
    每克的价格基本能确定是否同产品。
    所以：
    取得最准段数，取得最准系列。
    取得最准重量。
    段数/系列 == 重量/价格 互为校验,
    把数据弄到最准，然后关联表都不用就能建立关联啦。
    """
    res = dbconn.query("select * from prenaifen")
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

