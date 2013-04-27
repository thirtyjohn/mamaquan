#coding:utf-8
from settings import dbconn,render,static_leibie,static_tp
import web,json
from webapp.models import shoppings,products
from helpers.utils import _xsseccape


class index:
    def GET(self):
        itemlist = dbconn.query("select * from formalitem order by generalscore desc limit 20 ")
        """
        for r in res:
            itemlist.append(r)
        
        pid = 0
        product = None
        for r in res:
            if r.pid <> pid:
                if product:
                    productlist.append(product)
                pid = r.pid
                product = {"gooditem":r,"famitems":[]}
            else:
                product["famitems"].append(r)
        print len(productlist)
        productlist = sorted(productlist,key=lambda product:product["gooditem"].generalscore ,reverse=True)
        """
        ##itemlist = sorted(itemlist,key=lambda item:item.generalscore ,reverse=True)
        return render.index(itemlist=itemlist)



class shoppingitem:
    def GET(self,name):
        spid = int(name)
        data = web.input()
        sp = shoppings.getsp(spid)
        famsps = shoppings.getfamsp(sp.pid)
        if data.has_key("type") and data["type"] == "json":
            return json.dumps({"html":render.spjson(sp=sp,famsps=famsps)})



class mulu:
    def GET(self):
        return render.muluindex()



class productsearch:
    def GET(self,tp):

        
        
        qd= {
            u"naifen":
                {
                u"d":u"duan",
                u"s":u"series",
                u"p":u"place",
                u"b":u"brand"
                },
             u"niaobu":
                {
                u"b":u"brand"    
                },
            }

        dq= {
            u"naifen":
                {
                u"duan":u"d",
                u"series":u"s",
                u"place":u"p",
                u"brand":u"b"
                },
             u"niaobu":
                {
                u"brand":u"b"    
                },
            }

        qs = list()
        qdict = dict()
        """
        {"duan":u"1","series":u"fdf",}
        """
        data = web.input()
        data_q = None
        if data.has_key("q"):
            data_q = data["q"]
            qs = data["q"].split(",")
        print data_q
        print qs
        for q in qs:
            print q
            nv = q.split(u":") if len(q.split(":"))==2 else None
            if not nv:
                continue
            n = nv[0]
            v = nv[1]
            if n and n in qd[tp].keys() and _xsseccape(v):
                qdict.update({qd[tp][n]:v})
        print qdict
        prlist = products.getprs(tp,qdict)

        """
        where = ""
        for k,v in qdict.items():
            if v:
                where = where + " and "+k+"= "+v

        
        lbdict =dict()
        for v in qd[tp].values():
            lbdict.update({v:[]})

        """
        
        """
        prs =list()
        for r in products.getprs(tp,where=where):
            prs.append(r)
            for col in lbdict.keys():
                icount = 0
                for d in lbdict[col]:
                    if r[col] == d.key:
                        d.update({d.key:d.v+1})
                        icount = 1
                        continue
                if icount == 0:
                    lbdict[col].append({r[col]:1})
        """
        """
        有一个固定列表
        如果总项数小于7，就不用重排序
        如果总项数大于7，有的按数量排，没的原定排
        """
        lbvs = list()
        for r in products.getlbs(tp,qdict):
            print r.name
            lbvs.append(r.name)
        lblist = list()
        for lb in static_leibie[tp]:
            vlist = list()
            for static_v in lb[2]:
                if static_v in lbvs:
                    vlist.append({"name":lb[3][static_v],"value":static_v,"checked":1 if static_v in qdict.values() else 0})
            if len(vlist) > 0:
                lblist.append((dq[tp][lb[0]],lb[1],vlist))

        """
        [("duan","阶段",[{1段:4},{}]),]
        """
        
        return render.products(prlist=prlist,lblist=lblist,tp=tp,data_q=data_q)

class product:
    def GET(self,tp,prid):
        if tp not in static_tp.keys():
            return web.notfound()
        pr = products.getpr(tp,prid)
        if not pr:
            return web.notfound()
        pritems = products.getpritems(tp,prid)
        otherprs = products.getotherprs(tp,prid)
        return render.product(tp=tp,pr=pr,pritems=pritems,otherprs=otherprs)


"""
from analyscript import genItemUrl
from analyscript import getExtra,insertmap,insertnaifen,deallater,getjiaoyan,getqueshi
class matchitem:
    def GET(self):
        data = web.input()
        if data.has_key("act"):
            act = data.act
            itemid = data.itemid if data.has_key("itemid") else None
            market = data.market if data.has_key("market") else None
            naifenid = data.naifenid if data.has_key("naifenid") else None

            if act == "new":
                newid = insertnaifen(itemid,market)
                insertmap(itemid,newid,market)
            elif act == "later":
                deallater(itemid,market)
            elif act == "match":
                insertmap(itemid,naifenid,market)
        brand = data.brand if data.has_key("brand") else None
        market = data.market if data.has_key("market") else None
        famlist = getExtra(brand,market) if brand and market else list()

        brandlist = dbconn.query("select distinct brand from naifen")
        marketlist = dbconn.query("select distinct market from naifen")

        return render.matchitem(famlist=famlist,brandlist=brandlist,marketlist=marketlist)      

class mmredict:
    def GET(self):
        data = web.input()
        naifenid = data.naifenid
        r = web.listget(dbconn.query(
            select n.itemid,n.market from naifenmatch m
            join naifen n
            on m.itemid = n.itemid and m.market = n.market
            where m.naifenid = $naifenid
        ,vars=dict(naifenid=naifenid)),0,None)
        if r:
            return web.seeother(genItemUrl(r.itemid,r.market))
        


class check:
    def GET(self):
        data = web.input()
        if data.has_key("act") and data["act"] == "ok":
            dbconn.update("formalnaifen",checked=1,where="id=$naifenid",vars=dict(naifenid=int(data["id"])))
            return web.seeother("/jiaoyan")
        res_list = getjiaoyan()
        return render.jiaoyan(res_list=res_list)

class queshi:
    def GET(self):
        res_list = getqueshi()
        return render.queshi(res_list=res_list)


class editnaifen:
    def GET(self):
        data = web.input()
        naifenid = int(data["id"])
        nf = web.listget(dbconn.query("select * from formalnaifen where id = $naifenid",vars=dict(naifenid=naifenid)),0,None)
        return render.editnaifen(nf=nf)
    
    def POST(self):
        data = web.input()
        naifenid = int(data["id"])
        tag = data["tag"] if data["tag"] <> "" or data["tag"] <> "None" else None
        dbconn.update("formalnaifen",weight=int(data["weight"]),duan=int(data["duan"]),series=data["series"],tag=tag,where="id=$naifenid",vars=dict(naifenid=naifenid))
        return web.seeother("/jiaoyan")



class naifen:
    def GET(self,name):
        naifenid = int(name)
        nf = web.listget(dbconn.query("select * from formalnaifen where id = $naifenid",vars=dict(naifenid=naifenid)),0,None)
        
        nfs = dbconn.query(
                select n.price,n.market,n.itemid from naifenmatch m
                join formalnaifen f
                on f.id = m.naifenid
                join naifen n
                on m.itemid = n.itemid and m.market = n.market
                where f.id= $naifenid
        ,vars=dict(naifenid=naifenid))
        return render.naifen(nf=nf,nfs=nfs)

"""
