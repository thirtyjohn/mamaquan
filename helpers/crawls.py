#coding:utf-8
import urllib2,time
from urllib2 import HTTPError
from helpers.loggers import get_logger

isCrawlling = False

failurecount = 0

MAX_FAILCOUNT = 20


"""
可增加一个缓存逻辑
"""

def getUrl(url):
    global isCrawlling
    if isCrawlling:
        time.sleep(1)
        getUrl(url)
    else:
        isCrawlling = True
        resp = crawl(url)
        isCrawlling = False
    return resp


def crawl(url):
    global failurecount
    try:
        resp = urllib2.urlopen(url)
    except HTTPError,e:
        get_logger("crawl").debug(str(e.code)+":"+url)
        failurecount += 1
        return None
    if needreset():
        resetip()
    return resp

def needreset():
    return failurecount > MAX_FAILCOUNT

def resetip():
    global failurecount
    failurecount = 0
    pass

def isfailure(resp):
    return False
