#coding:utf-8
import web,json
from manager.settings import render
from manager.products.product_init import get_fam_to_match,aggr_attr,aggr_val,gen_product_attr,verify_product,verify_product_match
from manager.models import products
from bson.objectid import ObjectId
from manager.settings import mongoconn

class match:
    def POST(self):
        data = web.input()
        item_fams = None
        if data.has_key("json") and data["json"]:
            d = json.loads(data["json"])
            item_fams = get_fam_to_match(**d)
        return render.match(item_fams=item_fams)

    def GET(self):
        return render.match(item_fams=None)

class matchdata:
    def POST(self):
        data = web.input()
        if data.action == "match":
            item = products.get_item( _id=ObjectId(data.item) )[0]
            pr = products.get_product( _id=ObjectId(data.pr) )[0]
            products.add_pr_match(item=item,pr=pr)
        elif data.action == "add":
            item = products.get_item( _id=ObjectId(data.item) )[0]
            pr = gen_product_attr(item)
            pr.match_ids = [item["_id"]] 
            products.insert_product(pr)
        return json.dumps({u"html":u"ok"}) 

class aggr:
    def POST(self):
        data = web.input()
        cond = None
        if data.has_key("json") and data["json"]:
            cond = json.loads(data["json"])
        else:
            return None
        
        if data.aggr == "attr":
            aggrlist = aggr_attr(**cond)
        elif data.aggr == "val":
            aggrlist = aggr_val(data.table,**cond)
    
        return render.aggr(aggrlist=aggrlist,aggr_type=data.aggr,json=data["json"] if data.has_key("json") else "")

    def GET(self):
        return render.aggr()


class verifydata:
    def GET(self):
        return render.verify()

    def POST(self):
        data = web.input()
        cond = None
        if data.has_key("json") and data["json"]:
            cond = json.loads(data["json"])
        else:
            return None
        verify_type = data["type"]
        if verify_type == "product":
            verify_res = verify_product(**cond)
            verify_list = list()
            for k,v in verify_res.items():
                verify_list.append((k,v))
            verify_list = sorted(verify_list, key=lambda x:len(x[1]) ,reverse=True)
            verify_copy = list()
            for i in range(0,len(verify_list)):
                pr = products.get_product(_id=ObjectId(verify_list[i][0]))[0]
                cps = []
                for j in range(0, len(verify_list[i][1])):
                    cps.append( (products.get_product(_id=ObjectId(verify_list[i][1][j][0]))[0],verify_list[i][1][j][1]))
                verify_copy.append((pr,cps))
        else:
            verify_copy = verify_product_match(**cond)
        return render.verify(verify_list=verify_copy,json=data["json"] if data.has_key("json") else "",verify_type=verify_type)
 

class viewdata:
    def POST(self):
        data = web.input()
        rows = None
        if data.has_key("json") and data["json"]:
            cond = json.loads(data["json"])
            tablename = cond.pop("table") 
            if cond.has_key("_id"):
                cond["_id"] = ObjectId(cond["_id"])
            rows = mongoconn.query(tablename,cond)
        return render.viewdata(rowsd=rows,json=data["json"] if data.has_key("json") else "")

    def GET(self):
        return render.viewdata(rowsd=None)


class data:
    def GET(self):
        data = web.input()
        item = mongoconn.query_one(data["table"],{"_id":ObjectId(data["dataid"])})
        return json.dumps({"html":render.data(item=item)})


"""
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
        r = web.listget(dbconn.query("select n.itemid,n.market from formalprmatch m
            join naifenitem n
            on m.itemid = n.itemid and m.market = n.market
            where m.naifenid = $naifenid
        ",vars=dict(naifenid=naifenid)),0,None)
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
    
  " def POST(self):
        data = web.input()
        naifenid = int(data["id"])
        tag = data["tag"] if data["tag"] <> "" or data["tag"] <> "None" else None
        dbconn.update("formalnaifen",weight=int(data["weight"]),duan=int(data["duan"]),series=data["series"],tag=tag,where="id=$naifenid",vars=dict(naifenid=naifenid))
        return web.seeother("/jiaoyan")



class naifen:
    def GET(self,name):
        naifenid = int(name)
        nf = web.listget(dbconn.query("select * from formalnaifen where id = $naifenid",vars=dict(naifenid=naifenid)),0,None)
        
        nfs = dbconn.query("
                select n.price,n.market,n.itemid from prmatch m
                join formalnaifen f
                on f.id = m.naifenid
                join naifenitem n
                on m.itemid = n.itemid and m.market = n.market
                where f.id= $naifenid
        ",vars=dict(naifenid=naifenid))
        return render.naifen(nf=nf,nfs=nfs)

"""
