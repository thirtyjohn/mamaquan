#!/usr/bin/env python
#coding:utf-8
import web



urls = (
    "/match","manager.controllers.browse.match",
    "/aggr","manager.controllers.browse.aggr",
    "/mmredict","manager.controllers.browse.mmredict",
    "/jiaoyan","manager.controllers.browse.check",
    "/editnaifen","manager.controllers.browse.editnaifen",
    "/queshi","manager.controllers.browse.queshi",
    "/naifen/(\d+)","manager.controllers.browse.naifen",
)

app = web.application(urls,globals())

        
if __name__ == "__main__":
    app.run()
