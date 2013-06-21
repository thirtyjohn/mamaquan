#coding:utf8
from webapp.settings import dbconn
import web

def getindexdps():
    dplist = list()
    dpids = list()
    res = dbconn.query("select * from danping order by id desc limit 5 ")
    for r in res:
        dplist.append((r,[]))
        dpids.append(r.ID)
    res = dbconn.query("""
        select * from danpingmatch
        where dpid in $dpids
        order by dpid,price
    """,vars=dict(dpids=dpids))
    match_dict = {}
    for r in res:
        if match_dict.has_key(r.dpid):
            match_dict[r.dpid].append(r)
        else:
            match_dict.update({r.dpid:[r]})

    for dp in dplist:
        dp[1].extend(match_dict[dp[0].ID])

    return dplist

def getdp(dpid):
    return web.listget(dbconn.query("select * from danping where id = $dpid",vars=dict(dpid=dpid)),0,None)
