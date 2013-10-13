#coding:utf8
import pymongo
class mongo:
    def __init__(self,ip,port,dbname):
        client = pymongo.MongoClient(ip, port)
        self.db = client[dbname]
    def insert(self,tablename,data):
        self.db[tablename].insert(data)
    def query(self,tablename,where=None):
        return self.db[tablename].find(where) if where else self.db[tablename].find()
    def query_one(self,tablename,where=None):
        return self.db[tablename].find_one(where) if where else self.db[tablename].find_one()
