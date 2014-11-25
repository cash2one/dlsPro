# coding=utf-8
from django.db import connection,transaction
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from transport.models import *
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.db.models import Q
import simplejson as json
from singon import *
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
import hashlib 
import sys
import cStringIO
from datetime import *
from models import *
from storage import * 
from django.core.mail import send_mail
import simplejson as json
from PIL import Image, ImageDraw, ImageFont
import random
import time
import re
from random import choice
import string
import urllib2


def GenPassword(length=3,chars=string.ascii_letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])

def register_info1(request):
	context = RequestContext(request)
	context_dict = {}
	usercl=request.POST.get('clazz')
	userid=' '
	user=[]
	if(usercl=="1"):
		userid='P'+GenPassword(3)
		user=sys_user.objects.filter(user_id=userid)
		while user:
			userid='P'+GenPassword(3)
			user=sys_user.objects.filter(user_id=userid)
	else:
		userid='Z'+GenPassword(3)
		user=sys_user.objects.filter(user_id=userid)
		while user:
			userid='Z'+GenPassword(3)
			user=sys_user.objects.filter(user_id=userid)

	#Storage.userid=request.POST.get('userid')
	Storage.userid=userid
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
	p.user_createtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	p.user_updatetime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	p.save()
	title='激活账号'
	massage='请点击该链接激活账户  http://localhost:8000/t/register_activate1?id='+p.user_id.encode('utf8')
	sender='caocuiling0927@163.com'
	mail_list=[request.POST.get('bemail')]
	send_mail(
		title,
		massage,
		sender,
		mail_list,
		fail_silently=True,  
		)
	return render_to_response('transport/register2.html',{'email':p.user_email,'href':'http://mail.'+p.user_email.split('@')[1]},context)

'''
#用户Id验证唯一性
def testajax(request):
	context=RequestContext(request)
	context_dict={}
	if request.method=='GET':
		userId=request.GET.get('userid','')
		if not userId:
			context_dict['msg'] = '请输入用户ID'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		if len(userId)!=12:
			context_dict['msg'] ='用户ID是12位'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		user=sys_user.objects.filter(user_id=userId)
		if user:
			context_dict['msg'] ='该ID已经注册，请换一个'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		else:
			context_dict['msg'] = 'sucess'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")

	return HttpResponse(json.dumps(context_dict))
'''
def uniname(request):
	context=RequestContext(request)
	context_dict={}
	if request.method=='GET':
		username=request.GET.get('usname','')
		if not username:
			context_dict['msg'] = '请输入用户名'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		m = re.match(r"^[a-zA-Z_]{1}[0-9a-zA-Z_]{1,}$",username)
		if not m:
			context_dict['msg'] = '用户名必须由字母、数字或\"_\"组成,且首位不能是数字！'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		if len(username)<6:
			context_dict['msg'] ='用户名长度不能小于6！'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		if len(username)>20:
			context_dict['msg'] ='用户名长度不能大于20'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		user=sys_user.objects.filter(user_name=username)
		if user:
			context_dict['msg'] ='该用户名已经被占用，请选择其他！'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		else:
			context_dict['msg'] = 'sucess'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")

def authcode(request):
	context=RequestContext(request)
	context_dict={}
	if request.method=='GET':
		authcode=request.GET.get('imgcode','')
		if not authcode:
			context_dict['msg'] = '请输入验证码'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		if authcode!=request.session['checkcode']:
			context_dict['msg'] = '验证码输入错误'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		else:
			context_dict['msg'] = 'sucess'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")


def get_check_code_image(request,image="static/img/imgcode.jpg"):
	im = Image.open(image)
	draw = ImageDraw.Draw(im)
	mp = hashlib.md5()
	mp_src = mp.update(str(datetime.now()))
	mp_src = mp.hexdigest()
	rand_str = mp_src[0:4]
	draw.text((5,0), rand_str[0], font=ImageFont.truetype("static/file/ARIAL.TTF", random.randrange(15,35)))
	draw.text((20,0), rand_str[1], font=ImageFont.truetype("static/file/ARIAL.TTF", random.randrange(15,35)))
	draw.text((35,0), rand_str[2], font=ImageFont.truetype("static/file/ARIAL.TTF", random.randrange(15,35)))
	draw.text((50,0), rand_str[3], font=ImageFont.truetype("static/file/ARIAL.TTF", random.randrange(15,35)))
	del draw
	request.session['checkcode'] = rand_str
	buf = cStringIO.StringIO()
	im.save(buf,'gif')
	return HttpResponse(buf.getvalue(),'img/gif')

def activate1(request):
	context = RequestContext(request)
	u_id=request.GET.get('id','-1')
	print u_id
	try:
		p=sys_user.objects.get(user_id = u_id)
		print p.user_id 
		p.user_state="已激活"
		p.save()
		print p.user_state
	except:
		print "no user"
	
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
		lastlogintime = client_obj[0].user_lastlogintime
		context_dict["lastlogintime"] = lastlogintime

		loginlastaddress = client_obj[0].user_loginlastaddress
		context_dict["lastloginaddress"] = loginlastaddress

		lastip = client_obj[0].user_lastip
		context_dict["lastip"] = lastip

		logincount = client_obj[0].user_logincount
		context_dict["logincount"] = logincount
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
	client_obj = sys_user.objects.get(user_name = request.session.get("username"))
	client_obj.user_lastalivetime = '1970-01-01 00:00:00'
	client_obj.save()
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
		if len(user)==0:
			context_dict['error'] = '用户名不能为空'
			return render_to_response('transport/login.html',context_dict,context)
		elif len(password)==0:
			context_dict['error'] = '密码不能为空'
			return render_to_response('transport/login.html',context_dict,context)
		client_obj = sys_user.objects.filter(user_name = user)
		if client_obj:
			try:
				client_obj = sys_user.objects.get(user_name = user,user_password = password)
				if client_obj.user_state == "未激活":
					context_dict['error'] = '该用户尚未激活,请激活后再登陆！'
					return render_to_response('transport/login.html',context_dict,context)
				lastalivetime = client_obj.user_lastalivetime
				if lastalivetime:
					print lastalivetime
					lastalivetime = str(lastalivetime)
					print lastalivetime
					time_last = datetime.strptime(lastalivetime,'%Y-%m-%d %H:%M:%S')
					print time_last
					print "ss"
					time_now = datetime.now()
					time_now = str(time_now)[:19]
					print time_now
					time_now = datetime.strptime(time_now,'%Y-%m-%d %H:%M:%S')
					jiange = time_now - time_last
				# 	jiange = time.strftime('%Y-%m-%d %X',time.localtime(time.time())) - lastalivetime
					print jiange.seconds
					if int(jiange.seconds) < 600:
						print "jinlailema"
						waittime = 600-int(jiange.seconds)
						print waittime
						context_dict['error'] = '用户未退出,请在%d秒后重试！'% waittime
						return render_to_response('transport/login.html',context_dict,context)
				print 'login success'
				client_obj.user_lastalivetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
				client_obj.user_lastlogintime = client_obj.user_logintime
				client_obj.user_logintime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
				address = urllib2.urlopen('http://pv.sohu.com/cityjson').read()#获取到ip地址和城市名  
				address = eval(str(address[19:-1]))#得到json字符串  
				print address
				ip = address["cip"]#得到ip 
				dizhi = address["cname"]#得到城市
				if client_obj.user_loginaddress:
					client_obj.user_loginlastaddress = client_obj.user_loginaddress
				client_obj.user_loginaddress = dizhi.decode('GBK')#解码
				if client_obj.user_ip:
					client_obj.user_lastip = client_obj.user_ip
				client_obj.user_ip = ip
				logincount = client_obj.user_logincount
				if logincount:
					logincount = int(logincount)+1
				else:
					logincount = 1
				client_obj.user_logincount = logincount
				client_obj.save()
				request.session['realname'] = client_obj.user_realname
				request.session['username'] = user
				request.session['user_id'] = client_obj.user_id
				request.session['USERID'] = client_obj.id
				
				print request.session
				print "#"*60
				return HttpResponseRedirect('/t/index')
			except:
				print 'password error'
				context_dict['error'] = '用户名密码不匹配'
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
		if value == None or value == "":
			try:
				context_dict["EQid"] = request.session.get("EQid")
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
		p = Paginator(EQ_obj,10)
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
		request.session["EQid"] = value
		eqObj = EQInfo.objects.get(eq_earthquakeid = value)
		request.session["EQID"] = eqObj.id
		print "Eqid is ",request.session.get("EQid")
		print "EQID is ",request.session.get("EQID")
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
	if request.session.get("user_id"):
		print request.session.get("user_id")#用户编号
	else:
		print "no user id "
		return HttpResponseRedirect('/t')
	if request.session.get("EQid"):
		print request.session.get("EQid")#地震编号
	else:
		print "no eq id "
		return HttpResponseRedirect('/t/checkup')
	structObj = building_structure.objects.all()
	context_dict["structObj"] = structObj
	if request.method == "GET":
		print "enter checkup2 get"
		try:
			print request.session.get("structtype")
			context_dict["structtype"] = request.session.get("structtype")
			print "$"*60,context_dict["structtype"]
			return render_to_response('transport/checkup2.html',context_dict,context)
		except:
			print "no structtype value"
		return render_to_response('transport/checkup2.html',context_dict,context)
	else:
		print "enter checkup2 post"
		note = request.POST.get("name")
		print note,"#"*60
		try:
			print "eqid is ",request.session.get("EQid"),"type is ",note
		except:
			return HttpResponse('没有选择地震！即将跳转选择地震页面！')
		request.session["structtype"] = note
		print note,"I am  note "
		try:
			structnameObj = building_structure.objects.get(construct_typeid = note)
			request.session["structtypename"] = structnameObj.construct_typename
			request.session["structtypeid"] = structnameObj.id
			print structnameObj.construct_typename,structnameObj.id
			return HttpResponse("success")
		except:
			return HttpResponse('请选择结构类型!')


def checkup3(request):
	context = RequestContext(request)
	context_dict = {}
	useageObj = building_usage.objects.all()
	context_dict["useageObj"] = useageObj
	context_dict["useageObjji"] = useageObj[::2]
	regionObj = region.objects.all()
	context_dict["regionObj"] = regionObj

	if request.session.get("user_id"):
		userid = request.session.get("user_id")#用户编号
	else:
		print "no user id "
		return HttpResponseRedirect('/t')
	if request.session.get("EQid"):
		earthquakeid = request.session.get("EQid")#地震编号
	else:
		print "no eq id "
		return HttpResponseRedirect('/t/checkup')
	if request.session.get("structtypename"):
		context_dict["structtypename"] = request.session.get("structtypename")#地震编号
	else:
		print "no structname "
		return HttpResponseRedirect('/t/checkup2')
	if request.session.get("structtype"):
		structtype = request.session.get("structtype")#地震编号
	else:
		print "no structtype "
		return HttpResponseRedirect('/t/checkup2')
	if request.method == "GET":
		print "enter checkup3 get"
		try:#测试有无建筑物信息
			# buidObj = building_information_tem.objects.get(building_constructtypeid__construct_typeid = structtype,building_userid__user_id=userid,building_earthquakeid__eq_earthquakeid=earthquakeid)
			buidObj = building_information_tem.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
			print "*"*60
			context_dict["building"] = buidObj
			return render_to_response('transport/checkup3.html',context_dict,context)
		except:
			#没有建筑物信息时，新生成一个建筑物id
			print "no building_information value"
			date1 = time.strftime('%Y%m%d',time.localtime(time.time()))#鉴定日期为当前系统时间的格式化如20141113
			buidatedate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
			#查询当天插入数据库中的建筑物信息条数
			count = building_information.objects.filter(building_constructtypeid__construct_typeid = structtype,building_userid__user_id=userid,building_earthquakeid__eq_earthquakeid=earthquakeid,building_createdate=buidatedate).count()
			count = '%04d' % (count)
			print count,"*"*20
			# building_informations={}#生成一个字典，目的是与有建筑物时相统一
			# building_informations["building_buildnumber"] = structtype+userid+earthquakeid+date1+count
			try:
				buidObj = building_information.objects.order_by('-building_createtime').filter(building_constructtypeid__construct_typeid = structtype,building_userid__user_id=userid,building_earthquakeid__eq_earthquakeid=earthquakeid)[0]
				print "%"*60
				context_dict["building"] = buidObj
			except:
				print "no build_information value in database!"
			context_dict["number"]= structtype+userid+earthquakeid+date1+count
		return render_to_response('transport/checkup3.html',context_dict,context)
	else:
		try:
			print "eqid is ",earthquakeid,"type is ",structtype
			builddict = {}
			builddict["building_buildnumber"] = request.POST.get("build_id")#建筑物id
			request.session["building_buildnumber"] = builddict["building_buildnumber"]#将buildnumber存储到session中，在存储环境信息时使用
			builddict["building_number"] = int(request.POST.get("build_num",0))#建筑物栋数
			builddict["building_buildyear"] = request.POST.get("build_year")#建筑物建成年份
			builddict["building_buildname"] = request.POST.get("build_name")#建筑物名称
			builddict["building_househostname"] = request.POST.get("build_hostname")#建筑物房主姓名
			builddict["building_buildarea"] = request.POST.get("build_area")#建筑物建筑面积
			builddict["building_uplayernum"] = int(request.POST.get("build_uplayernum",1))#建筑物主题层数(上)
			builddict["building_downlayernum"] = int(request.POST.get("build_downlayernum",1))#建筑物主题层数(下)
			builddict["building_partlayernum"] = int(request.POST.get("build_partlayernum",1))#建筑物局部层数
			builddict["building_buildusage"] = request.POST.get("build_use")#建筑物用途
			builddict["building_usageid"] = request.POST.get("build_use")#建筑物用途
			builddict["building_constructtypeid"] = request.session.get("structtypeid")#结构类型
			builddict["building_earthquakeid"] = request.session.get("EQID")#地震id
			builddict["building_userid"] = request.session.get('USERID')#用户id
			builddict["building_longitude"] = float(request.POST.get("build_longitude",0))#建筑物中心经度
			builddict["building_latitude"] = float(request.POST.get("build_latitude",0))#建筑物中心纬度
			builddict["building_province"] = request.POST.get("build_province")#建筑物所在省份
			builddict["building_city"] = request.POST.get("build_city")#建筑物所在城市
			builddict["building_district"] = request.POST.get("build_district")#建筑物所在县区
			builddict["building_locationdetail"] = request.POST.get("xiangxidiqu")#详细地区
			builddict["building_admregioncode"] = request.POST.get("build_admregioncode")#建筑物所在行政区编号
			builddict["building_areanumber"] = request.POST.get("build_areanumber")#建筑物所在地区
			#有了抗震设防才有抗震烈度
			builddict["building_fortificationinfo"] = request.POST.get("level")#建筑物抗震设防情况
			#先判断level值
			if builddict["building_fortificationinfo"] =="1":
				builddict["building_fortificationdegree"] = "";
			else:
				builddict["building_fortificationdegree"] = request.POST.get("yl")#建筑物抗震设防中心烈度
			# identify_result.identifydict["building"] = builddict
			# print identify_result.identifydict["building"]
			print "ready to save tem building"
			try:#检测是否有临时建筑物信息，如果有说明此次是修改而不是新建
				print "modify buildinformation start"
				buidObj = building_information_tem.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
				try:
					usage = building_usage.objects.get(id = builddict["building_buildusage"])
					areanumber = region.objects.get(Q(region_location__startswith = builddict["building_areanumber"]))
					buidObj.building_buildusage = usage
					buidObj.building_areanumber = areanumber
					buidObj.building_number =  builddict["building_number"]
					buidObj.building_buildname =  builddict["building_buildname"]
					buidObj.building_uplayernum =  builddict["building_uplayernum"]
					buidObj.building_downlayernum =  builddict["building_downlayernum"]
					buidObj.building_partlayernum =  builddict["building_partlayernum"]
					buidObj.building_househostname =  builddict["building_househostname"]
					buidObj.building_buildyear =  builddict["building_buildyear"]
					buidObj.building_buildarea =  builddict["building_buildarea"]
					buidObj.building_longitude =  builddict["building_longitude"]
					buidObj.building_latitude =  builddict["building_latitude"]
					buidObj.building_province =  builddict["building_province"]
					buidObj.building_city =  builddict["building_city"]
					buidObj.building_district =  builddict["building_district"]
					buidObj.building_locationdetail =  builddict["building_locationdetail"]
					buidObj.building_admregioncode =  builddict["building_admregioncode"]
					buidObj.building_fortificationinfo =  builddict["building_fortificationinfo"]
					buidObj.building_fortificationdegree =  builddict["building_fortificationdegree"]
					buidObj.save()
					print "modify success"
				except:
					return HttpResponseRedirect('/t/checkup3')
			except:
				try:
					construct = building_structure.objects.get(id = builddict["building_constructtypeid"])
					usage = building_usage.objects.get(id = builddict["building_buildusage"])
					areanumber = region.objects.get(Q(region_location__startswith = builddict["building_areanumber"]))
					earthquake = EQInfo.objects.get(id = builddict["building_earthquakeid"])
					user = sys_user.objects.get(id = builddict["building_userid"])
					print "foreignkey get success"
					mybuild = building_information_tem(
						building_buildnumber = builddict["building_buildnumber"],
						building_number = builddict["building_number"],
						building_constructtypeid = construct,
						building_buildusage = usage,
						building_areanumber = areanumber,
						building_earthquakeid = earthquake,
						building_userid = user,
						building_buildname = builddict["building_buildname"],
						building_uplayernum = builddict["building_uplayernum"],
						building_downlayernum = builddict["building_downlayernum"],
						building_partlayernum = builddict["building_partlayernum"],
						building_househostname = builddict["building_househostname"],
						building_buildyear = builddict["building_buildyear"],
						building_buildarea = builddict["building_buildarea"],
						building_longitude = builddict["building_longitude"],
						building_latitude = builddict["building_latitude"],
						building_province = builddict["building_province"],
						building_city = builddict["building_city"],
						building_district = builddict["building_district"],
						building_locationdetail = builddict["building_locationdetail"],
						building_admregioncode = builddict["building_admregioncode"],
						building_fortificationinfo = builddict["building_fortificationinfo"],
						building_fortificationdegree = builddict["building_fortificationdegree"],
						)
					print "tem_buiding init over"*10
					# myBuild = building_information(**build)
					#为了保证保存时，保存完一个表另一个表出现故障，要对以保存的表进行删除操作，如保存环境信息时出现错误，要对刚保存的建筑物数据删除
					mybuild.save()
					print "tem_buiding save over"*10
				except:
					HttpResponse("建筑物信息有误！请核对后再保存！")
		except:
			print "no value"
		print request.POST.get("build_areanumber"),"#"*60

		return HttpResponseRedirect('/t/checkup4')


def checkup4(request):
	context = RequestContext(request)
	context_dict = {}
	context_dict["foundation_status"] = foundation_status.objects.all()
	context_dict["field_effect"] = field_effect.objects.all()
	if request.session.get("user_id"):
		userid = request.session.get("user_id")#用户编号
	else:
		print "no user id "
		return HttpResponseRedirect('/t')
	if request.session.get("EQid"):
		earthquakeid = request.session.get("EQid")#地震编号
	else:
		print "no eq id "
		return HttpResponseRedirect('/t/checkup')
	if request.session.get("structtypename"):
		context_dict["structtypename"] = request.session.get("structtypename")#地震编号
	else:
		print "no structname "
		return HttpResponseRedirect('/t/checkup2')
	if request.session.get("structtype"):
		structtype = request.session.get("structtype")#地震编号
	else:
		print "no structtype "
		return HttpResponseRedirect('/t/checkup2')
	try:
		b = building_information_tem.objects.get(building_buildnumber = request.session.get("building_buildnumber"))#建筑物实例
	except:
		return HttpResponseRedirect('/t/checkup3')
	if request.method == "GET":
		print "enter checkup4 GET"
		try:
			# environmentObj = environment_tem.objects.get(environment_buildnumber__building_userid__user_id = request.session.get('user_id'))
			environmentObj = environment_tem.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
			context_dict["building_environment"] = environmentObj
		except: 
			print "tem_environment has no value！"
			try:
				environmentObj = environment.objects.filter(environment_buildnumber__building_userid__user_id = request.session.get('user_id'))[0]
				context_dict["building_environment"] = environmentObj
				print "get enviroment in database success"
			except:
				print "database has no environment value"
				return render_to_response('transport/checkup4.html',context_dict,context)
		cdyx = environmentObj.environment_earthquakeeff.split(",")
		djzk = environmentObj.environment_foundation.split(",")
		if "CDYXQT" in environmentObj.environment_earthquakeeff:
			context_dict["cdyxqita"] = ((cdyx[-1])[3:-2]).decode('unicode_escape')
		if "DJZKQT" in environmentObj.environment_foundation:
			context_dict["djzkqita"] = ((djzk[-1])[3:-2]).decode('unicode_escape')

		return render_to_response('transport/checkup4.html',context_dict,context)
	else:
		print "enter checkup4 POST"
		environment1 = {}
		cdyx = request.POST.getlist("cdyx")
		if "CDYXQT" in cdyx:
			cdyx.append(request.POST.get("cdyxqita"))
		environment1["environment_earthquakeeff"] = cdyx
		djzk = request.POST.getlist("djzk")
		if 'DJZKQT' in djzk:
			djzk.append(request.POST.get("djzkqita"))
		environment1["environment_foundation"] = djzk
		environment1["environment_adjoinbuild"] = request.POST.getlist("pljz")
		environment1["environment_seismicintensity"] = request.POST.get("ph")
		environment1["environment_smallaffect"] = request.POST.get("ps")
		environment1["environment_bigaffect"] = request.POST.get("pb")
		#保存环境信息到临时表
		print "get enviroment post info success"
		try:
			#判断是否是修改环境信息
			# environmentObj = environment_tem.objects.get(environment_buildnumber__building_userid__user_id = request.session.get('user_id'))
			environmentObj = environment_tem.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
			print "modify tem environment start"
			try:
				environmentObj.environment_earthquakeeff = environment1["environment_earthquakeeff"]
				environmentObj.environment_foundation = environment1["environment_foundation"]
				environmentObj.environment_adjoinbuild = environment1["environment_adjoinbuild"]
				environmentObj.environment_seismicintensity = environment1["environment_seismicintensity"]
				environmentObj.environment_smallaffect = environment1["environment_smallaffect"]
				environmentObj.environment_bigaffect = environment1["environment_bigaffect"]
				environmentObj.save()
				print "modify tem environment over"
			except:
				print "modify tem environment failed"
				return HttpResponseRedirect('/t/checkup4')
		except: 
			print "tem_environment has no value！"
			try:
				b = building_information_tem.objects.get(building_buildnumber = request.session.get("building_buildnumber"))#建筑物实例
				print "get tem buildinfo success"
				print b
			except:
				print "no tem buildinginfo"
			try:
				print "tem environment save start"
				myenvironment = environment_tem(environment_buildnumber = b,**environment1)
				print "****************"
				myenvironment.save()
				print "tem environment save over"
			except:
				print "save environment failed"
		# print "this is checkup4 the cdyx is ",cdyx[:],"   and  the djzk is  ",djzk," and the fzld is ",fzld,"  and the ps is ",xz,"and zhe dz is ",dz
		return HttpResponseRedirect('/t/checkup5')
def checkup5(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method == "GET":
		print "enter checkup5 GET"
		try:
			userid = request.session.get('user_id')#获取用户id
		except:
			return HttpResponseRedirect('/t')
		try:
			earthquakeid = request.session.get("EQid")#地震编号
		except:
			return HttpResponseRedirect('/t/checkup')
		try:
			context_dict["structtypename"] = request.session.get("structtypename")
			structtype = request.session.get("structtype")#获取结构类型编号
		except:
			return HttpResponseRedirect('/t/checkup2')
		try:#测试有无建筑物信息
			# buidObj = building_information_tem.objects.get(building_constructtypeid__construct_typeid = structtype,building_userid__user_id=userid,building_earthquakeid__eq_earthquakeid=earthquakeid)
			buidObj = building_information_tem.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
			print "*"*60
		except:
			return HttpResponseRedirect('/t/checkup3')
		try:
			# environmentObj = environment_tem.objects.get(environment_buildnumber__building_userid__user_id = request.session.get('user_id'))
			environmentObj = environment_tem.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
		except: 
			return HttpResponseRedirect('/t/checkup4')
		try:
			print "n1"
			sublocalObj = sublocal.objects.filter(sublocal_constructtypeid__construct_typeid = structtype)#查询出所有的细部震损信息
			locationObj = buildlocation.objects.filter(location_constructtype__construct_typeid = structtype)#查询出所有部位信息
			catalogObj = SubLocationCatalog.objects.filter(catalog_constructtypeid__construct_typeid = structtype)#查询出所有的细部分类信息
		except:
			print "no value sublocalObj"
		try:
			print str("n2")
			context_dict["sublocalObj"] = sublocalObj
			context_dict["locationObj"] = locationObj
			context_dict["catalogObj"] = catalogObj
			context_dict["struct"] = sublocalObj[0].sublocal_constructtypeid
		except:
			return HttpResponseRedirect('/t/checkup')
		# try:
		# 	print str("n3")
		# 	context_dict["dama_data"] = identify_result.identifydict["dama_data"]
		# except:
		# 	print str("no damage information")
		try:
			buidObj = building_information_tem.objects.filter(building_constructtypeid__construct_typeid = structtype,building_userid__user_id=request.session.get('user_id'),building_earthquakeid__eq_earthquakeid=request.session.get("EQid"))[0]
			buildnum = buidObj.building_buildnumber
			print str("Build id is："),buildnum
			dataObj = damage_tem.objects.filter(damage_id = buildnum)
			print "here"
			for x in dataObj:
				print x.damage_locationid
			context_dict["dama_data"] = dataObj
		except:
			print "database has no dama_data value"
		return render_to_response('transport/checkup5.html',context_dict,context)
	else:
		print "enter checkup5 post"
		quakedata = request.POST.get("name")
		try:
			data = quakedata.split("*")
			data_list = []
		except:
			print "ss"
		try:
			for x in data:
				data_item = eval(x)
				# print data_item
				data_list.append(data_item)
				print data_item["damage_isfirst"]
		except:
			print "mei de shi ni a "
		try:
			buidObj_tem = building_information_tem.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
		except:
			return HttpResponse("未提交建筑物信息！")
		try:
			# environmentObj = environment_tem.objects.get(environment_buildnumber__building_userid__user_id = request.session.get('user_id'))
			environmentObj_tem = environment_tem.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
		except: 
			return HttpResponse("未提交环境信息！")
		try:
			print "test the building_buildnumber exist"
			try:
				buidObj_exist = building_information.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
				buidObj_exist.delete()
				print "building_information zhong  build yi shan chu   "
			except:
				print "building_information zhong  mei  you  gai build   "
			print "save build_information start"
			mybuild = building_information(
				building_buildnumber =buidObj_tem.building_buildnumber,
				building_number = buidObj_tem.building_number,
				building_constructtypeid = buidObj_tem.building_constructtypeid,
				building_buildusage =  buidObj_tem.building_buildusage,
				building_areanumber = buidObj_tem.building_areanumber,
				building_earthquakeid = buidObj_tem.building_earthquakeid,
				building_userid = buidObj_tem.building_userid,
				building_buildname = buidObj_tem.building_buildname,
				building_uplayernum = buidObj_tem.building_uplayernum,
				building_downlayernum = buidObj_tem.building_downlayernum,
				building_partlayernum = buidObj_tem.building_partlayernum,
				building_househostname = buidObj_tem.building_househostname,
				building_buildyear = buidObj_tem.building_buildyear,
				building_buildarea = buidObj_tem.building_buildarea,
				building_longitude = buidObj_tem.building_longitude,
				building_latitude = buidObj_tem.building_latitude,
				building_province = buidObj_tem.building_province,
				building_city = buidObj_tem.building_city,
				building_district = buidObj_tem.building_district,
				building_locationdetail = buidObj_tem.building_locationdetail,
				building_admregioncode = buidObj_tem.building_admregioncode,
				building_fortificationinfo = buidObj_tem.building_fortificationinfo,
				building_fortificationdegree = buidObj_tem.building_fortificationdegree,
				building_createdate = buidObj_tem.building_createdate,
				)
			mybuild.save()
			print "build has saved"
		except:
			return HttpResponse("未能保存建筑物信息！")
		try:
			print "test the environment exist"
			try:
				envi_exist = environment.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
				envi_exist.delete()
				print "delete environment success"
			except:
				print "environment zhong  wu ci environment_info"
			print "save environment start"
			b = building_information.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
			myenvironment = environment(
				environment_buildnumber = b,
				environment_earthquakeeff = environmentObj_tem.environment_earthquakeeff,
				environment_foundation = environmentObj_tem.environment_foundation,
				environment_adjoinbuild = environmentObj_tem.environment_adjoinbuild,
				environment_seismicintensity = environmentObj_tem.environment_seismicintensity,
				environment_smallaffect = environmentObj_tem.environment_smallaffect,
				environment_bigaffect = environmentObj_tem.environment_bigaffect,
				)
			myenvironment.save()
			print "environment has saved"
		except:
			#保存环境信息出错需要删除已保存的建筑物信息
			try:#按理说没必要这样做，但是为了保险，还是try下吧
				mybuild_info = building_information.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
				mybuild_info.delete()
			except:
				print "bao cun huangjing shi bai,qie shan chu build shibai"
				return HttpResponse("没有要删除的编号为"+request.session.get('building_buildnumber')+"的建筑物信息！")
			# return HttpResponse("未能保存环境信息！")
		try:
			#数据都保存到了正式表中，需要将临时表中数据删除
			print "delete tem environment start"
			environmentObj_tem.delete()
			print "tem environment delete success"
		except:
			mybuild_info = building_information.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
			mybuild_info.delete()
			environment_info = environment.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
			environment_info.delete()
			return HttpResponse("系统错误2！")
		try:
			#数据都保存到了正式表中，需要将临时表中数据删除
			print "delete tem build start"
			
			print buidObj_tem.building_buildnumber,"#"*20
			buidObj_tem.delete()
			print "tem build delete success"
				# return HttpResponse("临时表中没有要删除的编号为"+request.session.get('building_buildnumber')+"的建筑物信息！")
		except:
			print "error",request.session.get('building_buildnumber')
			# mybuild_info = building_information.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
			# mybuild_info.delete()
			# environment_info = environment.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
			# environment_info.delete()
			# return HttpResponse("系统错误1,请重新提交!")
		try:
			try:
				b = building_information.objects.get(building_buildnumber = request.session.get("building_buildnumber"))
			except:
				HttpResponse("没有建筑物编号为"+request.session.get('building_buildnumber')+"的建筑物信息！")
			try:
				construct = building_structure.objects.get(id = request.session.get("structtypeid"))
			except:
				HttpResponse("没有结构类型编号为"+request.session.get("structtypeid")+"的结构类型信息！")
			for xx in data_list:
				local = xx["damage_locationid"]
				catalog = xx["damage_catalogid"]
				sub = xx["damage_sublocationid"]
				localObj = buildlocation.objects.get(id = local)
				catalogObj = SubLocationCatalog.objects.get(id = catalog)
				sub = sublocal.objects.get(id = sub)
				buid = request.session.get('building_buildnumber')
				myitem = damage(
					damage_id = buid,
					damage_buildnumber = b,
					damage_constructtypeid = construct,
					damage_locationid = localObj,
					damage_catalogid = catalogObj,
					damage_sublocationid = sub,
					damage_number = xx["damage_number"],
					damage_degree = xx["damage_degree"],
					damage_parameteradjust = float(xx["damage_parameteradjust"]),
					damage_description = xx["damage_description"],
					damage_isfirst = xx["damage_isfirst"],
					)
				myitem.save()
				print "saved + 1"
		except:
			HttpResponse("震损信息有误！请核对后再保存！")
		print "**"*30
		b = building_information.objects.get(building_buildnumber = request.session.get("building_buildnumber"))
		print b.building_buildnumber

		result = identify_result(
			result_buildnumber = b,
			result_id = "result",
			result_securitycategory = "可用",
			result_totaldamageindex = random.random(),
			result_damagedegree = "轻微破坏",
			)
		result.save()
	return HttpResponse("success")

def check5save(request):
	print "enter checkup5save method"
	quakedata = request.POST.get("name")
	try:
		data = quakedata.split("*")
		data_list = []
	except:
		print "ss"
	try:
		for x in data:
			data_item = eval(x)
			# print data_item
			data_list.append(data_item)
			print data_item["damage_isfirst"]
	except:
		print "mei de shi ni a "
	# try:
	print request.session.get("building_buildnumber")
	b = building_information_tem.objects.get(building_buildnumber = request.session.get("building_buildnumber"))
	# print b.decode('utf8')
	print request.session.get("structtypeid")
	construct = building_structure.objects.get(id = request.session.get("structtypeid"))
	print construct
	damageObj = damage_tem.objects.filter(damage_buildnumber = b)
	if damageObj:
		damageObj.delete()
	for xx in data_list:
		local = xx["damage_locationid"]
		catalog = xx["damage_catalogid"]
		sub = xx["damage_sublocationid"]
		# localObj = buildlocation.objects.get(id = local)
		# catalogObj = SubLocationCatalog.objects.get(id = catalog)
		# sub = sublocal.objects.get(id = sub)
		# buid = request.session.get('building_buildnumber')
		print "enter forloop"
		cursor = connection.cursor()            #获得一个游标(cursor)对象
		# cursor = connection.cursor()            #获得一个游标(cursor)对象
		#更新操作
		print request.session.get('building_buildnumber')
		print b.id
		print request.session.get('building_buildnumber')
		print b.id,request.session.get("structtypeid"),local,catalog,sub,xx["damage_number"],xx["damage_degree"],float(xx["damage_parameteradjust"]),xx["damage_description"],xx["damage_isfirst"]
		sqlstring = 'insert into transport_damage_tem (damage_id,damage_buildnumber_id,damage_constructtypeid_id,damage_locationid_id,damage_catalogid_id,damage_sublocationid_id,damage_number,damage_degree,damage_parameteradjust,damage_description,damage_isfirst) values(%s,%d,%d,%d,%d,%d,%s,%s,%f,%s,%s)'
		print "here"
		# cursor.execute(sqlstring,[request.session.get('building_buildnumber'),b.id,request.session.get("structtypeid"),local,catalog,sub,xx["damage_number"],xx["damage_degree"],float(xx["damage_parameteradjust"]),xx["damage_description"],xx["damage_isfirst"]])    #执行sql语句
		cursor.execute(sqlstring,['RCYH001EQ001201411240001',43,3,1,1,1,'0','0',0.0,'','yes'])    #执行sql语句
		print "here"
		transaction.commit_unless_managed() #提交到数据库
		print "saved + 1"   
			# myitem = damage_tem(
			# 	damage_id = buid,
			# 	damage_buildnumber = b,
			# 	damage_constructtypeid = construct,
			# 	damage_locationid = localObj,
			# 	damage_catalogid = catalogObj,
			# 	damage_sublocationid = sub,
			# 	damage_number = xx["damage_number"],
			# 	damage_degree = xx["damage_degree"],
			# 	damage_parameteradjust = float(xx["damage_parameteradjust"]),
			# 	damage_description = xx["damage_description"],
			# 	damage_isfirst = xx["damage_isfirst"],
			# 	)
			# myitem.save()
			
	# except:
		# print "保存check5错误".decode('utf8')
		# HttpResponse("震损信息有误！请核对后再保存！")
	print "**"*30
	return HttpResponse("success")


def checkup6(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('transport/checkup6.html',context_dict,context)


#统计页面
def count(request):
	context = RequestContext(request)
	context_dict = {}
	sqlstring = "SELECT DISTINCT a.building_buildnumber,b.result_securitycategory,b.result_totaldamageindex,a.building_admregioncode,a.building_buildname,a.building_province,a.building_househostname,f.construct_typename,a.building_buildyear,a.building_fortificationinfo,a.building_fortificationdegree,e.eq_epicentralintensity,b.result_assetdate,a.building_longitude,a.building_latitude,a.building_buildarea,a.building_uplayernum,d.building_usagename,c.user_id,c.user_realname,c.user_title,c.user_workunit,b.result_damagedegree from transport_building_information a ,transport_identify_result b,transport_sys_user c,transport_building_usage d,transport_eqinfo e,transport_building_structure f where c.user_id = '"+request.session.get("user_id")+"' and b.result_buildnumber_id = a.id and a.building_userid_id = c.id and a.building_buildusage_id = d.id and a.building_earthquakeid_id = e.id and f.id = a.building_constructtypeid_id "
	if request.method == "GET":
		qstring = request.GET.get("qstring1","")
		if qstring == "":
			resultObj = identify_result.objects.filter()
		else:
			print "#"*30
			print qstring
			qstring = qstring.replace("@@@","%")
			sqlstring = sqlstring +qstring+")"
			print sqlstring
	cursor = connection.cursor()            #获得一个游标(cursor)对象
	cursor.execute(sqlstring)
	print sqlstring
	resultObj = cursor.fetchall() 
	print "*"*50
	p = Paginator(resultObj,10)

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

#地图数据接口
def countMap(request):
	context = RequestContext(request)
	context_dict = {}
	sqlstring = "SELECT DISTINCT a.building_longitude as longitude,a.building_latitude as latitude,b.result_securitycategory as safe,f.construct_typename as struct ,f.id as icon,a.building_buildyear as years ,concat(a.building_province,a.building_city,a.building_district,a.building_locationdetail) address from transport_building_information a ,transport_identify_result b,transport_sys_user c,transport_building_usage d,transport_eqinfo e,transport_building_structure f where c.user_id = '"+request.session.get("user_id")+"' and b.result_buildnumber_id = a.id  and a.building_earthquakeid_id = e.id and f.id = a.building_constructtypeid_id "
	if request.method == "POST":
		qstring = request.POST.get("qstring1","")
		if len(qstring) <15:
			print qstring
		else:
			# print qstring
			qstring = qstring.replace("@@@","%")
			sqlstring = sqlstring +qstring+")"
			print sqlstring 
	cursor = connection.cursor()            #获得一个游标(cursor)对象
	cursor.execute(sqlstring)
	resultObj = dictfetchall(cursor)
	print "%"*60
	return HttpResponse(json.dumps(resultObj))
#统计图表接口_sj
def countCharts_sj(request):
	context = RequestContext(request)
	context_dict = {}
	sj_sqlstring = "select count(*) as '栋数',DATE_FORMAT(building_createdate,'%Y-%m' ) as '月份' from transport_building_information a,transport_sys_user b,transport_identify_result c where a.id = c.result_buildnumber_id and a.building_userid_id = b.id and b.user_id = '"+request.session.get("user_id")+"' GROUP BY DATE_FORMAT(building_createdate,'%Y-%m' )"
	if request.method == "POST":
		qstring = request.POST.get("qstring1","")
		if len(qstring) <15:
			print qstring
		else:
			# print qstring
			qstring = qstring.replace("@@@","%")
			sj_sqlstring = sj_sqlstring +qstring+")"
			print sj_sqlstring 
	cursor = connection.cursor()            #获得一个游标(cursor)对象
	cursor.execute(sj_sqlstring)
	resultObj = sj_fetchall(cursor)
	print "%"*60
	print resultObj
	return HttpResponse(json.dumps(resultObj))
#统计图表接口_use
def countCharts_use(request):
	context = RequestContext(request)
	context_dict = {}
	sj_sqlstring = "select sum(a.building_buildarea) as 面积,count(*) as '栋数',case a.building_buildusage_id when 1 then '住宅' when 2 then '政府' WHEN 3 then '商业' when 4 then '站点' when 5 then '工业厂房' WHEN 6 then '公共集会场所' when 7 then '医疗卫生系统' when 8 then '生命线' WHEN 9 then '文化教育系统' else '其它' end from transport_building_information a,transport_identify_result b,transport_building_usage c,transport_sys_user d where d.user_id = '"+request.session.get("user_id")+"' and a.building_userid_id = d.id   and a.id = b.result_buildnumber_id and c.id = a.building_buildusage_id GROUP BY case a.building_buildusage_id when 1 then '住宅' when 2 then '政府' WHEN 3 then '商业' when 4 then '站点' when 5 then '工业厂房' WHEN 6 then '公共集会场所' when 7 then '医疗卫生系统' when 8 then '生命线' WHEN 9 then '文化教育系统' else '其它' end"
	if request.method == "POST":
		qstring = request.POST.get("qstring1","")
		if len(qstring) <15:
			print qstring
		else:
			# print qstring
			qstring = qstring.replace("@@@","%")
			sj_sqlstring = sj_sqlstring +qstring+")"
			print sj_sqlstring 
	cursor = connection.cursor()            #获得一个游标(cursor)对象
	cursor.execute(sj_sqlstring)
	resultObj = use_fetchall(cursor)
	print "%"*60
	print resultObj
	return HttpResponse(json.dumps(resultObj))
#统计图表接口_设防
def countCharts_sf(request):
	context = RequestContext(request)
	context_dict = {}
	sj_sqlstring = "select sum(a.building_buildarea) as 面积,case a.building_fortificationdegree	WHEN 6 then '6度设防'	when 7 then '7度设防'  when 8 then '8度设防'	WHEN 9 then '9度设防'	when 10 then '采用非正规抗震措施（民居、自建房等）' else '未设防'end ,count(*) as '栋数' from transport_building_information a,transport_identify_result b,transport_building_usage c,transport_sys_user d where d.user_id = '"+request.session.get("user_id")+"' and  a.building_userid_id = d.id   and a.id = b.result_buildnumber_id and c.id = a.building_buildusage_id GROUP BY case a.building_fortificationdegree WHEN 6 then '6度设防'	when 7 then '7度设防' when 8 then '8度设防'	WHEN 9 then '9度设防' when 10 then '采用非正规抗震措施（民居、自建房等）' else '未设防'end"
	if request.method == "POST":
		qstring = request.POST.get("qstring1","")
		if len(qstring) <15:
			print qstring
		else:
			# print qstring
			qstring = qstring.replace("@@@","%")
			sj_sqlstring = sj_sqlstring +qstring+")"
			print sj_sqlstring 
	cursor = connection.cursor()            #获得一个游标(cursor)对象
	cursor.execute(sj_sqlstring)
	resultObj = sf_fetchall(cursor)
	print "%"*60
	print resultObj
	return HttpResponse(json.dumps(resultObj))
#chu li user
def user(request):
	context = RequestContext(request)
	context_dict = user_query(request)
	return render_to_response('transport/user.html',context_dict,context)

def edituser(request):
	context = RequestContext(request)
	context_dict = {}
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
			context_dict["savesuc"] = "保存成功！"
	context_dict["user"] = user_query(request)	
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
	
def readFile(fn, buf_size=262144):
	f = open(fn, "rb")
	while True:
		c = f.read(buf_size)
		if c:
			yield c
		else:
			break
	f.close()
   

def downloadpdf(request):
	from cStringIO import StringIO
	#from xhtml2pdf import pisa as pisa
	import xhtml2pdf.pisa as pisa 
	data = open('templates/transport/pdf.html').read()
	result = file('templates/test.pdf', 'wb') 
	pdf = pisa.CreatePDF(data, result)
	result.close() 
	data1 = readFile('templates/test.pdf')
	response = HttpResponse( data1,content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="test.pdf"'	
	return response
	
# def dlcompdf(request):
# 	from cStringIO import StringIO
# 	#from xhtml2pdf import pisa as pisa
# 	import xhtml2pdf.pisa as pisa 
# 	data = open('templates/transport/compdf.html').read()
# 	result = file('templates/report.pdf', 'wb') 
# 	pdf = pisa.CreatePDF(data, result)
# 	result.close() 
# 	data1 = readFile('templates/report.pdf')
# 	response = HttpResponse( data1,content_type='application/pdf')
# 	response['Content-Disposition'] = 'attachment; filename="report.pdf"'	
# 	return response

	
def dlcompdf(request):
	from cStringIO import StringIO
	#from xhtml2pdf import pisa as pisa
	import xhtml2pdf.pisa as pisa 
	import urllib2
	import urllib
	import httplib
	from random import Random
	htmlcontent = urllib2.urlopen('http://localhost:8000/t/pdfdata?buildid='+request.session.get('building_buildnumber')).read()
	myhtml2pdf = open('templates/myhtml2pdf.html','wb')
	myhtml2pdf.write(htmlcontent)
	myhtml2pdf.close()
	data1 = open('templates/myhtml2pdf.html').read()
	# data = open('/t/pdfdata').read()
	result = file('templates/report.pdf', 'wb') 
	pdf = pisa.CreatePDF(data1, result)
	result.close() 
	data1 = readFile('templates/report.pdf')
	response = HttpResponse( data1,content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="report.pdf"'	
	return response

#读取页面提交数据存要生成的报告中
def pdfdata(request):
	context = RequestContext(request)
	context_dict = {}
	if len(request.GET.get("buildid",""))>2:
	#context_dict['build'] = request.session.get["building_buildnumber"]
		build_obj = building_information.objects.get(building_buildnumber = request.GET.get('buildid'))
		if build_obj:
			context_dict['build_obj'] = build_obj
			context_dict['usage'] = building_usage.objects.get(building_usageid = build_obj.building_buildusage)
		environmentObj = environment.objects.get(environment_buildnumber__building_buildnumber = request.GET.get('buildid'))
		damageObj = damage.objects.filter(damage_buildnumber__building_buildnumber = request.GET.get('buildid'))
	else:
		build_obj = building_information.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
		if build_obj:
			context_dict['build_obj'] = build_obj
			context_dict['usage'] = building_usage.objects.get(building_usageid = build_obj.building_buildusage)
		environmentObj = environment.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
		damageObj = damage.objects.filter(damage_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
	if environmentObj:
		context_dict['building_environment'] = environmentObj
	if damageObj:
		context_dict['xdamage'] = damageObj
	return render_to_response('transport/compdf.html',context_dict,context) 
def test(request):
	
    cursor = connection.cursor()            #获得一个游标(cursor)对象
    cursor.execute('SELECT DISTINCT a.building_buildnumber,b.result_securitycategory,b.result_totaldamageindex,a.building_admregioncode,a.building_buildname,a.building_province,a.building_househostname,f.construct_typename,a.building_buildyear,a.building_fortificationinfo,a.building_fortificationdegree,e.eq_epicentralintensity,b.result_assetdate,a.building_longitude,a.building_latitude,a.building_buildarea,a.building_uplayernum,d.building_usagename,c.user_id,c.user_realname,c.user_title,c.user_workunit,b.result_damagedegree from transport_building_information a ,transport_identify_result b,transport_sys_user c,transport_building_usage d,transport_eqinfo e,transport_building_structure f where b.result_buildnumber_id = a.id and a.building_userid_id = c.id and a.building_buildusage_id = d.id and a.building_earthquakeid_id = e.id and f.id = a.building_constructtypeid_id and c.user_name like "%s%\";')
    raw = cursor.fetchall() 
    print raw[0]
    return HttpResponse(raw)