#coding:utf8
from webapp.settings import dbconn
import web


def getindexsps():
    return dbconn.query("select * from shopping where picked=1 order by score desc limit 20 ")

def getsp(spid):
    return web.listget(dbconn.query("select * from shopping where id=$spid",vars=dict(spid=spid)),0,None)

def getfamsp(pid):
    return dbconn.query("select * from shopping where pid = $pid and picked=0 order by score desc",vars=dict(pid=pid))
