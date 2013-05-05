#coding:utf8
from webapp.settings import dbconn
import web


def getindexsps():
    return dbconn.query("select * from shopping where picked=1 and wdate > '2013-05-03 22:00:00' order by score desc limit 30 ")

def getsp(spid):
    return web.listget(dbconn.query("select * from shopping where id=$spid",vars=dict(spid=spid)),0,None)

def getfamsp(pid):
    return dbconn.query("select * from shopping where pid = $pid and picked=0 order by score desc",vars=dict(pid=pid))


##score-(timestampdiff(second,udate,now()))/864 desc
