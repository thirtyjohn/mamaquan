#coding:utf8
from manager.settings import dbconn
from helpers.b2c import factory
from helpers.loggers import get_logger
import traceback

def getDpForCheck():
    return dbconn.query("select * from (select * from formaldanping order by id desc limit 100)t where t.stock = 1")

def check(dp):

    b2c_item = factory(dp.market)
    b2c_item.itemid = dp.itemid

    price = b2c_item.getPrice()
    stock = b2c_item.getStock()


    if price > dp.price or stock == 0:
        return False
    return True

def main():
    dps = getDpForCheck()
    for dp in dps:
        try:
            stock = check(dp)
            if not stock:
                dbconn.update("formaldanping",where="id=$dpid",vars=dict(dpid=dp.ID),stock=0,syn=2)
        except:
            get_logger("general").debug(traceback.format_exc())
