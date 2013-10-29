#coding:utf8
from helpers.b2c import factory
from manager.models import products
from manager.models.products import semistatus,Product
from helpers.rules import get_name_from_rule,get_val_from_rule,get_attr_val_key,gen_name_rule,img_market_rule,get_attr_name_key,get_attr_val_other_key,get_val_other_from_rule

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
def get_list_to_insert_semiitem(market,cat,page=None,**kwargs):
    b2c_list = factory(market)
    nextpage = page if page else 1
    while nextpage:
        url = products.getHost(cat=cat,market=market,page=nextpage,other=kwargs)
        print url
        b2c_list.listurl = url
        itemlist = b2c_list.getlist()
        for item in itemlist:
            item.market = market
            item.cat = cat
            if kwargs:
                for k,v in kwargs.items():
                    item[k] = v 
            if not products.has_semi_item(itemid=item.itemid,market=item.market):
                products.insert_semi_item(item)
        if len(itemlist) == 0:
            break
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
            b2c_item.itemid = item["itemid"]
            updict = {"status":semistatus.JUST_MORE}
            nvdict = b2c_item.getProperty()
            if nvdict:
                updict.update(nvdict)
            ##nfitem = products.getNfProperty(nvlist)
            products.update_semi_item(item["_id"],updict)



"""
通过迭代的更新不断完善rules
"""
def std_attr_name_to_item_temp(**kwargs):
    semi_items = products.get_semi_item(status={"$lte":semistatus.JUST_MORE},**kwargs)
    for semi_item in semi_items:
        std_attr_name(semi_item)
        semi_item.pop("_id")
        products.insert_item_temp(semi_item)

def std_attr_val_to_item_temp(**kwargs):
    temp_items = products.get_temp_item(**kwargs)
    for temp_item in temp_items:
        std_attr_val(temp_item)
        mid = temp_item.pop("_id")
        products.update_item_temp(mid,temp_item)

"""
    标准化属性信息（根据规则表）
    1. 标准化属性名称
    2. 标准化属性值
    3. 如果确实关键属性，根据名称进行增补
"""

def update_attr_to_item(limit=None,**kwargs):
    semi_items = products.get_semi_item(status={"$lte":semistatus.JUST_MORE},**kwargs)
    for semi_item in semi_items:
        std_attr_name(semi_item)
        std_attr_val(semi_item)
        for k in get_attr_val_key(semi_item):
            ##如果缺失，则从名称中获取,否则记None
            if not semi_item.has_key(k) or not semi_item[k]:
                new_v = get_val_from_rule(semi_item,k,semi_item["name"])
                semi_item[k] = new_v
        semi_item.pop("_id")

        if limit and not limit(semi_item):
            continue
        if not products.has_item(itemid=semi_item["itemid"],market=semi_item["market"]):
            products.insert_item(semi_item)

"""
导入新商品后，先启动
1.与产品库自动配对。
2.商品内部配对
3.人工配对
"""
def match_with_product(**kwargs):
    matched_item_ids = products.get_matched_item_ids(**kwargs)
    new_kw = {"_id":{"$nin":matched_item_ids}} if matched_item_ids and len(matched_item_ids) > 0 else {}
    if kwargs:
        new_kw.update(kwargs)
    items_to_match = products.get_item(**new_kw)
    print "item to match:" + str(items_to_match.count())
    products_to_match = [ x for x in products.get_product(**kwargs)]
    matched = 0
    for item in items_to_match:
        for pr in products_to_match:
            if item_compare(item,pr):
                matched += 1
                products.add_pr_match(pr=pr,item=item)
    print "item matched:" + str(matched)

"""
    进行匹配尝试，整理出产品
"""
def match_item_to_product(**kwargs):
    matched_item_ids = products.get_matched_item_ids(**kwargs)
    new_kw = {"_id":{"$nin":matched_item_ids}} if matched_item_ids and len(matched_item_ids) > 0 else {}
    if kwargs:
        new_kw.update(kwargs)
    items_to_match = products.get_item(**new_kw)
    itemlist = [ x for x in items_to_match ]
    itemlist = classify(itemlist,item_compare)
    """
        整理出的产品
            有配对成功的 -> 加入product，加入对应表
            没有配对成功的 -> 留着尝试与product进行相似配对
    """
    c = 0
    for m in itemlist:
        if len(m) > 1:
            pr = gen_product_attr(m)
            pr.match_ids = []
            for i in m:
                pr.match_ids.append(i["_id"])
            products.insert_product(pr)
            c += 1
    print "match:" + str(c) +" , unmatch:"+str(len(itemlist) - c)


def gen_product_attr(m):
    if isinstance(m,list):
        item = m[0]
        pr = Product()
        pr.cat = item["cat"]
        pr.name = u""
        for key in gen_name_rule(item):
            if key[0] <> u"$":
                pr.name += item[key] if item[key] else u""
            else:
                pr.name += key[1:]
        pr.img = min(m,key=lambda x:img_market_rule.index(x["market"]))["img"]
        pr.price = min(m,key=lambda x:x["price"])["price"]
        for key in get_attr_val_key(item):
            pr[key] = item[key]
        return pr
    else:
        item = m
        pr = Product()
        pr.cat = item["cat"]
        pr.name = u""
        for key in gen_name_rule(item):
            if key[0] <> u"$":
                pr.name += item[key] if item[key] else u""
            else:
                pr.name += key[1:]
        pr.img = item["img"]
        pr.price = item["price"]
        for key in get_attr_val_key(item):
            pr[key] = item[key]
        return pr


"""
启动人工配对,算出相似分，从高到低排序
"""
def get_fam_to_match(**kwargs):
    new_kwargs = kwargs.copy()
    if new_kwargs.has_key("market"):
        del new_kwargs["market"]
    matched_item_ids = products.get_matched_item_ids(**new_kwargs)
    new_kw = {"_id":{"$nin":matched_item_ids}}
    if kwargs:
        new_kw.update(kwargs)
    items_to_match = products.get_item(**new_kw)
    products_to_match = [ x for x in products.get_product(**new_kwargs)]
    res = list()
    for item in items_to_match:
        prlist = sorted(products_to_match,key=lambda pr:item_pr_compare(item,pr),reverse=True)
        res.append((item,prlist))
    return res

"""
相似分 = 价格分 + 关键值相同数
"""
def item_pr_compare(item,pr):
    if item["cat"] <> pr["cat"]:
        return 0
    price_score = item["price"]/pr["price"] if item["price"] < pr["price"] else pr["price"]/item["price"]
    key_score = 0
    for k in get_attr_val_key(item):
        if item[k] == pr[k]:
            key_score += 1
    return price_score + key_score


"""
item 比较方法，两个常数值可以进行配置
主要比较价格和关键属性相同的个数
"""
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
            if semi_item.has_key(new_k) and semi_item[new_k]:
                semi_item[new_k] = semi_item[new_k] + "$" + semi_item.pop(k)
            else:
                semi_item[new_k] = semi_item.pop(k)


def std_attr_val(semi_item):
    for k in get_attr_val_key(semi_item):
        if semi_item.has_key(k) and semi_item[k]:
            new_v = get_val_from_rule(semi_item,k,semi_item[k])
            if new_v and new_v <> semi_item[k]:
                semi_item[k] = new_v

    for k in get_attr_val_other_key(semi_item):
        if semi_item.has_key(k) and semi_item[k]:
            new_v = get_val_other_from_rule(semi_item,k,semi_item[k])
            if new_v and new_v <> semi_item[k]:
                semi_item[k] = new_v
        
    

"""
    else:
        ##通过名称提取信息
        nfs = products.getNfitemNotProcessed(market=market,brand=brand)
        for nf in nfs:
            duan,series,weight = analyname(nf.name,brand=brand)
            products.updateNfitem(nf.ID,series=series,duan=duan,weight=weight)
"""

"""
获取属性名称汇聚数据，用来确定属性名称使用
"""
def aggr_attr(**kwargs):
    attr_dict = dict()
    attr_list = list()
    for r in  products.get_semi_item(**kwargs):
        for k in r.keys():
            if attr_dict.has_key(k):
                attr_dict[k] += 1
            else:
                attr_dict[k] = 1
    for k,v in attr_dict.items():
        attr_list.append((k,v))
    return sorted(attr_list,key=lambda x:x[1],reverse=True)



"""
获取关键属性值的属性汇总数据
"""

def aggr_val(table,**kwargs):
    k_v_list = list()
    def aggr(key,where):
        pipe = [
            { "$match": where },
            { "$group": { "_id": "$"+key , "count":{"$sum":1} } },
            { "$sort": { "count":-1 } }
        ]
        return products.aggregate(table,pipe)

    for k in get_attr_name_key(kwargs):
        val_list = list()
        r = aggr(k,kwargs)
        for d in r["result"]:
             val_list.append((d["_id"],d["count"]))
        k_v_list.append((k,val_list))
    return k_v_list 

    



