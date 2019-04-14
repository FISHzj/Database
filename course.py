from connectmdb import *
from bson.objectid import ObjectId
import bson.binary
import os
course=Connectmdb()
class Course:
    _num=0
    _courseware_num=0
    def __init__(self,name,description,course_type,courseware,courseware_back,schoolyear,student,teacher):
        if not isinstance(name,str) and isinstance(description,str) and course_type in('大','小'):
            raise TypeError('name','description','course_type')
        if not isinstance(courseware,str) and isinstance(courseware_back,str):
            raise TypeError('courseware','courseware_back')
        if not isinstance(schoolyear,str) and isinstance(student,list) and isinstance(teacher,str):
            raise TypeError('schoolyear','student','teacher')
        with open(courseware, 'rb') as f:
            content = bson.binary.Binary(f.read())
            course._db.course.insert_one({'name': name, 'description': description, 'course_type': course_type, 'courseware0_name':f.name,'courseware0': content
                                          ,'schoolyear':schoolyear,'student':student,'teacher':teacher})
            Course._courseware_num+=1
        self._courseware_back = courseware_back
        self._id = ObjectId(course._db.course.find_one({'name': name,'description':description})['_id'])
        self._condition = {'_id': self._id}
    def get_courseware(self,courseware_num):#输入查找的课件序号
        if not isinstance(courseware_num,int):
            raise TypeError('coursware is not integer!')
        courseware='courseware'+str(courseware_num) #文件内容名=courseware+数字
        data = course._db.course.find_one(self._condition)
        filename=course._db.course.find_one(self._condition)[courseware+'_name']#文件名=courseware+数字+_name
        self._courseware = os.path.join(self._courseware_back, os.path.basename(filename))
        with open(self._courseware, 'wb') as g:
            g.write(data[courseware])
     # 取得课程名称
    def name(self):
        self._name = course._db.course.find_one(self._condition)['name']
        return self._name
      # 设置课程描述
    def set_description(self,new_description):
        if not isinstance(new_description,str):
            raise TypeError('new_description!')
        course._db.course.update_one(self._condition, {'$set': {'description': new_description}})
     # 取得课程描述
    def description(self):
        self._description = course._db.course.find_one(self._condition)['description']
        return self._description
    # 取得课程类型（大小班）
    def course_type(self):
        self._course_type = course._db.course.find_one(self._condition)['course_type']
        return self._course_type
     # 设置课程类型
    def set_course_type(self,new_type):
        if not new_type in ('男','女'):
            raise TypeError('new_type!')
        course._db.course.update_one(self._condition, {'$set': {'course_type': new_type}})
     # 取得课程学生列表
    def student(self):
        self._student = course._db.course.find_one(self._condition)['student']
        return self._student
    # 取得授课教师
    def course_teacher(self):
        self._teacher = course._db.course.find_one(self._condition)['teacher']
        return self._teacher
    # 删除学生
    def delete_student(self,**student_name):
        self._student = course._db.course.find_one(self._condition)['student']
        if len(list(student_name)) == 1:
            newstudent = self._student.remove(list(student_name)[0])
            course._db.course.update_one(self._condition, {'$set': {'student': newstudent}})
        else:#删除学生
            student1 = self._student
            for i in range(0, len(student1) - 1):
                for j in range(0, len(list(student_name))):
                    if student1[i] == list(student_name)[j]:
                        del student1[i]
            course._db.course.update_one(self._condition, {'$set': {'student': student1}})
     # 增加学生
    def add_student(self,**student_name):
        newstudent = self._student.extend(list(student_name))
        newstudent1 = list(set(newstudent))#删除重复学生
        course._db.course.update_one(self._condition, {'$set': {'student': newstudent1}})
        return True
      # 取得课程学年
    def course_schoolyear(self):
        self._schoolyear = course._db.course.find_one(self._condition)['schoolyear']
        return self._schoolyear
     # 插入新的课件内容
    def add_courseware(self,new_courseware):
        if not isinstance(new_courseware, str):
            raise TypeError('new_courseware')
        with open(new_courseware, 'rb') as p:
            a='courseware'+str(Course._courseware_num)
            filename=a+'_name'
            content = bson.binary.Binary(p.read())
            course._db.course.update_one(self._condition, {'$set': {a: content}})
            course._db.course.update_one(self._condition, {'$set': {filename: p.name}})
            Course._courseware_num+=1
    @classmethod
    #返回所有课程数量
    def course_num(cls):
        return Course._num







