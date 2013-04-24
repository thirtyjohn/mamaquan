#coding:utf-8
import web
from web.contrib.template import render_mako

render = render_mako(
        directories=['templates'],
        input_encoding='utf-8',
        output_encoding='utf-8'
        )

dbconn = web.database(dbn='mysql', user="root", host="127.0.0.1", db="interest")
localdir = "/Users/macbookpro/workspace/interest/taobaoyouhui/"


