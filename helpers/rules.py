#coding:utf8
from settings import serieslist,brandlist
import re
from helpers.utils import getResultForDigit
from ordereddict import OrderedDict

def get_name_from_rule(semi_item,name):
    for r in attr_name_rule():
        if r[1](name,r[2]):
            return r[0]

def get_val_from_rule(semi_item,k,v):
    d = attr_val_rule(semi_item) 
    return d[k][0](v,d[k][1])


def get_attr_val_key(semi_item):
    return attr_val_rule(semi_item).keys()



"""
    attr_name 规则

"""
def attr_name_rule():
    rule = [
        (u"品牌", include, [u"品牌",u"brand"]),
        (u"段数", include, [u"段数",u"duan",u"阶段"]),
        (u"重量", include, [u"weight",u"重量"]),
        (u"系列", include, [u"series",u"系列"]),
    ]
    return rule


"""
    attr_val 规则
    方法接受两个参数 foo(str,data) str是样本数据，data封装了方法需要用到的可配置数据
"""
def attr_val_rule(semi_item):
    rule = {
        "naifen":OrderedDict((
            (u"品牌",(include_kv,brandlist)),
            (u"段数",(danwei,{"txt":[u"阶段",u"段"],"dw":u"段"})),
            (u"系列",(include,lambda : serieslist[semi_item[u"品牌"]] if semi_item.has_key(u"品牌") else None)),
            (u"重量",(danwei,{"txt":[u"克",u"g"],"dw":u"g"})),
        ))
    }
    return rule[semi_item["cat"]]


def gen_name_rule(item):
    rule = {
        "naifen":[u"品牌",u"系列",u"段数",u"$奶粉",u"重量"],
    }
    return rule[item["cat"]]

img_market_rule = [u"jd",u"zcn",u"tmall",u"amazon"]

"""
    文字匹配规则
"""

def include(sample,data):
    if isinstance(data,unicode):
        if sample.find(data) > -1:
            return data
    elif isinstance(data,list):
        data = sorted(data,key= lambda x: len(x) ,reverse=True)
        for d in data:
            if sample.find(d) > -1:
                return d
    else:
        datas = sorted(data(),key= lambda x: len(x) ,reverse=True)
        for d in datas:
            if sample.find(d) > -1:
                return d

def danwei(name,data):
    q,q_txt = None,None
    comp_m = re.match(u"[0-9一二三四五六七八九十百千万亿]+",name)
    comp_q = re.compile(u"([0-9一二三四五六七八九十百千万亿]+)("+u"|".join(data["txt"])+")")
    if comp_m:
        q_txt = name 
    else:
        m = comp_q.search(name)
        q_txt = m.group(1) if m else None
    try:
        q = int(q_txt) if q_txt else None
    except:
        q = getResultForDigit(q_txt) if q_txt else None 
    return unicode(q) + data["dw"] if q else None

def same(name,data):
    return name


def include_kv(name,data):
    for k,v in data:
        for n in v:
            if name.find(n) > -1:
                return k
