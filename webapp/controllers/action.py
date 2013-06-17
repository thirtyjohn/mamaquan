#coding:utf8
from webapp.models import shoppings,products
import web

class delitem:
    def GET(self,name):
        spid = int(name)
        shoppings.delete(spid)
        return web.seeother("/")

