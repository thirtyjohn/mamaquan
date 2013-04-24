#!/usr/bin/env python
#coding:utf-8
import web



urls = (
    "/","controllers.browse.index",
    "/match","controllers.browse.matchitem",
    "/mmredict","controllers.browse.mmredict",
    "/jiaoyan","controllers.browse.check",
    "/editnaifen","controllers.browse.editnaifen",
    "/queshi","controllers.browse.queshi",
    "/naifen/(\d+)","controllers.browse.naifen",
)

app = web.application(urls,globals())


        
if __name__ == "__main__":
    app.run()


