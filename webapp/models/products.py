#coding:utf8
from webapp.settings import dbconn,static_leibie,static_tp,tp_same
import web

def getprs(tp,qdict):
    condis = list()
    for k,v in qdict.items():
        condis.append(k+"='"+v+"'")
    sql = "select * from "+static_tp[tp]["tablename"]
    if len(condis) > 0:
        sql = sql + " where " + " and ".join(condis)
    res = dbconn.query(sql)
    return res


def getlbs(tp,qdict):
 
    for lb in static_leibie[tp]:
        if not lb[0] in qdict.keys():
            qdict.update({lb[0]:None})


    cols = qdict.keys()
    sqls = list()
    for i in range(len(cols)):
        sql = "select distinct "+cols[i]+" as name from "+static_tp[tp]["tablename"]
        wheres = list()
        for j in range(len(cols)):
            if i==j or qdict[cols[j]] is None:
                continue
            else:
                wheres.append(cols[j]+"= '"+qdict[cols[j]]+"'")
        if len(wheres) > 0:
            sqls.append(sql +" where "+ " and ".join(wheres))
        else:
            sqls.append(sql)
    res = dbconn.query((" union ").join(sqls))
    return res



def getpr(tp,prid):
    return web.listget(dbconn.query("select * from "+static_tp[tp]["tablename"]+" where id=$prid",vars=dict(prid=prid)),0,None)

def getpritems(prid):
    return dbconn.query("select * from prmatch where prid = $prid ",vars=dict(prid=prid))

def getotherprs(tp,prid):
    sql = ""
    for c in tp_same[tp]:
        sql = sql + " and p."+c+" = n."+c
    return dbconn.query("select n.* from "+static_tp[tp]["tablename"]+" p join "+static_tp[tp]["tablename"]+" n on p.id =$prid and n.id <> $prid"+sql,vars=dict(prid=prid))

