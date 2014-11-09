# coding=utf-8
from django.db import connection,transaction
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from transport.models import field_effect,foundation_status,building_usage,sys_user,identify_result,building_information,EQInfo,building_structure,region,SubLocationCatalog,sublocal,buildlocation
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.db.models import Q
from singon import *
import time
from models import *
from storage import * 
from django.core.mail import send_mail
# Create your views here.

def register_info1(request):
	context = RequestContext(request)
	context_dict = {}
	Storage.userid=request.POST.get('userid')
	Storage.username=request.POST.get('username')
	Storage.password=request.POST.get('password')
	return render_to_response('transport/register1.html',context_dict,context)


def register_info2(request):
	context = RequestContext(request)
	p=sys_user()
	p.user_id=Storage.userid
	p.user_name=Storage.username
	p.user_password=Storage.password
	p.user_realname=request.POST.get('realname')
	p.user_workunit=request.POST.get('depart')
	p.user_idcard=request.POST.get('idnum')
	p.user_major=request.POST.get('major')
	p.user_title=request.POST.get('title')
	p.user_address=request.POST.get('address')
	p.user_postcode=request.POST.get('zipcode')
	p.user_email=request.POST.get('bemail')
	p.user_tel=request.POST.get('phnum')
	p.user_state='未激活'
	p.save()
	title='激活账号'
	massage='请点击该链接激活账户  http://localhost:8000/t/register_activate1'
	sender='caocuiling0927@163.com'
	mail_list=[request.POST.get('bemail')]
	print mail_list
	send_mail(
		title,
		massage,
		sender,
		mail_list,
		fail_silently=True,  
		)
	return render_to_response('transport/register2.html',{'email':p.user_email,'href':'http://mail.'+p.user_email.split('@')[1]},context)

def activate1(request):
	context = RequestContext(request)
	return render_to_response('transport/register3.html',context)

def activate2(request):
	context = RequestContext(request)
	p=sys_user.objects.filter(user_id=request.POST.get('userid'))
	p.user_state='已激活'
	return render_to_response('transport/register4.html',context)

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
		context_dict["uname"] = user
		context_dict["upass"] = password
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
	identify_result = identifyClass()

	if request.method == "GET":
		value = request.GET.get("value")
		zhi = request.GET.get("zhi")
		if value == None or value == "":
			try:
				context_dict["EQid"] = identify_result.identifydict["EQid"]
				EQ_obj = EQInfo.objects.filter(eq_earthquakeid = context_dict["EQid"])
				context_dict["obj"] = EQ_obj[0]
				context_dict["item"] = EQ_obj[0]
			except:
				EQ_obj = EQInfo.objects.all()
		else:
			if zhi == None or zhi == "":
				EQ_obj = EQInfo.objects.all()
				print "*"*60
			else:
				value_new = value + '__icontains'
				args = {value_new:zhi}
				print args
				EQ_obj = EQInfo.objects.filter(**args)
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
				print "#"*60
				context_dict["zhi"] = zhi
				context_dict["sele"] = value
		p = Paginator(EQ_obj,1)
		page_num  = request.GET.get("page",1)
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
		return render_to_response('transport/checkup.html',context_dict,context)
	else:
		value = request.POST.get("infolist")
		identify_result = identifyClass()
		identify_result.identifydict["EQid"] = value
		print "Eqid is ",identify_result.identifydict["EQid"]
		print "##"*60
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
	identify_result = identifyClass()
	structObj = building_structure.objects.all()
	context_dict["structObj"] = structObj
	if request.method == "GET":
		print "enter checkup2 get"
		try:
			print identify_result.identifydict["structtype"]
			context_dict["structtype"] = identify_result.identifydict["structtype"]
			print "$"*60,context_dict["structtype"]
			return render_to_response('transport/checkup2.html',context_dict,context)
		except:
			print "no structtype value"
		return render_to_response('transport/checkup2.html',context_dict,context)
	else:
		print "enter checkup2 post"
		note = request.POST.get("note")
		print note,"#"*60

		try:
			print "eqid is ",identify_result.identifydict["EQid"],"type is ",note
		except:
			return HttpResponseRedirect('/t/checkup')
		identify_result.identifydict["structtype"] = note
		return HttpResponseRedirect('/t/checkup3')


def checkup3(request):
	context = RequestContext(request)
	context_dict = {}
	identify_result = identifyClass()
	useageObj = building_usage.objects.all()
	context_dict["useageObj"] = useageObj
	context_dict["useageObjji"] = useageObj[::2]
	regionObj = region.objects.all()
	context_dict["regionObj"] = regionObj
	if request.method == "GET":
		print "enter checkup3 get"
		try:
			print identify_result.identifydict["building_information"]
			context_dict["building_information"] = identify_result.identifydict["building_information"]
			# print "look yi xia",context_dict["building_buildnumber"]
			print identify_result.identifydict["building_information"]["building_areanumber"]
			return render_to_response('transport/checkup3.html',context_dict,context)
		except:
			print "no building_information value"
			date = time.strftime('%Y%m%d',time.localtime(time.time()))
			building_information={}
			building_information["building_buildnumber"] = "JZW"+date+"12655"
			context_dict["building_information"] = building_information
		return render_to_response('transport/checkup3.html',context_dict,context)
	else:
		try:
			print "eqid is ",identify_result.identifydict["EQid"],"type is ",identify_result.identifydict["structtype"]
			builddict = {}
			builddict["building_buildnumber"] = request.POST.get("build_id")#建筑物id
			builddict["building_number"] = request.POST.get("build_num")#建筑物栋数
			builddict["building_buildyear"] = request.POST.get("build_year")#建筑物建成年份
			builddict["building_buildname"] = request.POST.get("build_name")#建筑物名称
			builddict["building_househostname"] = request.POST.get("build_hostname")#建筑物房主姓名
			builddict["building_buildarea"] = request.POST.get("build_area")#建筑物建筑面积
			builddict["building_uplayernum"] = request.POST.get("build_uplayernum")#建筑物主题层数(上)
			builddict["building_downlayernum"] = request.POST.get("build_downlayernum")#建筑物主题层数(下)
			builddict["building_partlayernum"] = request.POST.get("build_partlayernum")#建筑物局部层数
			builddict["building_buildusage"] = request.POST.get("build_use")#建筑物用途

			builddict["building_longitude"] = request.POST.get("build_longitude")#建筑物中心经度
			builddict["building_latitude"] = request.POST.get("build_latitude")#建筑物中心纬度

			builddict["building_province"] = request.POST.get("build_province")#建筑物所在省份
			builddict["building_city"] = request.POST.get("build_city")#建筑物所在城市
			builddict["building_district"] = request.POST.get("build_district")#建筑物所在县区
			builddict["xiangxi"] = request.POST.get("xiangxidiqu")#详细地区
			builddict["building_admregioncode"] = request.POST.get("build_admregioncode")#建筑物所在行政区编号
			builddict["building_areanumber"] = request.POST.get("build_areanumber")#建筑物所在地区
			#有了抗震设防才有抗震烈度
			builddict["building_fortificationinfo"] = request.POST.get("level")#建筑物抗震设防情况
			#先判断level值
			if builddict["building_fortificationinfo"] =="1":
				builddict["building_fortificationdegree"] = "";
			else:
				builddict["building_fortificationdegree"] = request.POST.get("yl")#建筑物抗震设防中心烈度
			identify_result.identifydict["building_information"] = builddict
		except:
			print "no value"
		print request.POST.get("build_areanumber"),"#"*60
		return HttpResponseRedirect('/t/checkup4')


def checkup4(request):
	context = RequestContext(request)
	context_dict = {}
	identify_result = identifyClass()
	context_dict["foundation_status"] = foundation_status.objects.all()
	context_dict["field_effect"] = field_effect.objects.all()
	field_effect

	if request.method == "GET":
		print "enter checkup4 GET"
		try:
			context_dict["building_environment"] = identify_result.identifydict["building_environment"]
			print "$$$"*60
			print context_dict["building_environment"]["environment_adjoinbuild"]
		except: print "no environment value!"
		return render_to_response('transport/checkup4.html',context_dict,context)
	else:
		print "enter checkup4 POST"
		environment = {}
		environment["environment_earthquakeeff"] = request.POST.getlist("cdyx")
		environment["environment_foundation"] = request.POST.getlist("djzk")
		environment["environment_adjoinbuild"] = request.POST.getlist("pljz")
		environment["environment_seismicintensity"] = request.POST.get("ph")
		environment["environment_smallaffect"] = request.POST.get("ps")
		environment["environment_bigaffect"] = request.POST.get("pb")
		identify_result.identifydict["building_environment"] = environment
		# print "this is checkup4 the cdyx is ",cdyx[:],"   and  the djzk is  ",djzk," and the fzld is ",fzld,"  and the ps is ",xz,"and zhe dz is ",dz
		return HttpResponseRedirect('/t/checkup5')
def checkup5(request):
	context = RequestContext(request)
	context_dict = {}
	identify_result = identifyClass()
	if request.method == "GET":
		print "enter checkup5 GET"
		try:
			structtype = identify_result.identifydict["structtype"]
			print structtype,"i am structtype"
		except:
			return  HttpResponseRedirect('/t/checkup2')#若没有类型值则返回选择类型界面
		try:
			sublocalObj = sublocal.objects.filter(sublocal_constructtypeid = structtype)#查询出所有的细部震损信息
			locationObj = buildlocation.objects.filter(location_constructtype = structtype)#查询出所有部位信息
			catalogObj = SubLocationCatalog.objects.filter()#查询出所有的细部分类信息
			print sublocalObj
		except:
			print "no value sublocalObj"
		context_dict["sublocalObj"] = sublocalObj
		context_dict["locationObj"] = locationObj
		context_dict["catalogObj"] = catalogObj
		context_dict["struct"] = sublocalObj[0].sublocal_constructtypeid
		# print sublocalObj[0].sublocal_name,"$"*60
		# print context_dict["sublocalObj"][0].sublocal_constructtypeid,"$"*60
		return render_to_response('transport/checkup5.html',context_dict,context)
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



