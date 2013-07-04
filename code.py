#!/usr/bin/env python
#coding:utf-8
import web



urls = (
    "/","webapp.controllers.browse.index",
    "/shopping/(\d+)","webapp.controllers.browse.shoppingitem",
    "/shopping/(\d+)/delete","webapp.controllers.action.delitem",
    "/mulu","webapp.controllers.browse.mulu",
    "/(naifen|niaobu|wanju|baojian)","webapp.controllers.browse.productsearch",
    "/(naifen|niaobu|wanju|baojian)/s","webapp.controllers.browse.productsearch",
    "/(naifen|niaobu|wanju|baojian)/(\d+)","webapp.controllers.browse.product",
)

app = web.application(urls,globals())

"""
    "/match","controllers.browse.matchitem",
    "/mmredict","controllers.browse.mmredict",
    "/jiaoyan","controllers.browse.check",
    "/editnaifen","controllers.browse.editnaifen",
    "/queshi","controllers.browse.queshi",
    "/naifen/(\d+)","controllers.browse.naifen",

"""
        
if __name__ == "__main__":
    app.run()


