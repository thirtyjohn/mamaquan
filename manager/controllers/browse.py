#coding:utf-8
from manager.settings import dbconn,render
from manager.products.item2pre2formal import getExtra,getjiaoyan,getqueshi
from manager.models.products import insertmap,insertPreNf,deallater
import web
from helpers.b2c import factory,getItemUrl

class index:
    def GET(self):
        productlist = list()
        res = dbconn.query("select * from formalitem ")
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
        return render.index(productlist=productlist)



class matchitem:
    def GET(self):
        data = web.input()
        if data.has_key("act"):
            act = data.act
            itemid = data.itemid if data.has_key("itemid") else None
            market = data.market if data.has_key("market") else None
            prid = data.prid if data.has_key("prid") else None

            if act == "new":
                newid = insertPreNf(itemid,market)
                insertmap(itemid,newid,market)
            elif act == "later":
                deallater(itemid,market)
            elif act == "match":
                insertmap(itemid,prid,market)
        brand = data.brand if data.has_key("brand") else None
        market = data.market if data.has_key("market") else None
        famlist = getExtra(brand,market) if brand and market else list()

        brandlist = dbconn.query("select distinct brand from naifenitem")
        marketlist = dbconn.query("select distinct market from naifenitem")

        return render.matchitem(famlist=famlist,brandlist=brandlist,marketlist=marketlist)      

class mmredict:
    def GET(self):
        data = web.input()
        naifenid = data.naifenid
        r = web.listget(dbconn.query("""
            select n.itemid,n.market from formalprmatch m
            join naifenitem n
            on m.itemid = n.itemid and m.market = n.market
            where m.naifenid = $naifenid
        """,vars=dict(naifenid=naifenid)),0,None)
        if r:
            return web.seeother(getItemUrl(r.itemid,r.market))
        


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
        
        nfs = dbconn.query("""
                select n.price,n.market,n.itemid from prmatch m
                join formalnaifen f
                on f.id = m.naifenid
                join naifenitem n
                on m.itemid = n.itemid and m.market = n.market
                where f.id= $naifenid
        """,vars=dict(naifenid=naifenid))
        return render.naifen(nf=nf,nfs=nfs)


