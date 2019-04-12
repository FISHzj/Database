import datetime
from bson.objectid import ObjectId
import re
import bson.binary
from connectmdb import *
import os
student=Connectmdb() #实例化对象连接数据库,localhost:27014,database=myclass
class Student:  
    _number=0#所有学生数量
    def __init__(self,name,sex,birthday,ident,email,photo='',photoback='',course=[],schoolyear=0,group=0):  #传入姓名，性别，学号，邮箱，照片，返回照片地址，课程列表，学年
        if not (isinstance(name,str) and sex in ("男","女") and isinstance(ident,str) and isinstance(photo,str) and isinstance(photoback,str)):#判断姓名，性别，照片地址是否为字符串
            raise ValueError(name,sex,ident,photo,photoback) #引发异常
        if not (isinstance(course,list) and isinstance(schoolyear,int) and isinstance(group,int)):#判断课程是否为列表，学年为int类型
            raise  ValueError(course,schoolyear,group)
        try:
            birth=datetime.datetime(*birthday)#生日为元组格式
        except:
            raise ValueError("Wrong date",birthday)
        if isinstance(email,str):#判断邮箱是否合法
            if not re.match(r"^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$",email):
                raise TypeError('Wrong type for the email!')
        if not photo.endswith(('.pdf', '.jpeg', '.jpg', '.png', '.bmp')):#判断照片格式
            raise TypeError('topic')
        with open(photo, 'rb') as f:#打开照片
            content = bson.binary.Binary(f.read())
            student._db.student.insert_one({'name':name,'sex':sex,'birthday':birth,'num':ident,'email':email,'photo':content,
                                            'course':course,'schoolyear':schoolyear,'group':group})#向数据库指定集合“student”写入数据
        self._photo = os.path.join(photoback, os.path.basename(f.name))
        self._photoback=photoback
        self._id=ObjectId(student._db.student.find_one({'num':ident})['_id'])
        self._condition={'_id':self._id}
        self._name=student._db.student.find_one(self._condition)['name']
        self._sex=student._db.student.find_one(self._condition)['sex']
        self._birth=student._db.student.find_one(self._condition)['birthday']
        self._num=student._db.student.find_one(self._condition)['num']
        self._email=student._db.student.find_one(self._condition)['email']
        self._course=student._db.student.find_one(self._condition)['course']
        self._schoolyear=student._db.student.find_one(self._condition)['schoolyear']
        self._group=student._db.student.find_one(self._condition)['group']
        Student._number +=1
    def get_photo(self):#获取照片写入指定地址
        data = student._db.student.find_one(self._condition)
        with open(self._photo, 'wb') as g:
            g.write(data['photo'])
        return self._photo
    def set_photo(self,newphoto):#设置照片
        if not isinstance(newphoto,str):
            raise TypeError('newphoto')
        with open(newphoto, 'rb') as p:
            content = bson.binary.Binary(p.read())
            student._db.student.update_one(self._condition,{'$set':{'photo':content}})
            self._photo = os.path.join(self._photoback, os.path.basename(p.name))
    def num(self):
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
        return self._email
    def course(self):
        return self._course
    def schoolyear(self):
        return self._schoolyear
    def group(self):
        return self._group
    def set_email(self, email_name):
        if not re.match(r"^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$",
                            email_name):
            raise TypeError('Wrong type for the new email!')
        if student._db.student.update_one(self._condition, {'$set': {'email': email_name}}):
            return True
    def add_course(self,**course_name):
        newcourse=self._course.extend(list(course_name))
        newcourse1=list(set(newcourse))
        student._db.student.update_one(self._condition,{'$set':{'course':newcourse1}})
        return True
    def delete_course(self,**course_name):
        if len(list(course_name))==1:
            newcourse=self._course.remove(list(course_name)[0])
            student._db.student.update_one(self._condition, {'$set': {'course': newcourse}})
        else:
            course1=self._course
            for i in range(0,len(course1)-1):
                for j in range(0,len(list(course_name))):
                    if course1[i]==list(course_name)[j]:
                        del course1[i]
            student._db.student.update_one(self._condition, {'$set': {'course': course1}})
    def account(self,username,password,wechatnum=''):#创建account集合，插入数据
        if not (isinstance(username,str) and isinstance(password,str) and isinstance(wechatnum,str)):
            raise  ValueError(username,password,wechatnum)
        student._db.account.insert_one({'username':username,'wechatnum':wechatnum,'password':password,'num':self._num})
    @classmethod
    def student_number(cls):
        return Student._number

