from pymongo import *
from bson.objectid import ObjectId
class Connectmdb:
    _client=None
    _db=None
    _collec=None
    _document=None
    _condition=None
    _id=None
    def __init__(self,hostname,port,database):
        if not  isinstance(hostname,str) and isinstance(port,int):
            raise TypeError('invalid hostname','invalid port')
        Connectmdb._client = MongoClient(hostname, port)
        if not isinstance(database,str):
            raise TypeError('invalid database')
        Connectmdb._db=Connectmdb._client[database]
        if Connectmdb._db.list_collection_names(session=None):
            print('Connect sucessfully with %s !'%database)
            self._hostname = hostname
            self._port = port
            self._database = database
        else:
            raise TimeoutError('connection refused!')
    @classmethod
    def login(cls,password,username=None,wechatnum=None,num=None):
        if not isinstance(password,str) and isinstance(username,str) and isinstance(wechatnum,str) and isinstance(num,str):
            raise TypeError('invalid password','invalid username','invalid wechatnum','invalid num')
        if Connectmdb._db.account.find_one({'password':password,'$or':[{'wechatnum':wechatnum},{'id':num},{'username':username}]}):
            Connectmdb._id=ObjectId(Connectmdb._db.account.find_one({'password':password,'$or':[{'wechatnum':wechatnum},{'num':num},{'username':username}]})['_id'])
            Connectmdb._condition={'_id':Connectmdb._id}
            print('Log in successfully!')
            return True
        else:
            return False
    @classmethod
    def username(cls):
        return Connectmdb._db.account.find_one(Connectmdb._condition)['username']
    @classmethod
    def set_username(cls,username):
        if not isinstance(username,str):
            raise TypeError('invalid username')
        if Connectmdb._db.account.update_one(Connectmdb._condition,{'$set':{'username':username}}):
            return True
        else:
            return False
    @classmethod
    def set_password(cls,password):
        if not isinstance(password,str):
            raise TypeError('invalid password')
        if Connectmdb._db.account.update_one(Connectmdb._condition,{'$set':{'password':password}}):
            return True
        else:
            return False
    @classmethod
    def password(cls):
        return Connectmdb._db.account.find_one(Connectmdb._condition)['password']
    @classmethod
    def wechatnum(cls):
        return Connectmdb._db.account.find_one(Connectmdb._condition)['wechatnum']
    @classmethod
    def num(cls):
        return Connectmdb._db.account.find_one(Connectmdb._condition)['num']
    @classmethod
    def querycollections(cls):
        return Connectmdb._db.list_collection_names(session=None)
    @classmethod
    def getcollection(cls,collec_name):
        Connectmdb._collec=collec_name
        return Connectmdb._collec
    @classmethod
    def disconnectmdb(cls):
        return Connectmdb._client.close()



