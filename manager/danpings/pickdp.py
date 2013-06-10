#coding:utf-8
import getdata
from manager.models import danpings
from manager.settings import filter_class
from helpers.prices import getRuyiHtml,getCpdata,getRuyiSearch,getCpdataFromSearch

def collect():
    s = getdata.Smzdm()
    s.getNewlist()
    s.getlist()
    s.insert()

def filter():
    dps = danpings.findstatus(0)
    for dp in dps:
        if dp.srcurl is None or dp.price is None or dp.market is None:
            danpings.updatestatus(dp.ID,-9)

def filterclass():
    dps = danpings.findstatus(0)
    for dp in dps:
        c_ok = False
        if not dp.itemclass:
            danpings.updatestatus(dp.ID,-1)
            continue
        classlist = dp.itemclass.split("$") 
        for c in classlist:
            if c in filter_class[dp.source]:
                c_ok = True
                continue
        if c_ok:
            danpings.updatestatus(dp.ID,1)
        else:
            danpings.updatestatus(dp.ID,-1)

def updatecpprice():
    dps = danpings.findstatus(1)
    for dp in dps:
        html = getRuyiHtml(dp.srcurl)
        print "getRuyi......"
        print html
        datalist = getCpdata(html)
        if datalist:
            for d in datalist:
                danpings.insertmatch(dp.ID,d)
            danpings.updatestatus(dp.ID,2)
            continue

        can_market = {"jd":"","dangdang":"","zcn":""}
        if can_market.has_key(dp.market):
            del can_market[dp.market]

        print "getRuyiSearch....."
        print can_market
        datalist = getRuyiSearch(dp.name)
        if datalist:
            print "datalenth: " +  str(len(datalist))
            for d in datalist:
                if len(can_market.keys()) == 0:
                    break
                if d.market in can_market.keys():
                    danpings.insertmatch(dp.ID,d)
                    del can_market[d.market]
        if len(can_market.keys()) < 2:
            danpings.updatestatus(dp.ID,2)
            continue

        print "getFromSearch....."
        print can_market
        datalist = getCpdataFromSearch(dp.name,can_market.keys())
        print len(datalist)
        if datalist:
            for d in datalist:
                if len(can_market.keys()) == 0:
                    break
                if d.market in can_market.keys():
                    danpings.insertmatch(dp.ID,d)
                    del can_market[d.market]
        if len(can_market.keys()) < 2:
            danpings.updatestatus(dp.ID,2)
            continue


        danpings.updatestatus(dp.ID,-2)
        

def filter_price():
    dps = danpings.findstatus(2)
    for dp in dps:
        avg = danpings.getavg_match(dp.ID)
        if dp.price/avg > 0.9:
            danpings.updatestatus(dp.ID,-3)
        else:
            danpings.updatestatus(dp.ID,3)


def imageprocess():
    findstatus()
    

def insertinttoformaldp():
    findstatus()
    updatestatus()

   


def startupdate():
    collect()
    filter_class()
    updatecpprice()
    filter_price()
    imageprocess()
    insertinttoformaldp()

    
