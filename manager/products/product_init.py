#coding:utf8
from helpers.b2c import factory
from manager.models import products
from manager.models.products import semistatus

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
            if not products.has_semi_item(itemid=item.itemid,market=item.market):
                products.insert_semi_item(item)
        nextpage = nextpage+1 if b2c_list.nextPage() else None

"""
    完善关键信息，增加属性信息
"""
def get_more_info_to_update_semiitem(brand=None,market=None):
    if not market:
        return
    b2c_test = factory(market)
    if hasattr(b2c_test,"getProperty"):
        items = products.get_semi_item(market=market,brand=brand,status=semistatus.JUST_INSERT)
        for item in items:
            b2c_item = factory(market)
            b2c_item.itemid = item.itemid
            nvdict = b2c_item.getProperty()
            ##nfitem = products.getNfProperty(nvlist)
            products.update_semi_item(item["_id"],nvdict)

"""
    else:
        ##通过名称提取信息
        nfs = products.getNfitemNotProcessed(market=market,brand=brand)
        for nf in nfs:
            duan,series,weight = analyname(nf.name,brand=brand)
            products.updateNfitem(nf.ID,series=series,duan=duan,weight=weight)
"""
