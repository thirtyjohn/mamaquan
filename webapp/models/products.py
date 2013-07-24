#coding:utf8
from webapp.settings import dbconn,static_leibie,static_tp,tp_same
import web

def getprs(tp,qdict):
    condis = list()
    for k,v in qdict.items():
        condis.append(k+"='"+v+"'")
    sql = "select * from product p join "+static_tp[tp]["tablename"] + " q on p.id = q.id "
    if len(condis) > 0:
        sql = sql + " where stock = 1 and " + " and ".join(condis)
    res = dbconn.query(sql)
    return res


def getlbs(tp,qdict):
    qdict = qdict.copy()
    """
    每个属性获取 在其他属性限制下的当前属性的所有属性值
    """
    for lb in static_leibie[tp]:
        if not lb[0] in qdict.keys():
            qdict.update({lb[0]:None})


    cols = qdict.keys()
    sqls = list()
    for i in range(len(cols)):
        sql = "select distinct "+cols[i]+" as v, '"+cols[i]+"' as k from product p join "+static_tp[tp]["tablename"] + " q on p.id = q.id "
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
    return web.listget(dbconn.query("select * from product p join "+static_tp[tp]["tablename"]+" q on p.id = q.id where p.id=$prid",
                    vars=dict(prid=prid)),0,None)

def getpritems(prid):
    return dbconn.query("select * from prmatch where prid = $prid  order by price ",vars=dict(prid=prid))

def getotherprs(pr):
    sql = "select * from product p join "+static_tp[pr.prtype]["tablename"]+" q on p.id = q.id where p.id <> $prid "
    dict_vars = dict(prid=pr.ID)
    for c in tp_same[pr.prtype]:
        sql = sql + " and "+c+" = $"+c
        dict_vars.update({c:pr[c]})
    return dbconn.query(sql,vars=dict_vars)


def getindexpr():
    pr = web.listget(dbconn.query("select * from product p join naifen q on p.id = q.id where p.id = 100094"),0,None)
    prmatch = dbconn.query("select * from prmatch where prid = $prid and stock=1 order by price",vars=dict(prid=pr.ID))
    return (pr,prmatch)


