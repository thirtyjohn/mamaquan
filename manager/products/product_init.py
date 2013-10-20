#coding:utf8
from helpers.b2c import factory
from manager.models import products
from manager.models.products import semistatus
from helpers.rules import get_name_from_rule,get_val_from_rule,get_attr_val_key

"""
    获取item列表插入semiitem，插入关键信息
    --
    name
    itemid
    market
    --
    option:
        img
        price
        currency
    --
"""
def get_list_to_insert_semiitem(brand=None,market=None):
    b2c_list = factory(market)
    nextpage = 1
    while nextpage:
        url = products.getHost(brand=brand,market=market,page=nextpage)
        print url
        b2c_list.listurl = url
        b2c_list.listhtml = b2c_list.getListHtml()
        itemlist = b2c_list.getlist()
        for item in itemlist:
            item.market = market
            item.brand = brand
            item.cat = "naifen"
            if not products.has_semi_item(itemid=item.itemid,market=item.market):
                products.insert_semi_item(item)
        nextpage = nextpage+1 if b2c_list.nextPage() else None

"""
    完善关键信息，增加属性信息
"""
def get_more_info_to_update_semiitem(**kwargs): 
    items = products.get_semi_item(status=semistatus.JUST_INSERT,**kwargs)
    for item in items:
        if not item["market"]:
            continue
        b2c_test = factory(item["market"])
        if hasattr(b2c_test,"getProperty"):
            b2c_item = factory(item["market"])
            b2c_item.itemid = item.itemid
            nvdict = b2c_item.getProperty()
            nvdict.update({"status":semistatus.JUST_MORE})
            ##nfitem = products.getNfProperty(nvlist)
            products.update_semi_item(item["_id"],nvdict)



"""
    标准化属性信息（根据规则表）
    1. 标准化属性名称
    2. 标准化属性值
    3. 如果确实关键属性，根据名称进行增补
"""

def update_attr_to_item(**kwargs):
    semi_items = products.get_semi_item(status={"$lte":semistatus.JUST_MORE},**kwargs)
    for semi_item in semi_items:
        std_attr_name(semi_item)
        std_attr_val(semi_item)
        semi_item.pop("_id")
        products.insert_item(semi_item)



"""
    进行匹配尝试，整理出产品
"""
def match_item_to_product(**kwargs):
    itemlist = list()
    items = products.get_item(**kwargs)
    for item in items:
        itemlist.append(item)
    itemlist = classify(itemlist,item_compare)
    return itemlist


MAX_DIFF = 1.2
MIN_EQ = 2

def item_compare(a,b):
    if a["cat"] <> b["cat"]:
        return False
    price_diff = a["price"]/b["price"] if a["price"] > b["price"] else b["price"]/a["price"]
    if price_diff > MAX_DIFF:
        return False
    keys = get_attr_val_key(a)
    eq_count = len(keys)
    for k in keys:
        if a[k] <> b[k]:
            return False
        if a[k] is None:
            eq_count -= 1
    return eq_count > MIN_EQ



"""
    列表分类算法
"""
def classify(alist,cp_method):
    
    class_list = list()

    def compare_rest(li):
        if len(li) == 0:
            return
        if len(li) == 1:
            class_list.append([li[0]])
            return
        samelist = [li[0]]
        same_i = [0]
        for i in range(1,len(li)):
            if cp_method(li[0],li[i]):
                samelist.append(li[i])
                same_i.append(i)
        class_list.append(samelist)
        j = 0
        for n in same_i:
            n = n - j
            del li[n]
            j += 1
        compare_rest(li)

    compare_rest(alist)
    return class_list


def std_attr_name(semi_item):
    for k in semi_item.keys():
        new_k = get_name_from_rule(semi_item,k)
        if new_k and new_k <> k:
            semi_item[new_k] = semi_item.pop(k)


def std_attr_val(semi_item):
    for k in get_attr_val_key(semi_item):
        if semi_item.has_key(k) and semi_item[k]:
            new_v = get_val_from_rule(semi_item,k,semi_item[k])
            if new_v and new_v <> semi_item[k]:
                semi_item[k] = new_v
        else:
            ##如果缺失，则从名称中获取,否则记None
            new_v = get_val_from_rule(semi_item,k,semi_item["name"])
            semi_item[k] = new_v
    

"""
    else:
        ##通过名称提取信息
        nfs = products.getNfitemNotProcessed(market=market,brand=brand)
        for nf in nfs:
            duan,series,weight = analyname(nf.name,brand=brand)
            products.updateNfitem(nf.ID,series=series,duan=duan,weight=weight)
"""
