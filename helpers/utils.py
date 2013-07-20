#coding:utf8
import re,time,urllib2,urllib
from mechanize import Browser
from settings import url_market,exchange_rate,market_name

comp_duan = re.compile(u"([0-9一二三四]+)(段|阶段)")
comp_weight = re.compile(u"(\d+)[g|克]")
comp_quantity = re.compile(u"[*x](\d+)")
serieslist = [u'启赋',u'幼儿乐',u'膳儿加',u'爱儿素',u'爱儿加',u'爱儿乐',u'健儿乐',u'学儿乐',u'爱儿复',u'小安素',u'喜康力',u'亲护',u'喜康宝',u'菁智',u'喜康素',u'舒心美',u'优阶',u'优衡多营养']


def analyname_duan(name):
    duan = None
    m = comp_duan.search(name)
    duan_txt = m.group(1) if m else None
    if duan_txt:
        if duan_txt == u"一":
            duan = 1
        elif duan_txt == u"二":
            duan = 2
        elif duan_txt == u"三":
            duan = 3
        elif duan_txt == u"四":
            duan = 4
        else:
            duan = int(duan_txt)
    return duan


def analyname_series(name):
    series = None
    for s in serieslist:
        if name.find(s) > -1:
            series = s
    return series


def analyname_weight(name):
    weight = None
    m = comp_weight.search(name)
    weight_unit = int(m.group(1)) if m else None
    if weight_unit and weight_unit > 2000:
        weight = weight_unit
    else:
        m = comp_quantity.search(name)
        weight = weight_unit*int(m.group(1)) if m else weight_unit
    return weight

"""
名称匹配的主要逻辑
"""
def analyname(name):
    
    duan = analyname_duan(name)

    series = analyname_series(name)

    weight = analyname_weight(name)         

    return duan,series,weight


def secondtodatetxt(sec):
    days = sec/86400
    hours = (sec - days*86400)/3600
    minutes = (sec - days*86400 - hours*3600)/60    
    if days > 0:
        return str(days) + u"天"
    if hours > 0:
        return str(hours) + u"小时"
    if minutes > 0:
        return str(minutes) + u"分钟"


def _xsseccape(t):
    return True


comp_domain = re.compile(u"[0-9a-z]+\.(com|net|cn)")
def getMarketFromUrl(url):
    m = comp_domain.search(url)
    if not m:
        return None
    domain = m.group()
    if url_market.has_key(domain):
        return url_market[domain]
    return None


def price(price,currency):
    return price*exchange_rate[currency]


def getMarketName(market):
    if market_name.has_key(market):
        return market_name[market]
    return None


def resetAdsl():
    print "============disconect========="
    req = urllib2.Request("http://192.168.0.1/goform/SysStatusHandle")
    req.add_header("Referer","http://192.168.0.1/system_status.asp")
    req.add_header("Cookie","admin:language=cn")
    data = {'CMD':'WAN_CON', 'GO':'system_status.asp', 'action':'4'}
    urllib2.urlopen(req,data=urllib.urlencode(data))
    time.sleep(1)
    print "============reconect========="
    data = {'CMD':'WAN_CON', 'GO':'system_status.asp', 'action':'3'}
    urllib2.urlopen(req,data=urllib.urlencode(data))



def clipText(txt,num):
    if len(txt) < num:
        return txt
    return txt[0:num]+u"..."

