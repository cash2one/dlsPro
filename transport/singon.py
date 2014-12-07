#-*- encoding=utf-8 -*-  

class Singleton(object):  
    # def __new__(cls, *args, **kw):  
    #     if not hasattr(cls, '_instance'):  
    #         orig = super(Singleton, cls)  
    #         cls._instance = orig.__new__(cls, *args, **kw)  
    #     return cls._instance  
  loginUserList = []
# class identifyClass(Singleton):  
#     identifydict = {}
#获取当前ip并查询详细地址
		
# import urllib2  
# ip = urllib2.urlopen('http://www.coding123.net/getip.ashx?js=1').read() 
# print "my ip is"+ip[9:-2]
# ip = ip[9:-2]
# info = urllib2.urlopen('http://api.map.baidu.com/location/ip?ak=9K0lcP3ClGLagY9coxmoyKz8&ip='+ip+'&coor=bd09ll').read() 
# print info

from django.core.paginator import Paginator
class JuncheePaginator(Paginator):
	def __init__(self, object_list, per_page, range_num=5, orphans=0, allow_empty_first_page=True):
		Paginator.__init__(self, object_list, per_page, orphans, allow_empty_first_page)
		self.range_num = range_num
  
	def page(self, number):
		self.page_num = number
		return super(JuncheePaginator, self).page(number)
 
	def _page_range_ext(self):
		num_count = 2 * self.range_num + 1
		if self.num_pages <= num_count:
			return range(1, self.num_pages + 1)
		num_list = []
		num_list.append(self.page_num)
		for i in range(1, self.range_num + 1):
			if self.page_num - i <= 0:
				num_list.append(num_count + self.page_num - i)
			else:
				num_list.append(self.page_num - i)
 
			if self.page_num + i <= self.num_pages:
				num_list.append(self.page_num + i)
			else:
				num_list.append(self.page_num + i - num_count)
		num_list.sort()
		return num_list
		page_range_ext = property(_page_range_ext)

#将原生sql查询出的tuple类型转化为dict类型
def dictfetchall(cursor):
    #"将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return list(
    dict(zip([col[0] for col in desc], row))
    for row in cursor.fetchall()
    )

#将原生sql查询出的tuple类型转化为dict类型
def sf_fetchall(cursor):#将每一条记录转化成一个数组
	t = cursor.fetchall()
	i = list(list(r for r in row[1:]) for row in t)
	l = []
	j = []
	k = []
	w = []
	for row in t:
		l.append(row[0])
		j.append(row[1])
		w.append(row[2])
	k.append(l)
	k.append(j)
	k.append(w)
	k.append(i)
	return k
    

#将原生sql查询出的tuple类型转化为dict类型
def sj_fetchall(cursor):#将每一条记录转化成一个数组
	l = []
	j = []
	k = []
	for row in cursor.fetchall():
		l.append(row[0])
		j.append(row[1])
	k.append(l)
	k.append(j)
	return k

#将原生sql查询出的tuple类型转化为dict类型
def use_fetchall(cursor):#将每一条记录转化成一个数组
	l = []
	j = []
	k = []
	w = []
	for row in cursor.fetchall():
		l.append(row[0])
		j.append(row[1])
		w.append(row[2])
	k.append(l)
	k.append(j)
	k.append(w)
	return k

#转换成js能解析的数组
def transportArray(datastring):#将每一条记录转化成一个数组
	d = []
	k = []
	for i in datastring:
		j = []
		for t in i:
			j.append(t)
		d.append(j)
	k.append(d)
	return k

#pdf插入占位符函数
def insertTTTTT(i,s):
	str1 = s
	n = 0
	while(len(str1)>n+i):
		str1 = str1[0:n+i]+"ttttt"+str1[n+i:]
		n=n+5+i
	return str1