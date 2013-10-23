#coding:utf8
import pymongo
class mongo:
    def __init__(self,ip,port,dbname):
        client = pymongo.MongoClient(ip, port)
        self.db = client[dbname]
    def insert(self,tablename,data):
        return self.db[tablename].insert(data)
    def query(self,tablename,where=None,**kwargs):
        return self.db[tablename].find(where,**kwargs) if where else self.db[tablename].find(**kwargs)
    def query_one(self,tablename,where=None,**kwargs):
        return self.db[tablename].find_one(where,**kwargs) if where else self.db[tablename].find_one(**kwargs)
    def update(self,tablename,where,data):
        return self.db[tablename].update(where,{"$set":data},multi=True)
    def aggregate(self,tablename,pipeline):
        return self.db[tablename].aggregate(pipeline)
