#coding:utf-8
import web
from settings import dbconn

def insertpre(itemid,market):
    dbconn.query("insert into prenaifen (name,duration,weight,spec,brand,series,sellto,age,duan,pack,place,price,img) select name,duration,weight,spec,brand,series,sellto,age,duan,pack,place,price,img from naifen where itemid = $itemid and market=$market",vars=dict(itemid=itemid,market=market))
    ""
    return web.listget(dbconn.query("SELECT last_insert_id() as newid"),0,None).newid

def deallater(itemid,market):
    dbconn.update("naifen",where="itemid=$itemid and market=$market",vars=dict(itemid=itemid,market=market),matchlater=1)

