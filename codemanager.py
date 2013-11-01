#!/usr/bin/env python
#coding:utf-8
import web



urls = (
    "/match","manager.controllers.browse.match",
    "/matchdata","manager.controllers.browse.matchdata",
    "/aggr","manager.controllers.browse.aggr",
    "/view","manager.controllers.browse.viewdata",
    "/data","manager.controllers.browse.data",
    "/verify","manager.controllers.browse.verifydata",
    "/mmredict","manager.controllers.browse.mmredict",
    "/jiaoyan","manager.controllers.browse.check",
    "/editnaifen","manager.controllers.browse.editnaifen",
    "/queshi","manager.controllers.browse.queshi",
    "/naifen/(\d+)","manager.controllers.browse.naifen",
)

app = web.application(urls,globals())
        
if __name__ == "__main__":
    app.run()
