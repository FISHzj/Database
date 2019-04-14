from connectmdb import *
from bson.objectid import ObjectId
import bson.binary
import os
forumuser=Connectmdb()
class Forumuser:
    def __init__(self,num,nickname,photo,photoback):
        if not isinstance(num,str) and isinstance(nickname,str) and isinstance(photo,str):
            raise TypeError('num','nickname','photo')
        if not photo.endswith(('.jpg','.jpeg','.png','.bmp','.gif')):
            raise TypeError('photo')
        with open(photo,'rb') as f:
            content=bson.binary.Binary(f.read())
            forumuser._db.forumuser.insert_one({'num':num,'nickname':nickname,'photoname':f.name,'photodata':content})
        self._photoback=photoback
        self._idd = ObjectId(forumuser._db.forumuser.find_one({'num': num})['_id'])
        self._condition = {'_id':self._idd}
        self._num = forumuser._db.forumuser.find_one(self._condition)['num']
    def getNum(self):
        return self._num
    def getNickName(self):
        self._nickname = forumuser._db.forumuser.find_one(self._condition)['nickname']
        return self._nickname
    def setNickName(self,newnickname):
        if not isinstance(newnickname,str):
            raise TypeError('the nickname')
        if forumuser._db.forumuser.update_one(self._condition,{'$set':{'nickname':newnickname}}):
            return True
        else:
            return False
    def getPhoto(self):
        photoname=forumuser._db.forumuser.find_one(self._condition)['photoname']#获取照片名称
        self._photo = os.path.join(self._photoback, os.path.basename(photoname))#路径+照片名
        data = forumuser._db.forumuser.find_one(self._condition)#取得数据库照片内容
        with open(self._photo, 'wb') as g:
            g.write(data['photodata'])
    def set_photo(self, newphoto):
        if not isinstance(newphoto, str):
            raise TypeError('newphoto')
        with open(newphoto, 'rb') as p:
            content = bson.binary.Binary(p.read())
            forumuser._db.forumuser.update_one(self._condition, {'$set': {'photodata': content}})
            forumuser._db.forumuser.update_one(self._condition, {'$set': {'photoname': p.name}})
    def sex(self):
        return forumuser._db.student.find_one({'num':self._num})['sex']
    #@classmethod
    #def class_getPhoto(cls,photoback,nickname='',num=''):
     #   if not isinstance(photoback,str):
      #      raise TypeError('photoback')
       # if num:
        #    data1=forumuser._db.forumuser.find_one({'num':num})
         #   with open(photoback, 'wb') as f:
          #      f.write(data1['photodata'])
        #elif nickname:
         #   data1 = forumuser._db.forumuser.find_one({'nickname': nickname})
          #  with open(photoback, 'wb') as f:
           #     f.write(data1['photodata'])
        #else:
         #   return False









