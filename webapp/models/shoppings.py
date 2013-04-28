#coding:utf8
from settings import dbconn
import web

def getsp(spid):
    return web.listget(dbconn.query("select * from shopping where id=$spid",vars=dict(spid=spid)),0,None)

def getfamsp(pid):
    return dbconn.query("select * from shopping where pid = $pid and picked=0 order by generalscore desc",vars=dict(pid=pid))
