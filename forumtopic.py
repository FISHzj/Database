from connectmdb import *
from bson.objectid import ObjectId
from time import strftime
import bson.binary
forumtopic=Connectmdb()
import os
class Forumtopic:
    def __init__(self,title,topic,num,topicback):
        if not isinstance(title,str) and isinstance(topic,str) and isinstance(num,str):
            raise TypeError('title','topic','num')
        if not topic.endswith(('.txt','.docx','.doc','.wps','.xls','.pdf','.jpeg','.jpg','.png','.bmp','.gif')):
            raise TypeError('topic')
        self._time = strftime("%Y-%m-%d %H:%M:%S")
        with open(topic,'rb') as f:
            content=bson.binary.Binary(f.read())
            forumtopic._db.forumtopic.insert_one({'title':title,'topicname':f.name,'topic':content,'auther':num,'date':self._time})
        self._id=ObjectId(forumtopic._db.forumtopic.find_one({'title': title})['_id'])
        self._condition={'_id':self._id}
        self._title=forumtopic._db.forumtopic.find_one(self._condition)['title']
        self._authernum=forumtopic._db.forumuser.find_one({'num':num})['num']
        self._authername = forumtopic._db.forumuser.find_one({'num': num})['nickname']
        self._topicback =os.path.join(topicback,os.path.basename(forumtopic._db.forumtopic.find_one(self._condition)['topicname']))
        self._num=num
    def getTitle(self):
        return self._title
    def getTopic(self):
        data = forumtopic._db.forumtopic.find_one(self._condition)
        with open(self._topicback, 'wb') as f:
            f.write(data['topic'])
    def getAuthername(self):
        return self._authername
    def getAuthernum(self):
        return self._authernum
    def get_sex(self):  # 发帖者的性别
        return forumtopic._db.student.find_one({'num': self._num})['sex']
    def getTime(self):
        return self._time









