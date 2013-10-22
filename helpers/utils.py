#coding:utf8
import re,time,urllib2,urllib,types
from settings import url_market,exchange_rate,market_name,serieslist

comp_duan = re.compile(u"([0-9一二三四]+)(段|阶段)")
comp_weight = re.compile(u"(\d+)[g|克]")
comp_quantity = re.compile(u"[*x](\d+)")


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


def analyname_series(name,brand=None):
    series_list = sorted(serieslist[brand],key= lambda x: len(x) ,reverse=True)
    for s in series_list:
        if name.find(s) > -1:
            return s


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
def analyname(name,brand=None):
    
    duan = analyname_duan(name)

    series = analyname_series(name,brand=brand)

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

class TJORM:
    def __init__(self):
        self._tablename = None
    def insert(self,dbconn):
        colnamevalue = dict()
        colnames = filter(lambda aname: not aname.startswith('_') and not isinstance(getattr(self,aname),types.NoneType) and not isinstance(getattr(self,aname),types.MethodType),dir(self))
        for colname in colnames:
            colnamevalue.update({colname:getattr(self,colname)})
        dbconn.insert(self._tablename,**colnamevalue)


def objtodict(ob):
    colnamevalue = {}
    colnames = filter(lambda aname: not aname.startswith('_') and not isinstance(getattr(ob,aname),types.NoneType) and not isinstance(getattr(ob,aname),types.MethodType),dir(ob))
    for colname in colnames:
        print colname
        colnamevalue.update({colname:getattr(ob,colname)})
    return colnamevalue
    

def getResultForDigit(a, encoding="utf-8"):

    dict ={u'零':0, u'一':1, u'二':2, u'三':3, u'四':4, u'五':5, u'六':6, u'七':7, u'八':8, u'九':9, u'十':10, u'百':100, u'千':1000, u'万':10000,u'亿':100000000}

    if isinstance(a, str):
        a = a.decode(encoding)

    count = 0
    result = 0
    tmp = 0
    Billion = 0
    while count < len(a):
        tmpChr = a[count]
        #print tmpChr
        tmpNum = dict.get(tmpChr, None)
        #如果等于1亿
        if tmpNum == 100000000:
            result = result + tmp
            result = result * tmpNum
            #获得亿以上的数量，将其保存在中间变量Billion中并清空result
            Billion = Billion * 100000000 + result
            result = 0
            tmp = 0
        #如果等于1万
        elif tmpNum == 10000:
            result = result + tmp
            result = result * tmpNum
            tmp = 0
        #如果等于十或者百，千
        elif tmpNum >= 10:
            if tmp == 0:
                tmp = 1
            result = result + tmpNum * tmp
            tmp = 0
        #如果是个位数
        elif tmpNum is not None:
            tmp = tmp * 10 + tmpNum
        count += 1
    result = result + tmp
    result = result + Billion
    return result
