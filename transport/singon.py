#-*- encoding=utf-8 -*-  
import urllib2
import httplib
import json
from  datetime  import  *
from xlwt import *
import StringIO
import re
from django.http import HttpResponse
from django.utils.encoding import *
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
		
#   
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

def postdata(data1):
	try:
		url='http://localhost:8001/d/'
		values ={"data":data1}

		jdata = json.dumps(values)             # 对数据进行JSON格式化编码
		req = urllib2.Request(url, jdata)       # 生成页面请求的完整数据
		response = urllib2.urlopen(req)       # 发送页面请求
		return response.read()                    # 获取服务器返回的页面信息
	except Exception,e:
		print "error",e
		return 0
	return 0

def countExportEls(request,dataObj):
	try:
		w = Workbook(encoding='utf-8')
		ws= w.add_sheet('Hey, Dude')
		style  =  XFStyle()#栏目标题
		style1 = XFStyle()#内容
		style2  =  XFStyle()#上标题
		font2 =  Font()#上标题
		font2.bold = True
		align = Alignment()
		align.horz = align.HORZ_CENTER
		font2.height = 0x00FF
		style2.font = font2
		style2.alignment = align
		font =  Font()
		align = Alignment()
		align.horz = align.HORZ_CENTER
		font.bold = True
		style1.alignment = align
		style.alignment = align
		style.font = font
		for t in range(0,22):
			ws.col(t).width = 4000
		ws.col(0).width = 1500
		ws.col(1).width = 8500
		ws.col(3).width = 5000
		ws.col(4).width = 4000
		ws.col(5).width = 4000
		ws.col(6).width = 6000
		ws.col(8).width = 6000

		ws.write_merge(0,1, 0, 23, "地震现场建筑物安全鉴定结果统计——%s" % date.today(), style2)
		colnum = 1
		ws.write(2,colnum-1,"编号",style)
		ws.write(2,colnum+0,"建筑物编号",style)
		ws.write(2,colnum+1,"鉴定结论",style)
		ws.write(2,colnum+2,"震损指数",style)
		ws.write(2,colnum+3,"行政区编码",style)
		ws.write(2,colnum+4,"建筑物名称",style)
		ws.write(2,colnum+5,"建筑物地点",style)
		ws.write(2,colnum+6,"房主",style)
		ws.write(2,colnum+7,"建筑结构",style)
		ws.write(2,colnum+8,"建成年份",style)
		ws.write(2,colnum+9,"抗震设防状况",style)
		ws.write(2,colnum+10,"抗震设防烈度",style)
		ws.write(2,colnum+11,"即发地震烈度",style)
		ws.write(2,colnum+12,"鉴定日期",style)
		ws.write(2,colnum+13,"中心经度",style)
		ws.write(2,colnum+14,"中心纬度",style)
		ws.write(2,colnum+15,"建筑面积",style)
		ws.write(2,colnum+16,"主体层数",style)
		ws.write(2,colnum+17,"建筑物用途",style)
		ws.write(2,colnum+18,"鉴定人员编号",style)
		ws.write(2,colnum+19,"鉴定人",style)
		ws.write(2,colnum+20,"鉴定人员职称",style)
		ws.write(2,colnum+21,"鉴定单位",style)
		ws.write(2,colnum+22,"破坏等级",style)
		i = 2
		for item in dataObj:
			j = -1
			ws.write(i+1,j+1,str(i-1),style1)
			for ite in item:
				ws.write(i+1,j+2,ite,style1)
				j = j+1
			i = i+1
		xlsNameDay = str(date.today())
		fname = '统计数据%s.xls' %date.today()
		agent=request.META.get('HTTP_USER_AGENT') 
		if agent and re.search('MSIE',agent):
			response =HttpResponse(content_type="application/vnd.ms-excel") #解决ie不能下载的问题
			response['Content-Disposition'] ='attachment; filename=%s' % urlquote(fname) #解决文件名乱码/不显示的问题
		else:
			response =HttpResponse(content_type="application/ms-excel")#解决ie不能下载的问题
			response['Content-Disposition'] ='attachment; filename=%s' % smart_str(fname) #解决文件名乱码/不显示的问题
		##########################################保存
		w.save(response)
		return response

		# w.save('c:/xls/鉴定结构统计%sDay.xls' % xlsNameDay)
	except Exception,e:
		print "Exception:",e