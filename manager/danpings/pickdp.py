#coding:utf-8
import traceback
from manager.danpings import getdata 
from manager.models import danpings
from manager.settings import filter_class
from helpers.prices import getRuyiHtml,getCpdata,getRuyiSearch,getCpdataFromSearch
from helpers.utils import price
from helpers.b2c import factory
from helpers.loggers import get_logger


    
def collect(source):
    s = getdata.factory(source)
    s.getNewlist()
    s.getlist()
    s.insert()

def filter1st():
    dps = danpings.findstatus(0)
    for dp in dps:
        try:
            if dp.srcurl is None or dp.price is None or dp.market is None:
                danpings.updatestatus(dp.ID,-9)
        except:
            danpings.updatestatus(dp.ID,-9)
            get_logger("general").debug(traceback.format_exc())

def filterclass():
    dps = danpings.findstatus(0)
    for dp in dps:
        try:
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
        except:
            danpings.updatestatus(dp.ID,-1)
            get_logger("general").debug(traceback.format_exc())

def updatecpprice():
    dps = danpings.findstatus(1)
    for dp in dps:
        try:
            can_market = {"jd":"","dangdang":"","zcn":""}
            if can_market.has_key(dp.market):
                del can_market[dp.market]
            html = getRuyiHtml(dp.srcurl)
            print "getRuyi......"
            ##print html
            datalist = getCpdata(html)
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

            print "getRuyiSearch....."
            ##print can_market
            datalist = getRuyiSearch(dp.name)
            if datalist:
                ##print "datalenth: " +  str(len(datalist))
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
            ##print can_market
            datalist = getCpdataFromSearch(dp.name,can_market.keys())
            ##print len(datalist)
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
        except:
            danpings.updatestatus(dp.ID,-2)
            get_logger("general").debug(traceback.format_exc())
        

def filter_price():
    dps = danpings.findstatus(2)
    for dp in dps:
        try:
            min_price = danpings.getmatch_min(dp.ID)
            if price(dp.price,dp.currency) > min_price:
                danpings.updatestatus(dp.ID,-3)
            else:
                danpings.updatestatus(dp.ID,3)
        except:
            danpings.updatestatus(dp.ID,-3)
            get_logger("general").debug(traceback.format_exc())

#http://pn.zdmimg.com/201306/05/eef7e34.jpg_n3.jpg
def imageprocess():
    dps = danpings.findstatus(3)
    for dp in dps:
        try:
            if dp.img.find("zdmimg.com") > -1:
                print dp.market
                b2c_item = factory(dp.market)
                b2c_item.itemid = dp.itemid
                b2c_item.itemhtml = b2c_item.getItemHtml()
                image = b2c_item.getimg()
                if image:
                    danpings.update(dp.ID,image = image)
                    danpings.updatestatus(dp.ID,4)
                else:    
                    danpings.updatestatus(dp.ID,-4)
            else:
                danpings.update(dp.ID,image = dp.img)
                danpings.updatestatus(dp.ID,4)
        except:
            danpings.updatestatus(dp.ID,-4)
            get_logger("general").debug(traceback.format_exc())
        
    

def insertinttoformaldp():
    dps = danpings.findstatus(4)
    for dp in dps:
        danpings.insert_formal(dp)
        danpings.updatestatus(dp.ID,5)


def startupdate(source):
    collect(source)
    filter1st()
    filterclass()
    updatecpprice()
    filter_price()
    imageprocess()
    insertinttoformaldp()

    
