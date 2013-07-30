#!/usr/bin/python
#coding:utf-8

import web

urls = (
    "/","webapp.controllers.browse.index",
    "/shopping/(\d+)","webapp.controllers.browse.shoppingitem",
    "/danpin/(\d+)","webapp.controllers.browse.danpingitem",
    "/shopping/(\d+)/delete","webapp.controllers.action.delitem",
    "/mulu","webapp.controllers.browse.mulu",
    "/(naifen|niaobu|wanju|baojian)","webapp.controllers.browse.productsearch",
    "/(naifen|niaobu|wanju|baojian)/s","webapp.controllers.browse.productsearch",
    "/(naifen|niaobu|wanju|baojian)/(\d+)","webapp.controllers.browse.product",
)


app = web.application(urls,globals())
application = app.wsgifunc()
