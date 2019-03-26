# Database
# Based on MongoDB
#1.user:用户基本信息集合
#文档：用户学号（工号），昵称，头像名称，头像数据

#2.topic:主题集合
#文档:标题，内容，时间，作者工号

#3.reply:回复主题集合
#文档：内容，时间,作者工号
#在hostname=localhost,port=27014,database=myclass条件下可直接运行

#Forumuser:
#	Forumuser(self,str id,str nickname,photo)					#传入用户学号，工号，昵称，照片地址
#	set_nickname(self,str nickname)							#设置用户昵称
#	num(self)									#取得用户学号，工号
#	nickname(self)									#取得用户昵称
#	photo(self)									#取得用户头像
	
#Forumtopic:	
#	Forumtopic(self,str title,str topic,str num,str topicback)			#传入发帖标题，帖子内容地址，作者工号，返回帖子保存地址
#	title(self)									#取得帖子标题
#	topic(self)									#取得帖子内容地址
#	authername(self)								#取得发帖作者昵称
#	authernum(self)									#取得发帖作者工号
#	time(self)									#取得帖子存入数据库的时间
 #Forumreply:
#	Forumreply(self,str reply,str num,str replyback)				#传入回复者内容地址，作者工号，返回保存内容地址
#	content(self)
#	authernum(self)
#	authername(self)
#	time(self)
