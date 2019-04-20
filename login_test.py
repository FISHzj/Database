from connectmdb import *
from bson.objectid import ObjectId
login=Connectmdb()
def login_test(login,password,username='',wechatnum='',num=''):#输入用户名，密码，或者微信号，学号进行登录验证
    if not (username or wechatnum or num):
        raise ValueError('no input!')
    if not isinstance(password,str) and isinstance(username,str) and isinstance(wechatnum,str) and isinstance(num,str):
        raise TypeError('invalid password','invalid username','invalid wechatnum','invalid num')
    if login._db.account.find_one({'password':password,'$or':[{'wechatnum':wechatnum},{'id':num},{'username':username}]}):
        _id=ObjectId(login._db.account.find_one({'password':password,'$or':[{'wechatnum':wechatnum},{'num':num},{'username':username}]})['_id'])
        _condition={'_id':_id}
        print('Log in successfully for %s!'%password)
        _wechatnum=login._db.account.find_one(_condition)['wechatnum']
        _num=login._db.account.find_one(_condition)['num']
    else:
        raise ValueError('username','password','wechatnum','num')
def query_wechatnum(login,wechatnum=''):#判断微信号是否存在
    if login._db.account.find_one({'wechatnum':wechatnum}):
        return True
    else:
        return False
def username(login,_condition):#_condition是查询条件，从login中获取
    _username = login._db.account.find_one(_condition)['username']
    return _username
def set_username(login,_condition,username):
    if not isinstance(username,str):
        raise TypeError('invalid username')
    if login._db.account.update_one(_condition,{'$set':{'username':username}}):
        return True
    else:
        return False

