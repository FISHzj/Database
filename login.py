from connectmdb import *
from bson.objectid import ObjectId
login=Connectmdb()
class Login:
    def __init__(self,password,username='',wechatnum='',num=''):
        if not (username or wechatnum or num):
            raise ValueError('no input!')
        if not isinstance(password,str) and isinstance(username,str) and isinstance(wechatnum,str) and isinstance(num,str):
            raise TypeError('invalid password','invalid username','invalid wechatnum','invalid num')
        if login._db.account.find_one({'password':password,'$or':[{'wechatnum':wechatnum},{'id':num},{'username':username}]}):
            self._id=ObjectId(login._db.account.find_one({'password':password,'$or':[{'wechatnum':wechatnum},{'num':num},{'username':username}]})['_id'])
            self._condition={'_id':self._id}
            print('Log in successfully!')
            self._username=login._db.account.find_one(self._condition)['username']
            self._password=login._db.account.find_one(self._condition)['password']
            self._wechatnum=login._db.account.find_one(self._condition)['wechatnum']
            self._num=login._db.account.find_one(self._condition)['num']
        else:
            raise ValueError('username','password','wechatnum','num')
    def num(self):
        return self._num
    def wechatnum(self):
        return self._wechatnum
    def password(self):
        return self._password
    def username(self):
        return self._username
    def set_username(self,username):
        if not isinstance(username,str):
            raise TypeError('invalid username')
        if login._db.account.update_one(self._condition,{'$set':{'username':username}}):
            return True
        else:
            return False
    def set_password(self,password):
        if not isinstance(password,str):
            raise TypeError('invalid password')
        if login._db.account.update_one(self._condition,{'$set':{'password':password}}):
            return True
        else:
            return False
