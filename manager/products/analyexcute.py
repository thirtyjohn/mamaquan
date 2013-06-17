#coding:utf8
from item2pre2formal import insertmmlisturl, updatenafens, getlistandinsert, testmatch,yangben,insertformalproduct


##"http://abbott.tmall.com/search.htm?search=y&viewType=grid&orderType=_hotsell&pageNum=%d"

##"http://www.amazon.cn/mn/search/ajax/" + "ref=sr_in_-2_p_4_38?rh=n%3A42692071%2Cn%3A%2142693071%2Cn%3A79192071%2Cn%3A79193071%2Cp_4%3AMeiji+%E6%98%8E%E6%B2%BB&bbn=79193071&ie=UTF8&qid=1371023499&rnid=1952913051"+"&section=ATF,BTF&fromApp=gp%2Fsearch&fromPage=results&version=2&page="

def startupdate():
    ##先插listurl
    url = u"http://www.amazon.cn/mn/search/ajax/ref=sr_nr_p_6_1?rh=n%3A42692071%2Cn%3A%2142693071%2Cn%3A79192071%2Cn%3A79193071%2Cp_4%3AMeiji+%E6%98%8E%E6%B2%BB%2Cp_6%3AA1AJ19PSB66TGU&bbn=79193071&ie=UTF8&qid=1371023508&rnid=51325071&section=ATF,BTF&fromApp=gp%2Fsearch&fromPage=results&version=2&page="
    brand = u"meiji"
    market = u"tmall"

    ##系列表

    ##insertmmlisturl(brand=brand,market=market,url=url)
    ##return

    ##getlistandinsert(brand=brand,market=market)
    ##return

    ##updatenafens(brand=brand,market=market)

    ##market = u"tmall"
    ##yangben(brand=brand,market=market)
    ##market = 'zcn'
    ##testmatch(brand=brand,market=market)

    ##http://127.0.0.1:8080/match
    ##人工匹配
    
    ##插入正式表
    insertformalproduct(brand)
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
##testmatch()






