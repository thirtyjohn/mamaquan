#coding:utf8
from settings import serieslist,brandlist
import re
from helpers.utils import getResultForDigit
from ordereddict import OrderedDict

def get_name_from_rule(semi_item,name):
    for r in attr_name_rule(semi_item):
        if r[1](name,r[2]):
            return r[0]

def get_val_from_rule(semi_item,k,v):
    d = attr_val_rule(semi_item) 
    return d[k][0](v,d[k][1])

def get_val_other_from_rule(semi_item,k,v):
    d = attr_val_other_rule(semi_item) 
    return d[k][0](v,d[k][1])


def get_attr_val_key(semi_item):
    return attr_val_rule(semi_item).keys()

def get_attr_name_key(semi_item):
    return [ x[0] for x in  attr_name_rule(semi_item)]


def get_attr_val_other_key(semi_item):
    return attr_val_other_rule(semi_item).keys()

"""
    attr_name 规则

"""
def attr_name_rule(semiitem):
    rule = {
        "naifen":[
            (u"品牌", include, [u"品牌"]),
            (u"阶段", include, [u"段数",u"阶段"]),
            (u"重量", include, [u"重量"]),
            (u"系列", include, [u"系列"]),
            (u"包装", include, [u"包装"]),
            (u"产地", include, [u"产地"]),
            (u"类型", include, [u"类型"]),
            (u"适用年龄", include, [u"年龄"]),
        ]
    }
    return rule[semiitem["cat"]]


"""
    attr_val 规则
    方法接受两个参数 foo(str,data) str是样本数据，data封装了方法需要用到的可配置数据
"""
def attr_val_rule(semi_item):
    rule = {
        "naifen":OrderedDict((
            (u"品牌",(include_kv,brandlist)),
            (u"阶段",(danwei,{"txt":[u"阶段",u"段"],"dw":u"段"})),
            (u"系列",(include,lambda : serieslist[semi_item[u"品牌"]] if semi_item.has_key(u"品牌") and serieslist.has_key(semi_item[u"品牌"]) else None)),
            (u"重量",(danwei,{"txt":[u"克",u"g"],"dw":u"g"})),
        ))
    }
    return rule[semi_item["cat"]]


"""
    附加属性规则
"""
def attr_val_other_rule(semi_item):
    rule = {
        "naifen":OrderedDict((
            (u"包装",(include,[u"罐装",u"盒装",u"桶装",u"袋装",u"箱装"])),
            (u"产地",(first_out,[u"中国",u"新西兰",u"荷兰",u"澳洲",u"韩国",u"德国",u"美国",u"法国",u"丹麦",u"新加坡",u"瑞士",u"爱尔兰",u"澳大利亚",u"西班牙",u"英国",u"阿根廷",u"奥地利",u"台湾",u"马来西亚",u"进口",u"国产"])),
            (u"类型",(first_out,[u"防过敏配方",u"偏食配方",u"腹泻配方",u"早产儿"])),
            (u"适用年龄",(replace_txt,[("-","~")])),
        ))
    }
    return rule[semi_item["cat"]]


def gen_name_rule(item):
    rule = {
        "naifen":[u"品牌",u"系列",u"阶段",u"$奶粉",u"重量"],
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
        datas = data()
        if not datas:
            return None
        datas = sorted(datas,key= lambda x: len(x) ,reverse=True)
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


def first_out(name,data):
    for d in data:
        if name.find(d) > -1:
            return d

def replace_txt(name,data):
    for d in data: 
        name = name.replace(d[0],d[1])
    return name
