#coding:utf8
from settings import dbconn,static_leibie
import web

def getprs(tp,qdict):
    if tp=="naifen":
        tablename = "formalnaifen"
    condis = list()
    for k,v in qdict.items():
        condis.append(k+"='"+v+"'")
    sql = "select * from "+tablename
    if len(condis) > 0:
        sql = sql + " where " + " and ".join(condis)
    res = dbconn.query(sql,vars=dict(tablename=tablename)
    )
    return res


def getlbs(tp,qdict):

    if tp == "naifen":
        tablename = "formalnaifen"
    for lb in static_leibie[tp]:
        if not lb[0] in qdict.keys():
            qdict.update({lb[0]:None})


    cols = qdict.keys()
    sqls = list()
    for i in range(len(cols)):
        sql = "select distinct "+cols[i]+" as name from "+tablename
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


