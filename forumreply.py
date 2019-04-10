from connectmdb import *
from bson.objectid import ObjectId
from time import strftime
import bson.binary
forumreply=Connectmdb()
class Forumreply:
    def __init__(self,reply,num,replyback):
        if not isinstance(reply,str) and isinstance(num,str) and isinstance(replyback,str):
            raise TypeError('reply','num','replyback')
        if not reply.endswith(('.txt','.docx','.doc','.wps','.xls','.pdf','.jpeg','.jpg','.png','.bmp','.gif')):
            raise TypeError('reply')
        self._time = strftime("%Y-%m-%d %H:%M:%S")
        with open(reply,'rb') as f:
            content=bson.binary.Binary(f.read())
            forumreply._db.forumreply.insert_one({'reply':content,'auther':num,'date':self._time})
        self._id=ObjectId(forumreply._db.forumreply.find_one({'auther':num})['_id'])
        self._condition={'_id':self._id}
        self._reply=replyback
        data=forumreply._db.forumreply.find_one(self._condition)
        with open(self._reply,'wb') as f:
            f.write(data['reply'])
        self._authername=forumreply._db.forumuser.find_one({'num':num})['nickname']
        self._authernum=forumreply._db.forumreply.find_one(self._condition)['num']
    def getAuthername(self):
        return self._authername
    def getAuthernum(self):
        return self._authernum
    def getReply(self):
        return self._reply
    def getTime(self):
        return self._time





