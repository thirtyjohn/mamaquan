#coding:utf8
from analyscript import Tmall,Amazon,Jd
from zhengli import testmatch,yangben,insertformalproduct
from settings import dbconn

##先插listurl
##getlistandinsert(u'Dumex/多美滋','jd')
##updatenafens(brand=u'Dumex/多美滋',market='jd')
"""
匹配时需注意，系列是否有，如果产品较多杂，则容易出现问题
"""
##getAmazonDetail("B006QHWGDU")

##先插listurl
##hhhgetTmallNaifenId(u"Dumex/多美滋")
"""
选择样本时需要注意样本质量
"""
##yangben(u"Dumex/多美滋","tmall")





"""
插入调度入口
"""
def getlistandinsert(brand,market):
    dp = None
    if market == "tmall":
        dp = Tmall()
    elif market == "amazon":
        dp = Amazon()
    elif market == "jd":
        dp = Jd()
    dp.initNfs(brand)

"""
更新调度入口
"""
def updatenafens(brand=None,market=None):
    if not market:
        return
    res = dbconn.query("select * from naifen where processed is null and market = $market and brand = $brand",vars=dict(market=market,brand=brand))
    dp = None
    if market == "tmall":
        dp = Tmall()
    elif market == "amazon":
        dp = Amazon()
    elif market == "jd":
        dp = Jd()

    for r in res:
        dp.initNf(r.itemid)
