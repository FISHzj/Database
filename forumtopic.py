from connectmdb import *
from time import strftime
import bson.binary
forumtopic=Connectmdb(hostname='localhost',port=27014,database='myclass')
class Forumtopic:
    def __init__(self,title,topic,num,topicback):
        if not isinstance(title,str) and isinstance(topic,str) and isinstance(num,str):
            raise TypeError('title','topic','num')
        if not topic.endswith(('.txt','.docx','.doc','.wps','.xls','.pdf','.jpeg','.jpg','.png','.bmp','.gif')):
            raise TypeError('topic')
        self._time = strftime("%Y-%m-%d %H:%M:%S")
        with open(topic,'rb') as f:
            content=bson.binary.Binary(f.read())
            forumtopic._db.forumtopic.insert_one({'title':title,'topic':content,'auther':num,'date':self._time})
        forumtopic._id=ObjectId(forumtopic._db.forumtopic.find_one({'title': title})['_id'])
        forumtopic._condition={'_id':forumtopic._id}
        self._title=forumtopic._db.forumtopic.find_one(forumtopic._condition)['title']
        self._authernum=forumtopic._db.forumuser.find_one({'num':num})['num']
        self._authername=forumtopic._db.forumuser.find_one({'num':num})['nickname']
        data = forumtopic._db.forumtopic.find_one(forumtopic._condition)
        self._topic =topicback
        with open(self._topic, 'wb') as f:
            f.write(data['topic'])
    def getTitle(self):
        return self._title
    def getTopic(self):
        return self._topic
    def getAuthername(self):
        return self._authername
    def getAuthernum(self):
        return self._authernum
    def getTime(self):
        return self._time









