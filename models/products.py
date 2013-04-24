#coding:utf8
from settings import dbconn

def insertmap(itemid,naifenid,market):
    dbconn.insert("naifenmatch",itemid=itemid,naifenid=naifenid,market=market)
