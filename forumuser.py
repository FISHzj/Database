from connectmdb import *
import bson.binary
forumuser=Connectmdb(hostname='localhost',port=27014,database='myclass')
class Forumuser:
    def __init__(self,num,nickname,photo,photoback):
        if not isinstance(num,str) and isinstance(nickname,str) and isinstance(photo,str):
            raise TypeError('num','nickname','photo')
        if not photo.endswith(('.jpg','.jpeg','.png','.bmp','.gif')):
            raise TypeError('photo')
        with open(photo,'rb') as f:
            content=bson.binary.Binary(f.read())
            forumuser._db.forumuser.insert_one({'num':num,'nickname':nickname,'photoname':f.name,'photodata':content})
        forumuser._id = ObjectId(forumuser._db.forumuser.find_one({'num': num})['_id'])
        forumuser._condition = {'_id':forumuser._id}
        self._num=forumuser._db.forumuser.find_one(forumuser._condition)['num']
        self._nickname=forumuser._db.forumuser.find_one(forumuser._condition)['nickname']
        data = forumuser._db.forumuser.find_one(forumuser._condition)
        self._photo=photoback
        with open(self._photo, 'wb') as f:
            f.write(data['photodata'])
    def getNum(self):
        return self._num
    def getNickName(self):
        return self._nickname
    def setNickName(self,newnickname):
        if not isinstance(newnickname,str):
            raise TypeError('the nickname')
        if forumuser._db.forumuser.update_one(forumuser._condition,{'$set':{'nickname':newnickname}}):
            return True
        else:
            return False
    def getPhoto(self):
        return self._photo








