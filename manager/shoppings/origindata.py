#coding:utf8

import urllib2,urllib,re
import time
from helpers.crawls import getUrl

"""
采用条件：打折秒杀，默认排序
"""

url_host = "http://list.taobao.com/itemlist/"

general_params = {
        "isprepay":1,
        "viewIndex":1,
        "yp4p_page":0,
        "commend":"all",
        "atype":"b",
        "style":"grid",
        "tid":0,
        "as":0,
        "olu":"yes",
        "isnew":2,
        "user_type":0,
        "random":"false",
        "smc":1,
        "json":"on",
        "module":"page",
        "_input_charset":"utf-8",
        "data-key":"s",
        "data-value":0,
        "same_info":1,
        "zkFlag":1,
        "zk":"dzms"
        }




cat_dict = {
        "nvzhuang":16,
        "nvxie":50006843,
        "wenxiong":50016870,
        "shuiyi":50026786,
        "sushen":50026787,
        "danjianbao":50072721,
        "shoutibao":50072765,
        "xiekuabao":50072769,
        "qianbao":50072766,
        "shounabao":50072770,
        "tongzhuang":50008165,
        "chuangshang":50065205,
        "jiajushipin":50065206,
        "peishi":1705,
        "maorongwanju":50034017,
}

htm_dict = {
        "nvzhuang":"nvzhuang2011a.htm",
        "nvxie":"nvxieshichang2011a.htm",
        "wenxiong":"neiyi2011a.htm",
        "shuiyi":"neiyi2011a.htm",
        "sushen":"neiyi2011a.htm",
        "danjianbao":"nvbao2011a.htm",
        "shoutibao":"nvbao2011a.htm",
        "xiekuabao":"nvbao2011a.htm",
        "qianbao":"nvbao2011a.htm",
        "shounabao":"nvbao2011a.htm",
        "tongzhuang":"baby.htm",
        "chuangshang":"jiaju.htm",
        "jiajushipin":"jiaju.htm",
        "peishi":"shipinshichang.htm",
        "maorongwanju":"wanju.htm"

}

other_dict = {
        "nvzhuang":
            {"fl":"Shangpml"},
        "nvxie":
            {"fl":"nx_shangpml"},
        "wenxiong":
            {"fl":"1625","mSelect":"false"},
        "shuiyi":
            {"fl":"1625","msp":1,"mSelect":"false"},
        "danjianbao":
            {"fl":"danjianx","mSelect":"false"},
        "shoutibao":
            {"fl":"xiekuabaox","mSelect":"false"},
        "xiekuabao":
            {"fl":"xiekuabaox","mSelect":"false"},
        "qianbao":
            {"fl":"qianbaox","mSelect":"false"},
        "shounabao":
            {"fl":"shounabaox","mSelect":"false"},
        "tongzhuang":
            {"gobaby":1,"spercent":95,"mSelect":"false"},
        "chuangshang":
            {"sd":0},
        "jiajushipin":
            {"sd":0},
        "maorongwanju":
            {"sort":"coefp"}
}



def getListHtml(itemclass,page=None):
    params = general_params.copy()
    if other_dict.has_key(itemclass):
        params.update(other_dict[itemclass])
    private_params = {"cat":cat_dict[itemclass]}
    params.update(private_params)
    if page:
        params.update({"data-value":(page-1)*96})
    url = url_host + htm_dict[itemclass] + "?" + urllib.urlencode(params)
    resp = getUrl(url)
    html = resp.read() if resp else None
    return html

def getSameHtml(itemclass,item):
    params = {"style":"list",
              "hd":1,
              "_input_charset":"utf-8",
              "json":"on",
              "cat":cat_dict[itemclass],
              "sameItemId":item.itemId,
              "pid":item.pid
              }

    url = url_host + htm_dict[itemclass] + "?" + urllib.urlencode(params)
    resp = getUrl(url)
    html = resp.read() if resp else None
    return html



"""
    url = "http://list.taobao.com/itemlist/nvzhuang2011a.htm?cat=16&isprepay=1&viewIndex=1&zkFlag=1&fl=Shangpml&style=grid&tid=0&isnew=2&olu=yes&zk=dzms&user_type=0&random=false&as=0&yp4p_page=0&commend=all&atype=b&same_info=1&smc=1&json=on&tid=0&data-key=s&data-value=0&module=page&&_input_charset=utf-8&json=on"

**类目拓展


童装：可以，但是与年龄相关程度高，需要根据用户特征进行筛选。宝贝的丰富度是够的。
promoted_service4=4
spercent=95
gobaby=1


"""


def get30sellhtml(item):
    url = "http://ajax.tbcdn.cn/json/ifq.htm?id="+ str(item.itemId) +"&sid="+ str(item.sellerId) +"&p=1&al=false&ap=1&ss=0&free=0&q=1&ex=0&exs=0&shid=&at=b&ct=1"
    resp = getUrl(url)
    html = resp.read() if resp else None
    return html


def getItemHtml(item):
    url = "http://item.taobao.com/item.htm?id=" + str(item.itemId)
    resp = getUrl(url)
    html = resp.read() if resp else None
    return html


comp_counterApi = re.compile("counterApi:\"(\S+?)\"")
def getItemBFSHtml(txt):
    m = comp_counterApi.search(txt)
    if m:
        url = m.group(1)+"&callback=DT.mods.SKU.CountCenter.saveCounts"
        resp = getUrl(url)
        html = resp.read() if resp else None
        return html

def getItemPriceCutHtml(item):
    url = "http://detailskip.taobao.com/json/price_cut_data.htm?id=" + str(item.itemId)
    resp = getUrl(url)
    html = resp.read() if resp else None
    return html
    
"""
if __name__ == "__main__":
    ##html = getCloth()
    ##f = open(localdir+"test","w")
    ##f.write(html)
    print getListHtml("nvzhuang")
"""
