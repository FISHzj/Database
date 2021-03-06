import datetime
import pymongo
from bson.objectid import ObjectId
import re
import bson.binary
from connectmdb import *
import os
student=Connectmdb()
class Student:  #缺少photo
    _number=0
    def __init__(self,name,sex,birthday,ident,email,photo='',photoback='',schoolyear=0,group=0):
        if not (isinstance(name,str) and sex in ("男","女") and isinstance(ident,str) and isinstance(photo,str) and isinstance(photoback,str)):
            raise ValueError(name,sex,ident,photo,photoback)
        if not (isinstance(schoolyear,int) and isinstance(group,int)):
            raise  ValueError(schoolyear,group)
        try:
            birth=datetime.datetime(*birthday)
        except:
            raise ValueError("Wrong date",birthday)
        if isinstance(email,str):
            if not re.match(r"^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$",email):
                raise TypeError('Wrong type for the email!')
        if not photo.endswith(('.pdf', '.jpeg', '.jpg', '.png', '.bmp')):
             raise TypeError('topic')
        with open(photo, 'rb') as f:
            content = bson.binary.Binary(f.read())
            student._db.student.insert_one({'name':name,'sex':sex,'birthday':birth,'num':ident,'email':email,'photoname':f.name,'photo':content,
                                        'schoolyear':schoolyear,'group':group})
        self._photoback=photoback
        self._id=ObjectId(student._db.student.find_one({'num':ident})['_id'])
        self._condition={'_id':self._id}
        self._name=student._db.student.find_one(self._condition)['name']
        self._sex=student._db.student.find_one(self._condition)['sex']
        self._birth = student._db.student.find_one(self._condition)['birthday']
        Student._number +=1
    def get_photo(self):
        photoname=student._db.student.find_one(self._condition)['photoname']
        self._photo = os.path.join(self._photoback, os.path.basename(photoname))
        data = student._db.student.find_one(self._condition)
        with open(self._photo, 'wb') as g:
            g.write(data['photo'])
    def set_photo(self,newphoto):
        if not isinstance(newphoto,str):
            raise TypeError('newphoto')
        with open(newphoto, 'rb') as p:
            content = bson.binary.Binary(p.read())
            student._db.student.update_one(self._condition,{'$set':{'photo':content}})
            student._db.student.update_one(self._condition, {'$set': {'photoname': p.name}})
    def num(self):
        self._num = student._db.student.find_one(self._condition)['num']
        return self._num
    def name(self):
        return self._name
    def sex(self):
        return self._sex
    def birthday(self):
        return self._birth
    def age(self):
        return (datetime.date.today().year-self._birth.year)
    def email(self):
        self._email = student._db.student.find_one(self._condition)['email']
        return self._email
    def getCourse(self):
        #count=student._db.course.count_documents({'student':{'$student'!=[]}})
        self._course=[]
        for result in student._db.course.find():
            if self._name in result['student']:
                self._course.append(result['name'])



            #student._db.course.find_one({"student":{$in:self._name}}).skip(i)['name'
        return self._course
    def schoolyear(self):
        self._schoolyear = student._db.student.find_one(self._condition)['schoolyear']
        return self._schoolyear
    def group(self):
        self._group = student._db.student.find_one(self._condition)['group']
        return self._group
    def set_email(self, email_name):
        if not re.match(r"^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$",
                            email_name):
            raise TypeError('Wrong type for the new email!')
        if student._db.student.update_one(self._condition, {'$set': {'email': email_name}}):
            return True
    # def add_course(self,**course_name):
    #     self._course = student._db.student.find_one(self._condition)['course']
    #     newcourse=self._course.extend(list(course_name))
    #     newcourse1=list(set(newcourse))
    #     student._db.student.update_one(self._condition,{'$set':{'course':newcourse1}})
    #     return True
    # def delete_course(self,**course_name):
    #     self._course = student._db.student.find_one(self._condition)['course']
    #     if len(list(course_name))==1:
    #         newcourse=self._course.remove(list(course_name)[0])
    #         student._db.student.update_one(self._condition, {'$set': {'course': newcourse}})
    #     else:
    #         course1=self._course
    #         for i in range(0,len(course1)-1):
    #             for j in range(0,len(list(course_name))):
    #                 if course1[i]==list(course_name)[j]:
    #                     del course1[i]
    #         student._db.student.update_one(self._condition, {'$set': {'course': course1}})
    def account(self,username,password,wechatnum=''):
        if not (isinstance(username,str) and isinstance(password,str) and isinstance(wechatnum,str)):
            raise  ValueError(username,password,wechatnum)
        student._db.account.insert_one({'username':username,'wechatnum':wechatnum,'password':password,'num':self._num})
    @classmethod
    def student_number(cls):
        return Student._number

