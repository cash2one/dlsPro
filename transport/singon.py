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