#coding:utf-8
import web
from web.contrib.template import render_mako

render = render_mako(
        directories=['webapp/templates'],
        input_encoding='utf-8',
        output_encoding='utf-8'
        )

dbconn = web.database(dbn='mysql', user="root", host="127.0.0.1", db="interest")
localdir = "/Users/macbookpro/workspace/interest/taobaoyouhui/"


static_leibie = {
    "naifen":
        [
        ("brand",u"品牌",[u"Wyeth/惠氏",u"Abbott/雅培",u"Dumex/多美滋"],{u"Wyeth/惠氏":u"Wyeth/惠氏",u"Abbott/雅培":u"Abbott/雅培",u"Dumex/多美滋":u"Dumex/多美滋"}),
        ("duan",u"阶段",[u"1",u"2",u"3",u"4",u"0"],{u"1":u"1段",u"2":u"2段",u"3":u"3段",u"4":u"4段",u"0":u"0段"}),
        ("series",u"系列",[u"启赋",u"幼儿乐",u"膳儿加",u"优阶",u"菁智"],{u"启赋":u"启赋",u"幼儿乐":u"幼儿乐",u"膳儿加":u"膳儿加",u"优阶":u"优阶",u"菁智":u"菁智"}),
        ],

    "niaobu":[],
}

static_title = {
    "naifen":u"奶粉",    
}
 
