# coding=utf-8
from django.db import connection,transaction
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from transport.models import sys_user,identify_result,building_information,EQInfo
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.db.models import Q
from singon import *
import time
# Create your views here.

def islogined(request):
	username = request.session.get("username")
	print "被调用"
	if username:
		return 'true'
	else:
		return 'false'

def user_query(request):
	context = RequestContext(request)
	context_dict = {}
	client_obj = sys_user.objects.filter(user_name = request.session.get('username'))
	print "jin ru han shu le "
	if client_obj:
		context_dict['username'] = client_obj[0].user_name
		context_dict['userrealname'] = client_obj[0].user_realname
		context_dict['userid'] = client_obj[0].id
		context_dict['useridcard'] = client_obj[0].user_idcard
		context_dict['title'] = client_obj[0].user_title
		context_dict['danwei'] = client_obj[0].user_workunit
		context_dict['password'] = client_obj[0].user_password
		context_dict['profession'] = client_obj[0].user_major
		context_dict['address'] = client_obj[0].user_address
		context_dict['telnum'] = client_obj[0].user_tel
		context_dict['email'] = client_obj[0].user_email
		context_dict['zipcode'] = client_obj[0].user_postcode
		return context_dict
	else:
		return None

		
def login(request):
	context = RequestContext(request)
	context_dict = {}

	return render_to_response('transport/login.html',context_dict,context)

def register(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('transport/register.html',context_dict,context)


def exit(request):
	context = RequestContext(request)
	context_dict = {}
	request.session.clear()
	return render_to_response('transport/login.html',context_dict,context)


def ditu(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('transport/dls_pro.html',context_dict,context)

def login_va(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method == 'POST':
		user = request.POST.get("uname")
		password = request.POST.get("upass")
		client_obj = sys_user.objects.filter(user_name = user)
		if client_obj:
			client_obj = sys_user.objects.filter(user_name = user,user_password = password)
			if client_obj:
				print '登陆成功'
				request.session['realname'] = client_obj[0].user_realname
				request.session['username'] = user
				print client_obj
				if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
					ip =  request.META['HTTP_X_FORWARDED_FOR']  
				else:  
					ip = request.META['REMOTE_ADDR']  
				print "######################################"
				print ip
				return HttpResponseRedirect('/t/index')
			else:
				print 'password error'
				context_dict['error'] = '用户密码不匹配'
				return render_to_response('transport/login.html',context_dict,context)
		else:
			print 'login failed'
			context_dict['error'] = '用户不存在！'
			return render_to_response('transport/login.html',context_dict,context)

	return render_to_response('transport/login.html',context_dict,context)

def index(request):
	context = RequestContext(request)
	context_dict = user_query(request)
	return render_to_response('transport/index.html',context_dict,context)



def checkup(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method == "GET":
		value = request.GET.get("value")
		zhi = request.GET.get("zhi")
		if zhi == None or zhi == "":
			EQ_obj = EQInfo.objects.all()
			print "*"*60
		else:
			value_new = value + '__icontains'
			args = {value_new:zhi}
			print args
			# EQ_obj = EQInfo.objects.filter(**dict_data)
			EQ_obj = EQInfo.objects.filter(**args)
			print "#"*60
		p = Paginator(EQ_obj,5)
		page_num  = request.GET.get("page",1)
		context_dict["zhi"] = zhi
		context_dict["sele"] = value
		if value =="eq_earthquakeid":
			context_dict["selector"] = "地震编号"
		elif value == "eq_earthquakename":
			context_dict["selector"] = "地震名称"
		elif value == "eq_magnitude":
			context_dict["selector"] = "地震震级"	
		elif value == "eq_epicentralintensity":
			context_dict["selector"] = "震中烈度"	
		elif value == "eq_focaldepth":
			context_dict["selector"] = "震源深度"	
		try:
			item = p.page(page_num)
		except PageNotAnInteger:
			item = p.page(1)
		except EmptyPage:
			item = p.page(p.num_pages)
		context_dict["item"] = item
		try:
			context_dict["obj"] = item[0]
		except:
			context_dict["nodata"] = "true"
		identify_result = identifyClass()
		try:
			context_dict["EQid"] = identify_result.identifydict["EQid"]
			EQ_obj = EQInfo.objects.filter(eq_earthquakeid = context_dict["EQid"])
			context_dict["obj"] = EQ_obj[0]
		except:
			print "no id value"
		return render_to_response('transport/checkup.html',context_dict,context)
	else:
		value = request.POST.get("infolist")
		identify_result = identifyClass()
		identify_result.identifydict["EQid"] = value
		print "Eqid is ",identify_result.identifydict["EQid"]
		return HttpResponseRedirect('/t/checkup2')

def check_eq(request):
	context_dict = {}
	print "jin ru check_eq function "
	eq_id = request.GET.get("eq_id")
	print eq_id
	EQ_obj = EQInfo.objects.get(eq_earthquakeid = eq_id)
	print "jin ru check_eq function "
	str1 = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (EQ_obj.eq_earthquakeid,EQ_obj.eq_earthquakename,EQ_obj.eq_date,EQ_obj.eq_time,EQ_obj.eq_focaldepth,EQ_obj.eq_magnitude,EQ_obj.eq_focallongitude,EQ_obj.eq_focallatitude,EQ_obj.eq_epicentralintensity,EQ_obj.eq_remark,EQ_obj.eq_remark)

	print EQ_obj
	return HttpResponse(str1)
	

def checkup2(request):
	context = RequestContext(request)
	context_dict = {}

	if request.method == "GET":
		print "enter checkup2 get"
		return render_to_response('transport/checkup2.html',context_dict,context)
	else:
		print "enter checkup2 post"
		note = request.POST.get("note")
		print note,"#"*60
		identify_result = identifyClass()
		print "eqid is ",identify_result.identifydict["EQid"],"type is ",note
		identify_result.identifydict["structtype"] = note
		return HttpResponseRedirect('/t/checkup3')

def checkup3(request):
	context = RequestContext(request)
	context_dict = {}
	identify_result = identifyClass()
	if request.method == "GET":
		print "enter checkup3 get"
		try:
			print identify_result.identifydict["building_information"]
			context_dict = identify_result.identifydict["building_information"]
			print "look yi xia",context_dict["buildid"]
			return render_to_response('transport/checkup3.html',context_dict,context)
		except:
			print "no building_information value"
			date = time.strftime('%Y%m%d',time.localtime(time.time()))
			context_dict["buildid"] = "JZW"+date+"12655"
		return render_to_response('transport/checkup3.html',context_dict,context)
	else:
		try:
			print "eqid is ",identify_result.identifydict["EQid"],"type is ",identify_result.identifydict["structtype"]
			builddict = {}
			builddict["buildid"] = request.POST.get("build_id")#建筑物id
			builddict["buildnum"] = request.POST.get("build_num")#建筑物栋数
			builddict["buildyear"] = request.POST.get("build_year")#建筑物建成年份
			builddict["buildname"] = request.POST.get("build_name")#建筑物名称
			builddict["buildhostname"] = request.POST.get("build_hostname")#建筑物房主姓名
			builddict["buildarea"] = request.POST.get("build_area")#建筑物建筑面积
			builddict["builduplayernum"] = request.POST.get("build_uplayernum")#建筑物主题层数(上)
			builddict["builddownlayernum"] = request.POST.get("build_downlayernum")#建筑物主题层数(下)
			builddict["buildpartlayernum"] = request.POST.get("build_partlayernum")#建筑物局部层数
			builddict["builduse"] = request.POST.get("build_use")#建筑物用途

			builddict["buildlongitude"] = request.POST.get("build_longitude")#建筑物中心经度
			builddict["buildlatitude"] = request.POST.get("build_latitude")#建筑物中心纬度

			builddict["buildprovince"] = request.POST.get("build_province")#建筑物所在省份
			builddict["buildcity"] = request.POST.get("build_city")#建筑物所在城市
			builddict["builddistrict"] = request.POST.get("build_district")#建筑物所在县区
			builddict["buildadmregioncode"] = request.POST.get("build_admregioncode")#建筑物所在行政区编号
			builddict["buildareanumber"] = request.POST.get("build_areanumber")#建筑物所在行政区编号
			builddict["buildfortificationinfo"] = request.POST.get("level")#建筑物抗震设防情况
			builddict["buildfortificationdegree"] = request.POST.get("yl")#建筑物抗震设防情况
			identify_result.identifydict["building_information"] = builddict
		except:
			print "no value"
		
		return HttpResponseRedirect('/t/checkup4')
def checkup4(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('transport/checkup4.html',context_dict,context)
def checkup5(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('transport/checkup5.html',context_dict,context)
def checkup6(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('transport/checkup6.html',context_dict,context)


#统计页面
def count(request):
	context = RequestContext(request)
	context_dict = {}
	resultObj = identify_result.objects.filter()
	print "*"*50,resultObj
	p = Paginator(resultObj,1)

	page_num  = request.GET.get("page",1)
	try:
		item = p.page(page_num)
	except PageNotAnInteger:
		item = p.page(1)
	except EmptyPage:
		item = p.page(p.num_pages)
	context_dict["item"] = item
	context_dict["is_delete"] = request.GET.get("is_delete")
	return render_to_response('transport/count.html',context_dict,context)


#chu li user
def user(request):
	context = RequestContext(request)
	context_dict = user_query(request)
	return render_to_response('transport/user.html',context_dict,context)

def edituser(request):
	context = RequestContext(request)
	context_dict = user_query(request)
	if request.method == 'POST':
		print request.POST
		print "ti jiao le xiu gai xin xi"
		email = request.POST.get("email")
		userrealname = request.POST.get("userrealname")
		zipcode = request.POST.get("zipcode")
		telnum = request.POST.get("telnum")
		profession = request.POST.get("profession")
		danwei = request.POST.get("danwei")
		title = request.POST.get("title")
		address = request.POST.get("address")
		useridcard = request.POST.get("useridcard")
		client_obj = sys_user.objects.get(user_name=request.session.get("username"))
		if client_obj:
			client_obj.user_realname = userrealname
			client_obj.user_email = email
			client_obj.user_idcard = useridcard
			client_obj.user_postcode = zipcode
			client_obj.user_tel = telnum
			client_obj.user_major = profession
			client_obj.user_workunit = danwei
			client_obj.user_title = title
			client_obj.user_address = address
			client_obj.save()
	return render_to_response('transport/edituser.html',context_dict,context)

def editpass(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method == "POST":
		user_password = request.POST.get("old_password")
		try:
			client_obj = sys_user.objects.get(user_name = request.session.get('username'),user_password = user_password)
		except:
			client_obj = 0
		if client_obj:
			new_user_password = request.POST.get("new_password")
			client_obj.user_password = new_user_password
			client_obj.save()
			context_dict["result"] = "修改成功！"
		elif user_password == "":
			context_dict["result"] = "请输入密码！"
		else:
			context_dict["result"] = "密码错误！"
	return render_to_response('transport/editpass.html',context_dict,context)
	
def propass(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('transport/propass.html',context_dict,context)

def message(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('transport/message.html',context_dict,context)

def build_result_edit(request):
	context = RequestContext(request)
	context_dict = {}
	print "delete function*******************************************"
	print request.GET.get("_id")
	print "delete function*******************************************"
	return HttpResponseRedirect('/t/count')

def delete_build(request):
	context = RequestContext(request)
	context_dict = {}
	print "delete function*******************************************"
	if request.method == 'GET':
		idlist = request.GET.get("id_list")
		identify_result.objects.filter(id__in =idlist).delete()
		context_dict["is_delete"] = "yes"
		return HttpResponseRedirect('/t/count?is_delete=true')
	else:
		return HttpResponseRedirect('/t/count')



def export_xls(request):
	print "******************************************************"
	from pyExcelerator import *
	wb=Workbook()
	print "################################"
	ws=wb.add_sheet('hey')   
	ws.write(0,0,u"姓名")  
	ws.write(0,1,u"年龄")  
	ws.write(0,2,u"班级")  
	response = HttpResponse(wb.savestream(),mimetype='application/vnd.ms-excel')  
	response['Pragma'] = "no-cache"
	response['Expires'] = "0"
	response['Content-Disposition'] = 'attachment; filename=ss.xls' 
	return response  
		#帮助页
def help(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('transport/help.html',context_dict,context)

def helpcontent(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('transport/helpcontent.html',context_dict,context)


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
