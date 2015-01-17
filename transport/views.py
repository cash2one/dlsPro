# coding=utf-8
from django.db import connection,transaction
from django.shortcuts import render
from django.conf import settings
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
from pyExcelerator import *
import string
import os
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
import hashlib 
import sys
import cStringIO
from datetime import *
from models import *
from storage import * 
from django.core.mail import send_mail
from PIL import Image, ImageDraw, ImageFont
import random
import time
import re
from random import choice
import string
import urllib2
from xlwt import *
import sys 
from cStringIO import StringIO
import xhtml2pdf.pisa as pisa 
import urllib2
import urllib
import httplib
from random import Random
reload(sys) 
sys.setdefaultencoding('utf8')

youke = 1
def GenPassword(length=3,chars=string.ascii_letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])

def register_info1(request):
	context = RequestContext(request)
	context_dict = {}
	usercl=request.POST.get('clazz')
	userid=' '
	user=[]
	if(usercl=="1"):
		userid='G'+GenPassword(3)
		user=sys_user.objects.filter(user_id=userid)
		context_dict['idtag'] = "genenal"
		while user:
			userid='G'+GenPassword(3)
			user=sys_user.objects.filter(user_id=userid)
	else:
		userid='P'+GenPassword(3)
		user=sys_user.objects.filter(user_id=userid)
		context_dict['idtag'] = "profession"
		while user:
			userid='P'+GenPassword(3)
			user=sys_user.objects.filter(user_id=userid)

	#Storage.userid=request.POST.get('userid')
	Storage.userid=userid
	Storage.username=request.POST.get('username')
	Storage.password=request.POST.get('password')

	majorObj = user_major.objects.all()
	if majorObj:
		context_dict["majorObj"] = majorObj
	departObj = user_depart.objects.all()
	if departObj:
		context_dict["departObj"] = departObj
	titleObj = user_title.objects.all()
	if titleObj:
		context_dict["titleObj"] = titleObj
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
	if p.user_id[:1] == "P":
		p.user_role = "专家用户"
	else:
		p.user_role = "普通用户"
	p.user_createtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	p.user_updatetime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	p.save()
	title='激活账号'
	massage='请点击该链接激活账户  http://'+request.get_host()+'/t/register_activate1?id='+p.user_id.encode('utf8')
	sender='iem_SABPE@163.com'
	mail_list=[request.POST.get('bemail')]
	send_mail(
		title,
		massage,
		sender,
		mail_list,
		fail_silently=True,  
		)
	return render_to_response('transport/register2.html',{'email':p.user_email,'href':'http://mail.'+p.user_email.split('@')[1]},context)

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


def get_check_code_image(request):
	try:
		image="static/img/imgcode.jpg"
		im = Image.open(image)
		fontstyle ="static/file/arial.ttf"
		draw = ImageDraw.Draw(im)
		mp = hashlib.md5()
		mp_src = mp.update(str(datetime.now()))
		mp_src = mp.hexdigest()
		rand_str = mp_src[0:4]
		font=ImageFont.truetype(fontstyle, random.randrange(22,32))
		fontcolor = (random.randrange(150,255),random.randrange(70,150),random.randrange(0,70))
		draw.text((5,0), rand_str[0], font = font,fill=fontcolor)
		fontcolor = (random.randrange(150,255),random.randrange(0,70),random.randrange(70,150))
		draw.text((20,0), rand_str[1], font = font,fill=fontcolor)
		fontcolor = (random.randrange(70,150),random.randrange(0,70),random.randrange(150,255))
		draw.text((35,0), rand_str[2], font = font,fill=fontcolor)
		fontcolor = (random.randrange(0,70),random.randrange(150,255),random.randrange(70,150))
		draw.text((50,0), rand_str[3], font = font,fill=fontcolor)
		del draw
		request.session['checkcode'] = rand_str
		buf = cStringIO.StringIO()
		im.save(buf,'gif')
	except Exception,e:
		if settings.DEBUG == True:
			print "error ",e
		else:
			pass
	return HttpResponse(buf.getvalue(),'img/gif')

def activate1(request):
	context = RequestContext(request)
	u_id=request.GET.get('id','-1')
	if settings.DEBUG == True:
		print u_id
	else:
		pass
	try:
		p=sys_user.objects.get(user_id = u_id)
		if settings.DEBUG == True:
			print p.user_id 
		else:
			pass
		p.user_state="已激活"
		p.save()
		if settings.DEBUG == True:
			print p.user_state
		else:
			pass
	except:
		if settings.DEBUG == True:
			print "no user"
		else:
			pass
	
	return render_to_response('transport/register4.html',context)

def islogined(request):
	username = request.session.get("username")
	if settings.DEBUG == True:
		print "被调用"
	else:
		pass
	if username:
		return 'true'
	else:
		return 'false'

def user_query(request):
	context = RequestContext(request)
	context_dict = {}
	client_obj = sys_user.objects.filter(user_name = request.session.get('username'))
	if client_obj:
		context_dict['username'] = client_obj[0].user_name
		context_dict['userrealname'] = client_obj[0].user_realname
		context_dict['userid'] = client_obj[0].user_id
		context_dict['useridcard'] = client_obj[0].user_idcard
		context_dict['title'] = client_obj[0].user_title
		context_dict['danwei'] = client_obj[0].user_workunit
		context_dict['password'] = client_obj[0].user_password
		context_dict['profession'] = client_obj[0].user_major
		context_dict['address'] = client_obj[0].user_address
		context_dict['telnum'] = client_obj[0].user_tel
		context_dict['email'] = client_obj[0].user_email
		context_dict['zipcode'] = client_obj[0].user_postcode
		request.session['userrole'] = client_obj[0].user_role 
		lastlogintime = client_obj[0].user_lastlogintime
		context_dict["lastlogintime"] = lastlogintime
		request.session["logincount_zong"] = loginCount.objects.filter().count()
		request.session["todaycount"] = loginCount.objects.filter(login_date = date.today()).count()
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
	try:
		client_obj = sys_user.objects.get(user_name = request.session.get("username"))
	except:
		client_obj = sys_user.objects.get(user_name = "ykyh")
	client_obj.user_lastalivetime = '1970-01-01 00:00:00'
	client_obj.user_currenthost = ''
	client_obj.save()
	request.session.clear()
	return render_to_response('transport/login.html',context_dict,context)


def ditu(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('transport/dls_pro.html',context_dict,context)


def adLogVal(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method == 'POST':
		user = request.POST.get("uname","")
		password = request.POST.get("upass","")
		try:
			client_obj = sys_user.objects.get(user_name = user)
			try:
				client_obj = sys_user.objects.get(user_name = user,user_password = password)
				return HttpResponse("success")
			except:
				return HttpResponse("用户名密码不匹配!")
		except:
			return HttpResponse("用户不存在!")
	else:
		return HttpResponse("only support POST!")

def modUserPos(request):
	context = RequestContext(request)
	if request.method == 'POST':
		user = request.POST.get("username","")
		lon =  float(request.POST.get("lon",0))
		lat =  float(request.POST.get("lat",0))
		try:
			userObj = sys_user.objects.filter(user_name = user)[0]
			loctionObj = userLocation.objects.get(loc_user = userObj)
			loctionObj.loc_longitude = lon
			loctionObj.loc_latitude = lat
			loctionObj.save()
			return HttpResponse("success")
		except Exception,e:
			if settings.DEBUG == True:
				print "position save error ------------------->",e
			else:
				pass
			locationObj = userLocation(
			loc_user = userObj,
			loc_longitude = lon,
			loc_latitude = lat,)
			try:
				locationObj.save()
				return HttpResponse("success")
			except:
				return HttpResponse("modify failed")
	else:
		return HttpResponse("only support POST!")

def ulogin(request):
	context = RequestContext(request)
	context_dict = {}
	global youke
	youke = youke + 1
	request.session['realname'] = "游客"+str(youke)
	request.session['username'] = "youke"+str(youke)
	request.session['user_id'] = "YK9999"
	request.session['USERID'] = 9999
	return render_to_response('transport/index.html',context_dict,context)
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
					context_dict['error'] = '该用户尚未激活,请激活后再登录！'
					return render_to_response('transport/login.html',context_dict,context)
				lastalivetime = client_obj.user_lastalivetime
				if lastalivetime:
					lastalivetime = str(lastalivetime)
					time_last = datetime.strptime(lastalivetime,'%Y-%m-%d %H:%M:%S')
					time_now = datetime.now()
					time_now = str(time_now)[:19]
					time_now = datetime.strptime(time_now,'%Y-%m-%d %H:%M:%S')
					jiange = time_now - time_last
					if int(jiange.seconds) < 1200 and client_obj.user_currenthost != request.META.get("COMPUTERNAME"):
						waittime = 1200-int(jiange.seconds)
						context_dict['error'] = '用户未退出,请在%d秒后重试！'% waittime
						return render_to_response('transport/login.html',context_dict,context)
				client_obj.user_currenthost = request.META.get("COMPUTERNAME")
				client_obj.user_lastalivetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
				client_obj.user_lastlogintime = client_obj.user_logintime
				client_obj.user_logintime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
				address = urllib2.urlopen('http://pv.sohu.com/cityjson').read()#获取到ip地址和城市名  
				address = eval(str(address[19:-1]))#得到json字符串  
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
				loginCountObj = loginCount(
					login_user = client_obj,
					login_ip = ip,
					login_location = dizhi.decode('GBK')
					)
				loginCountObj.save()
				request.session['realname'] = client_obj.user_realname
				request.session['username'] = user
				request.session['user_id'] = client_obj.user_id
				request.session['USERID'] = client_obj.id
				return HttpResponseRedirect('/t/index')
			except:
				context_dict['error'] = '用户名密码不匹配'
				return render_to_response('transport/login.html',context_dict,context)
		else:
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
			else:
				value_new = value + '__icontains'
				args = {value_new:zhi}
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
		if request.POST.get("type")=="ajax":
			return HttpResponse("success")
		else:
			return HttpResponseRedirect('/t/checkup2')

def check_eq(request):
	context_dict = {}
	eq_id = request.GET.get("eq_id")
	EQ_obj = EQInfo.objects.get(eq_earthquakeid = eq_id)
	str1 = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (EQ_obj.eq_earthquakeid,EQ_obj.eq_earthquakename,EQ_obj.eq_date,EQ_obj.eq_time,EQ_obj.eq_focaldepth,EQ_obj.eq_magnitude,EQ_obj.eq_focallongitude,EQ_obj.eq_focallatitude,EQ_obj.eq_epicentralintensity,EQ_obj.eq_location,EQ_obj.eq_remark)
	return HttpResponse(str1)


#地震选择页面选择地震地图数据接口
def checkEqMap(request):
	context = RequestContext(request)
	context_dict = {}
	eqData = []
	if request.method == "POST":
		value = request.POST.get("value","")
		zhi = request.POST.get("zhi","")
		pagenum = request.POST.get("page",1)
		if value == None or value == "":
			EQ_obj = EQInfo.objects.filter()
		else:
			value_new = value + '__icontains'
			args = {value_new:zhi}
			EQ_obj = EQInfo.objects.filter(**args)
			for eq in EQ_obj:
				dic = {}
				dic["eqId"] = eq.eq_earthquakeid
				dic["eqName"] = eq.eq_earthquakename
				dic["eqTime"] = "%s:%s" % (eq.eq_date,eq.eq_time)
				dic["eqDepth"] = eq.eq_focaldepth
				dic["eqLiedu"] = eq.eq_epicentralintensity
				dic["eqLocation"] = eq.eq_location
				dic["eqLongitude"] = eq.eq_focallongitude
				dic["eqLatitude"] = eq.eq_focallatitude
				dic["eqMagnitude"] = eq.eq_magnitude
				eqData.append(dic)
	leng = EQ_obj.count()
	if leng*10/10-((leng/10)*10)>0:
		pageleng = leng/10+1
	else:
		pageleng = leng/10
	if pagenum == 1:
		return HttpResponse(json.dumps(eqData[0:10])+"pageleng:"+str(pageleng)+"nowpage:"+str(pagenum))
	else:
		pagepre = (int(pagenum)-1)*10
		pagenex = (int(pagenum))*10
		return HttpResponse(json.dumps(eqData[pagepre:pagenex])+"pageleng:"+str(pageleng)+"nowpage:"+str(pagenum))



def checkup2(request):
	context = RequestContext(request)
	context_dict = {}
	if request.session.get("user_id"):
		if settings.DEBUG == True:
			print request.session.get("user_id")#用户编号
		else:
			pass
	else:
		return HttpResponseRedirect('/t')
	if request.session.get("EQid"):
		if settings.DEBUG == True:
			print request.session.get("EQid")#地震编号
		else:
			pass
	else:
		return HttpResponseRedirect('/t/checkup')
	structObj = building_structure.objects.all()
	context_dict["structObj"] = structObj
	if request.method == "GET":
		if settings.DEBUG == True:
			print "enter checkup2 get"
		else:
			pass
		try:
			if settings.DEBUG == True:
				print request.session.get("structtype")
			else:
				pass
			context_dict["structtype"] = request.session.get("structtype")
			if settings.DEBUG == True:
				print "$"*60,context_dict["structtype"]
			else:
				pass
			return render_to_response('transport/checkup2.html',context_dict,context)
		except:
			if settings.DEBUG == True:
				print "no structtype value"
			else:
				pass
		return render_to_response('transport/checkup2.html',context_dict,context)
	else:
		if settings.DEBUG == True:
			print "enter checkup2 post"
		else:
			pass
		note = request.POST.get("name")
		if settings.DEBUG == True:
			print note,"#"*60
		else:
			pass
		try:
			if settings.DEBUG == True:
				print "eqid is ",request.session.get("EQid"),"type is ",note
			else:
				pass
		except:
			return HttpResponse('没有选择地震！即将跳转选择地震页面！')
		request.session["structtype"] = note
		if settings.DEBUG == True:
			print note,"I am  note "
		else:
			pass
		try:
			structnameObj = building_structure.objects.get(construct_typeid = note)
			request.session["structtypename"] = structnameObj.construct_typename
			request.session["structtypeid"] = structnameObj.id
			if settings.DEBUG == True:
				print structnameObj.construct_typename,structnameObj.id
			else:
				pass
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
		if settings.DEBUG == True:
			print "no user id "
		else:
			pass
		return HttpResponseRedirect('/t')
	if request.session.get("EQid"):
		earthquakeid = request.session.get("EQid")#地震编号
	else:
		if settings.DEBUG == True:
			print "no eq id "
		else:
			pass
		return HttpResponseRedirect('/t/checkup')
	if request.session.get("structtypename"):
		context_dict["structtypename"] = request.session.get("structtypename")#地震编号
	else:
		if settings.DEBUG == True:
			print "no structname "
		else:
			pass
		return HttpResponseRedirect('/t/checkup2')
	if request.session.get("structtype"):
		structtype = request.session.get("structtype")#地震编号
	else:
		if settings.DEBUG == True:
			print "no structtype "
		else:
			pass
		return HttpResponseRedirect('/t/checkup2')
	if request.method == "GET":
		if settings.DEBUG == True:
			print "enter checkup3 get"
		else:
			pass
		try:#测试有无建筑物信息
			buidObj = building_information_tem.objects.filter(building_constructtypeid__construct_typeid = structtype,building_userid__user_id=userid,building_earthquakeid__eq_earthquakeid=earthquakeid)[0]
			# buidObj = building_information_tem.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
			if settings.DEBUG == True:
				print "*"*60
			else:
				pass
			if settings.DEBUG == True:
				print buidObj
			else:
				pass
			if settings.DEBUG == True:
				print structtype,userid,earthquakeid
			else:
				pass
			request.session["building_buildnumber"] = buidObj.building_buildnumber
			if settings.DEBUG == True:
				print "#"*60
			else:
				pass
			context_dict["building"] = buidObj
			return render_to_response('transport/checkup3.html',context_dict,context)
		except:
			# try:#如果存在建筑物的话算式编辑建筑物
			# 	buidObj = building_information.objects.filter(building_buildnumber = request.session.get("building_buildnumber"))[0]
			# 	# buidObj = building_information_tem.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
			# 	if settings.DEBUG == True:
			# 		print "*"*60
			# 	else:
			# 		pass
			# 	if settings.DEBUG == True:
			# 		print buidObj
			# 	else:
			# 		pass
			# 	if settings.DEBUG == True:
			# 		print structtype,userid,earthquakeid
			# 	else:
			# 		pass
			# 	if settings.DEBUG == True:
			# 		print "#"*60
			# 	else:
			# 		pass
			# 	context_dict["building"] = buidObj
			# 	return render_to_response('transport/checkup3.html',context_dict,context)
			# except:
				#没有建筑物信息时，新生成一个建筑物id
			if settings.DEBUG == True:
				print "no building_information value"
			else:
				pass
			date1 = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))#鉴定日期为当前系统时间的格式化如20141113
			buidatedate = time.strftime('%Y',time.localtime(time.time()))
			#查询当天插入数据库中的建筑物信息条数
			count = building_information.objects.filter(building_constructtypeid__construct_typeid = structtype,building_userid__user_id=userid,building_earthquakeid__eq_earthquakeid=earthquakeid,building_createdate__year=buidatedate).count()
			count = '%04d' % (count)
			if settings.DEBUG == True:
				print count,"*"*20
			else:
				pass
			# building_informations={}#生成一个字典，目的是与有建筑物时相统一
			# building_informations["building_buildnumber"] = structtype+userid+earthquakeid+date1+count
			try:
				buidObj = building_information.objects.order_by('-building_createtime').filter(building_constructtypeid__construct_typeid = structtype,building_userid__user_id=userid,building_earthquakeid__eq_earthquakeid=earthquakeid)[0]
				if settings.DEBUG == True:
					print "%"*60
				else:
					pass
				context_dict["building"] = buidObj
			except:
				if settings.DEBUG == True:
					print "no build_information value in database!"
				else:
					pass
			context_dict["number"]= earthquakeid+structtype+userid+date1+count
			return render_to_response('transport/checkup3.html',context_dict,context)
	else:
		try:
			if settings.DEBUG == True:
				print "eqid is ",earthquakeid,"type is ",structtype
			else:
				pass
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
			if request.POST.get("jd",0) != "0.0":
				try:
					jd = float(request.POST.get("jd",0))
					jf = float(request.POST.get("jf",0))
					jm = float(request.POST.get("jm",0))
					wd = float(request.POST.get("wd",0))
					wf = float(request.POST.get("wf",0))
					wm = float(request.POST.get("wm",0))
					jdz = jd + float(jf)/60 + float(jm)/3600
					wdz = wd + float(wf)/60 + float(wm)/3600
					builddict["building_longitude"] = '%.6f'%jdz
					builddict["building_latitude"] = '%.6f'%wdz
				except Exception,e:
					if settings.DEBUG == True:
						print "error",e
					else:
						pass
			else:
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
			if settings.DEBUG == True:
				print "ready to save tem building"
			else:
				pass
			try:#检测是否有建筑物信息，如果有说明此次是修改而不是新建
				buidObj = building_information.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
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
					if settings.DEBUG == True:
						print "modify success"
					else:
						pass
				except:
					return HttpResponseRedirect('/t/checkup3')
			except:#没有建筑物信息时说明是新建或者是修改临时建筑物信息
				try:#检测是否有临时建筑物信息，如果有说明此次是修改而不是新建
					if settings.DEBUG == True:
						print "modify buildinformation start"
					else:
						pass
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
						if settings.DEBUG == True:
							print "modify success"
						else:
							pass
					except:
						return HttpResponseRedirect('/t/checkup3')
				except:
					try:
						construct = building_structure.objects.get(id = builddict["building_constructtypeid"])
						usage = building_usage.objects.get(id = builddict["building_buildusage"])
						areanumber = region.objects.get(Q(region_location__startswith = builddict["building_areanumber"]))
						earthquake = EQInfo.objects.get(id = builddict["building_earthquakeid"])
						try:
							user = sys_user.objects.get(id = builddict["building_userid"])
						except:
							user = sys_user.objects.get(id = 83)
						if settings.DEBUG == True:
							print "foreignkey get success"
						else:
							pass
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
						if settings.DEBUG == True:
							print "tem_buiding init over"*10
						else:
							pass
						request.session["buildareanumber"] = builddict["building_constructtypeid"]
						# myBuild = building_information(**build)
						#为了保证保存时，保存完一个表另一个表出现故障，要对以保存的表进行删除操作，如保存环境信息时出现错误，要对刚保存的建筑物数据删除
						mybuild.save()
						if settings.DEBUG == True:
							print "tem_buiding save over"*10
						else:
							pass
					except:
						HttpResponse("建筑物信息有误！请核对后再保存！")
		except:
			if settings.DEBUG == True:
				print "no value"
			else:
				pass
		if settings.DEBUG == True:
			print request.POST.get("build_areanumber"),"#"*60
		else:
			pass

		return HttpResponseRedirect('/t/checkup4')

def editCheckup3(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method == "GET":
		editBuildId = request.GET.get("buildid")
		buildObj = building_information.objects.get(building_buildnumber = editBuildId)
		request.session["structtypename"] = buildObj.building_constructtypeid.construct_typename
		request.session["structtypeid"] = buildObj.building_constructtypeid.id
		request.session["structtype"] = buildObj.building_constructtypeid.construct_typeid
		request.session["EQid"] = buildObj.building_earthquakeid.eq_earthquakeid
		request.session["EQID"] = buildObj.building_earthquakeid.id
		context_dict["building"] = buildObj
		request.session["building_buildnumber"] = buildObj.building_buildnumber
		useageObj = building_usage.objects.all()
		context_dict["useageObj"] = useageObj
		context_dict["useageObjji"] = useageObj[::2]
		regionObj = region.objects.all()
		context_dict["regionObj"] = regionObj
		context_dict["structtypename"] = request.session.get("structtypename")#地震编号
	return render_to_response('transport/checkup3.html',context_dict,context)



def checkup4(request):
	context = RequestContext(request)
	context_dict = {}
	context_dict["foundation_status"] = foundation_status.objects.all()
	context_dict["field_effect"] = field_effect.objects.all()
	if request.session.get("user_id"):
		userid = request.session.get("user_id")#用户编号
	else:
		if settings.DEBUG == True:
			print "no user id "
		else:
			pass
		return HttpResponseRedirect('/t')
	if request.session.get("EQid"):
		earthquakeid = request.session.get("EQid")#地震编号
	else:
		if settings.DEBUG == True:
			print "no eq id "
		else:
			pass
		return HttpResponseRedirect('/t/checkup')
	if request.session.get("structtypename"):
		context_dict["structtypename"] = request.session.get("structtypename")#地震编号
	else:
		if settings.DEBUG == True:
			print "no structname "
		else:
			pass
		return HttpResponseRedirect('/t/checkup2')
	if request.session.get("structtype"):
		structtype = request.session.get("structtype")#地震编号
	else:
		if settings.DEBUG == True:
			print "no structtype "
		else:
			pass
		return HttpResponseRedirect('/t/checkup2')
	try:
		b = building_information_tem.objects.get(building_buildnumber = request.session.get("building_buildnumber"))#建筑物实例
	except:
		try:
			b = building_information.objects.get(building_buildnumber = request.session.get("building_buildnumber"))#建筑物实例
		except:
			return HttpResponseRedirect('/t/checkup3')
	if request.method == "GET":
		if settings.DEBUG == True:
			print "enter checkup4 GET"
		else:
			pass
		try:#如果存在环境信息则说明是编辑建筑物。
			environmentObj = environment.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
			context_dict["building_environment"] = environmentObj
			# environmentObj = environment_tem.objects.get(environment_buildnumber__building_userid__user_id = request.session.get('user_id'))
		except:
			try:#不是编辑建筑物的情况下查看是否有缓存的建筑物环境信息
				environmentObj = environment_tem.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
				context_dict["building_environment"] = environmentObj
			except: 
				if settings.DEBUG == True:
					print "tem_environment has no value！"
				else:
					pass
				try:
					environmentObj = environment.objects.filter(environment_buildnumber__building_userid__user_id = request.session.get('user_id'))[0]
					context_dict["building_environment"] = environmentObj
					if settings.DEBUG == True:
						print "get enviroment in database success"
					else:
						pass
				except:
					if settings.DEBUG == True:
						print "database has no environment value"
					else:
						pass
					return render_to_response('transport/checkup4.html',context_dict,context)
		cdyx = environmentObj.environment_earthquakeeff.split(",")
		djzk = environmentObj.environment_foundation.split(",")
		if "CDYXQT" in environmentObj.environment_earthquakeeff:
			context_dict["cdyxqita"] = ((cdyx[-1])[3:-2]).decode('unicode_escape')
		if "DJZKQT" in environmentObj.environment_foundation:
			context_dict["djzkqita"] = ((djzk[-1])[3:-2]).decode('unicode_escape')
		return render_to_response('transport/checkup4.html',context_dict,context)
	else:
		if settings.DEBUG == True:
			print "enter checkup4 POST"
		else:
			pass
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
		if settings.DEBUG == True:
			print "get enviroment post info success"
		else:
			pass
		try:#判断是否是修改环境信息
			environmentObj = environment.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
			try:
				environmentObj.environment_earthquakeeff = environment1["environment_earthquakeeff"]
				environmentObj.environment_foundation = environment1["environment_foundation"]
				environmentObj.environment_adjoinbuild = environment1["environment_adjoinbuild"]
				environmentObj.environment_seismicintensity = environment1["environment_seismicintensity"]
				environmentObj.environment_smallaffect = environment1["environment_smallaffect"]
				environmentObj.environment_bigaffect = environment1["environment_bigaffect"]
				environmentObj.save()
				if settings.DEBUG == True:
					print "modify tem environment over"
				else:
					pass
			except:
				if settings.DEBUG == True:
					print "modify tem environment failed"
				else:
					pass
				return HttpResponseRedirect('/t/checkup4')
		except:
			try:
				#判断是否是修改环境信息
				# environmentObj = environment_tem.objects.get(environment_buildnumber__building_userid__user_id = request.session.get('user_id'))
				environmentObj = environment_tem.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
				if settings.DEBUG == True:
					print "modify tem environment start"
				else:
					pass
				try:
					environmentObj.environment_earthquakeeff = environment1["environment_earthquakeeff"]
					environmentObj.environment_foundation = environment1["environment_foundation"]
					environmentObj.environment_adjoinbuild = environment1["environment_adjoinbuild"]
					environmentObj.environment_seismicintensity = environment1["environment_seismicintensity"]
					environmentObj.environment_smallaffect = environment1["environment_smallaffect"]
					environmentObj.environment_bigaffect = environment1["environment_bigaffect"]
					environmentObj.save()
					if settings.DEBUG == True:
						print "modify tem environment over"
					else:
						pass
				except:
					if settings.DEBUG == True:
						print "modify tem environment failed"
					else:
						pass
					return HttpResponseRedirect('/t/checkup4')
			except: 
				if settings.DEBUG == True:
					print "tem_environment has no value！"
				else:
					pass
				try:
					b = building_information_tem.objects.get(building_buildnumber = request.session.get("building_buildnumber"))#建筑物实例
					if settings.DEBUG == True:
						print "get tem buildinfo success"
					else:
						pass
					if settings.DEBUG == True:
						print b
					else:
						pass
				except:
					if settings.DEBUG == True:
						print "no tem buildinginfo"
					else:
						pass
				try:
					if settings.DEBUG == True:
						print "tem environment save start"
					else:
						pass
					myenvironment = environment_tem(environment_buildnumber = b,**environment1)
					if settings.DEBUG == True:
						print "****************"
					else:
						pass
					myenvironment.save()
					if settings.DEBUG == True:
						print "tem environment save over"
					else:
						pass
				except:
					if settings.DEBUG == True:
						print "save environment failed"
					else:
						pass
		return HttpResponseRedirect('/t/checkup5')
def checkup5(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method == "GET":
		if settings.DEBUG == True:
			print "enter checkup5 GET"
		else:
			pass
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
			context_dict["buidObj"] = buidObj
			if settings.DEBUG == True:
				print "*"*60
			else:
				pass
		except:
			try:
				buidObj = building_information.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
				context_dict["buidObj"] = buidObj
				if settings.DEBUG == True:
					print "*"*60
				else:
					pass
			except:
				return HttpResponseRedirect('/t/checkup3')
		try:
			# environmentObj = environment_tem.objects.get(environment_buildnumber__building_userid__user_id = request.session.get('user_id'))
			environmentObj = environment_tem.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
		except:
			try:
				environmentObj = environment.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
			except:
				return HttpResponseRedirect('/t/checkup4')
		try:
			if settings.DEBUG == True:
				print "n1"
			else:
				pass
			sublocalObj = sublocal.objects.filter(sublocal_constructtypeid__construct_typeid = structtype)#查询出所有的细部震损信息
			locationObj = buildlocation.objects.filter(location_constructtype__construct_typeid = structtype)#查询出所有部位信息
			catalogObj = SubLocationCatalog.objects.filter(catalog_constructtypeid__construct_typeid = structtype)#查询出所有的细部分类信息
		except:
			if settings.DEBUG == True:
				print "no value sublocalObj"
			else:
				pass
		try:
			context_dict["sublocalObj"] = sublocalObj
			context_dict["locationObj"] = locationObj
			context_dict["catalogObj"] = catalogObj
			context_dict["struct"] = sublocalObj[0].sublocal_constructtypeid
		except:
			return HttpResponseRedirect('/t/checkup')
		try:
			buidObj = building_information_tem.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
			buildnum = buidObj.building_buildnumber
			if settings.DEBUG == True:
				print str("Build id is："),buildnum
			else:
				pass
			dataObj = damage_tem.objects.filter(damage_id = buildnum).order_by('id')
			if settings.DEBUG == True:
				print "here"
			else:
				pass
			for x in dataObj:
				if settings.DEBUG == True:
					print str(x.damage_locationid).decode('utf8')
				else:
					pass
			try:
				damageCacheObj = damage_cache_tem.objects.get(damage_buildnumber__building_buildnumber = buildnum)
				context_dict["damageCache"] = damageCacheObj
			except:
				pass
			context_dict["dama_data"] = dataObj
		except:
			try:
				buidObj = building_information.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
				buildnum = buidObj.building_buildnumber
				if settings.DEBUG == True:
					print str("Build id is："),buildnum
				else:
					pass
				dataObj = damage.objects.filter(damage_id = buildnum).order_by('id')
				if settings.DEBUG == True:
					print "here_edit"
				else:
					pass
				for x in dataObj:
					if settings.DEBUG == True:
						print str(x.damage_locationid).decode('utf8')
					else:
						pass
				try:
					damageCacheObj = damage_cache.objects.get(damage_buildnumber__building_buildnumber = buildnum)
					context_dict["damageCache"] = damageCacheObj
				except:
					pass
				context_dict["dama_data"] = dataObj
			except Exception,e:
				if settings.DEBUG == True:
					print "damage has no dama_data value_edit",e
				else:
					pass
		context_dict["buildObj"] = buidObj
		context_dict["buildFrontImg"] = buildFrontImage.objects.filter(buildid = buildnum)
		context_dict["buildBackImg"] = buildBackImage.objects.filter(buildid = buildnum)
		context_dict["buildFloorImg"] = buildFloorImage.objects.filter(buildid = buildnum)
		context_dict["buildSideImg"] = buildSideImage.objects.filter(buildid = buildnum)
		context_dict["img"] = "show"
		return render_to_response('transport/checkup5.html',context_dict,context)
	else:
		if settings.DEBUG == True:
			print "enter checkup5 post"
		else:
			pass
		quakedata = request.POST.get("name")
		damageCacheData = request.POST.get("cache")
		try:
			data = quakedata.split("*")
			data_list = []
		except:
			if settings.DEBUG == True:
				print "ss"
			else:
				pass
		try:
			for x in data:
				data_item = eval(x)
				data_list.append(data_item)
				if settings.DEBUG == True:
					print data_item["damage_isfirst"]
				else:
					pass
		except:
			if settings.DEBUG == True:
				print "mei de shi ni a "
			else:
				pass
		try:
			buidObj_tem = building_information_tem.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
		except:
			try:
				buidObj_tem = building_information.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
			except:
				return HttpResponse("未提交建筑物信息！")
		try:
			# environmentObj = environment_tem.objects.get(environment_buildnumber__building_userid__user_id = request.session.get('user_id'))
			environmentObj_tem = environment_tem.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
		except: 
			try:
				environmentObj_tem = environment.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
			except:
				return HttpResponse("未提交环境信息！")
		try:
			if settings.DEBUG == True:
				print "test the building_buildnumber exist"
			else:
				pass
			try:
				buidObj_exist = building_information.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
				buidObj_exist.delete()
				if settings.DEBUG == True:
					print "building_information zhong  build yi shan chu   "
				else:
					pass
			except:
				if settings.DEBUG == True:
					print "building_information zhong  mei  you  gai build   "
				else:
					pass
			if settings.DEBUG == True:
				print "save build_information start"
			else:
				pass
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
			if settings.DEBUG == True:
				print "build has saved"
			else:
				pass
		except:
			return HttpResponse("未能保存建筑物信息！")
		try:
			if settings.DEBUG == True:
				print "test the environment exist"
			else:
				pass
			try:
				envi_exist = environment.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
				envi_exist.delete()
				if settings.DEBUG == True:
					print "delete environment success"
				else:
					pass
			except:
				if settings.DEBUG == True:
					print "environment zhong  wu ci environment_info"
				else:
					pass
			if settings.DEBUG == True:
				print "save environment start"
			else:
				pass
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
			if settings.DEBUG == True:
				print "environment has saved"
			else:
				pass
		except:
			#保存环境信息出错需要删除已保存的建筑物信息
			try:#按理说没必要这样做，但是为了保险，还是try下吧
				mybuild_info = building_information.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
				mybuild_info.delete()
			except:
				if settings.DEBUG == True:
					print "bao cun huangjing shi bai,qie shan chu build shibai"
				else:
					pass
				return HttpResponse("没有要删除的编号为"+request.session.get('building_buildnumber')+"的建筑物信息！")
			# return HttpResponse("未能保存环境信息！")
		try:
			#数据都保存到了正式表中，需要将临时表中数据删除
			if settings.DEBUG == True:
				print "delete tem environment start"
			else:
				pass
			try:
				environmentObj_tem = environment_tem.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
				environmentObj_tem.delete()
			except:
				pass
			if settings.DEBUG == True:
				print "tem environment delete success"
			else:
				pass
		except:
			mybuild_info = building_information.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
			mybuild_info.delete()
			environment_info = environment.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
			environment_info.delete()
			return HttpResponse("系统错误2！")
		try:
			#数据都保存到了正式表中，需要将临时表中数据删除
			if settings.DEBUG == True:
				print "delete tem build start"
			else:
				pass
			
			if settings.DEBUG == True:
				print buidObj_tem.building_buildnumber,"#"*20
			else:
				pass
			try:
				buidObj_tem = building_information_tem.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
				buidObj_tem.delete()
			except:
				pass
			if settings.DEBUG == True:
				print "tem build delete success"
			else:
				pass
				# return HttpResponse("临时表中没有要删除的编号为"+request.session.get('building_buildnumber')+"的建筑物信息！")
		except:
			if settings.DEBUG == True:
				print "error",request.session.get('building_buildnumber')
			else:
				pass
			# mybuild_info = building_information.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
			# mybuild_info.delete()
			# environment_info = environment.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
			# environment_info.delete()
			# return HttpResponse("系统错误1,请重新提交!")
		try:
			if settings.DEBUG == True:
				print "进入震损数据存储阶段".decode('utf8')
			else:
				pass
			try:
				b = building_information.objects.get(building_buildnumber = request.session.get("building_buildnumber"))
			except:
				HttpResponse("没有建筑物编号为"+request.session.get('building_buildnumber')+"的建筑物信息！")
			# try:
			# 	construct = building_structure.objects.get(id = request.session.get("structtypeid"))
			# except:
			# 	HttpResponse("没有结构类型编号为"+request.session.get("structtypeid")+"的结构类型信息！")
			damageObj = damage_tem.objects.filter(damage_id = request.session.get("building_buildnumber"))
			if damageObj:
				if settings.DEBUG == True:
					print "临时震损信息表中值,开始删除".decode('utf8')
				else:
					pass
				damageObj.delete()
				if settings.DEBUG == True:
					print "删除成功".decode('utf8')
				else:
					pass
			try:
				damageCacheObj = damage_cache_tem.objects.get(damage_buildnumber__building_buildnumber = request.session.get("building_buildnumber"))
				damageCacheObj.delete()
			except:
				pass
			damageObj = damage.objects.filter(damage_id = request.session.get("building_buildnumber"))
			if damageObj:
				if settings.DEBUG == True:
					print "临时震损信息表中值,开始删除".decode('utf8')
				else:
					pass
				damageObj.delete()
				if settings.DEBUG == True:
					print "删除成功".decode('utf8')
				else:
					pass
			try:
				damageCacheObj = damage_cache.objects.get(damage_buildnumber__building_buildnumber = request.session.get("building_buildnumber"))
				damageCacheObj.delete()
			except:
				pass
			buid = request.session.get('building_buildnumber')
			if settings.DEBUG == True:
				print "开始存储震损数据".decode('utf8')
			else:
				pass
			for xx in data_list:
				local = xx["damage_locationid"]
				catalog = xx["damage_catalogid"]
				sub = xx["damage_sublocationid"]
				# localObj = buildlocation.objects.get(id = local)
				# catalogObj = SubLocationCatalog.objects.get(id = catalog)
				# sub = sublocal.objects.get(id = sub)
				cursor = connection.cursor()            #获得一个游标(cursor)对象
				sqlstring = 'insert into transport_damage (damage_id,damage_buildnumber_id,damage_constructtypeid_id,damage_locationid_id,damage_catalogid_id,damage_sublocationid_id,damage_number,damage_degree,damage_parameteradjust,damage_description,damage_isfirst) values("%s",%d,%d,%d,%d,%d,"%s","%s",%f,"%s","%s")' %(buid,b.id,request.session.get("structtypeid"),local,catalog,sub,xx["damage_number"],xx["damage_degree"],float(xx["damage_parameteradjust"]),xx["damage_description"],xx["damage_isfirst"])
				cursor.execute(sqlstring)    #执行sql语句
				# myitem = damage(
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
				if settings.DEBUG == True:
					print "saved + 1"
				else:
					pass
		except:
			HttpResponse("震损信息有误！请核对后再保存！")
		if settings.DEBUG == True:
			print "**"*30
		else:
			pass
		b = building_information.objects.get(building_buildnumber = request.session.get("building_buildnumber"))
		damageCacheObj = damage_cache(
			damage_buildnumber = b,
			damage_cache = damageCacheData,
			)
		damageCacheObj.save()

		if settings.DEBUG == True:
			print b.building_buildnumber
		else:
			pass
		
		try:
			configObj = paramconfig.objects.filter(areanumber__region_number = request.session.get("buildareanumber"),constructtypeid__construct_typename = request.session.get("structtypename"))[0]
			alpha = configObj.sysparaalpha
			beta = configObj.sysparabeta
			gamma = configObj.sysparagamma
			damageData = []
			abr = {}
			abr["alpha"] = alpha
			abr["beta"] = beta
			abr["gamma"] = gamma
			damageData.append(abr)
			configId = configObj.id
			for xx in data_list:
				dama = {}
				local = xx["damage_locationid"]
				sub = xx["damage_sublocationid"]
				paramObj = paramsubcon.objects.filter(configid__id = configId,sublocationid__id = sub)[0]
				if xx["damage_number"] == "0" and xx["damage_degree"] == "0":
					paramValue = paramObj.leve11value
				elif xx["damage_number"] == "0" and xx["damage_degree"] == "1":
					paramValue = paramObj.leve12value
				elif xx["damage_number"] == "0" and xx["damage_degree"] == "2":
					paramValue = paramObj.leve13value
				elif xx["damage_number"] == "1" and xx["damage_degree"] == "0":
					paramValue = paramObj.leve21value
				elif xx["damage_number"] == "1" and xx["damage_degree"] == "1":
					paramValue = paramObj.leve22value
				elif xx["damage_number"] == "1" and xx["damage_degree"] == "2":
					paramValue = paramObj.leve23value
				elif xx["damage_number"] == "2" and xx["damage_degree"] == "0":
					paramValue = paramObj.leve31value
				elif xx["damage_number"] == "2" and xx["damage_degree"] == "1":
					paramValue = paramObj.leve32value
				elif xx["damage_number"] == "2" and xx["damage_degree"] == "2":
					paramValue = paramObj.leve33value
				else:
					paramValue = 0.0
				paramAdjust = xx["damage_parameteradjust"]
				paramloconObj = paramlocon.objects.filter(configid__id = configId,locationid__id = local)[0]
				paramQ = paramloconObj.paravalue
				loc = paramloconObj.locationid.id
				dama["adjust"] = paramAdjust
				dama["value"] = paramValue
				dama["q"] = paramQ
				dama["loc"] = loc
				damageData.append(dama)
			try:
				if settings.DEBUG == True:
					print damageData
				else:
					pass
				res = postdata(damageData)
			except:
				if settings.DEBUG == True:
					print "result interface is not available"
				else:
					pass
				res = 0.25
		except Exception,e:
			if settings.DEBUG == True:
				print "error",e
			else:
				pass
			res = 0.25
		if settings.DEBUG == True:
			print "enter post"
		else:
			pass
		
		result = identify_result(
			result_buildnumber = b,
			result_id = "result",
			result_securitycategory = "安全",
			result_totaldamageindex = res,
			result_damagedegree = "基本完好",
			)
		result.save()
	return HttpResponse("success")

def check5save(request):
	if settings.DEBUG == True:
		print "enter checkup5save method"
	else:
		pass
	quakedata = request.POST.get("name")
	damageCacheData = request.POST.get("cache")
	data = quakedata.split("*")
	data_list = []
	try:
		b = building_information_tem.objects.get(building_buildnumber = request.session.get("building_buildnumber"))
	except:
		if settings.DEBUG == True:
			print "木有临时建筑了，".decode('utf8')
		else:
			pass
	try:
		for x in data:
			data_item = eval(x)
			data_list.append(data_item)
			if settings.DEBUG == True:
				print data_item["damage_isfirst"]
			else:
				pass
	except:
		if settings.DEBUG == True:
			print "here "
		else:
			pass
	# try:
	if settings.DEBUG == True:
		print request.session.get("building_buildnumber")
	else:
		pass
	try:
		b = building_information_tem.objects.get(building_buildnumber = request.session.get("building_buildnumber"))
		if settings.DEBUG == True:
			print request.session.get("structtypeid")
		else:
			pass
		try:
			damageCacheObj = damage_cache_tem.objects.get(damage_buildnumber__building_buildnumber = b.building_buildnumber)
			damageCacheObj.damage_cache = damageCacheData
			damageCacheObj.save()
		except:
			damageCacheObj = damage_cache_tem(
				damage_buildnumber = b,
				damage_cache = damageCacheData,
				)
			damageCacheObj.save()
		construct = building_structure.objects.get(id = request.session.get("structtypeid"))
		if settings.DEBUG == True:
			print construct
		else:
			pass
		damageObj = damage_tem.objects.filter(damage_id = request.session.get("building_buildnumber"))
		if damageObj:
			if settings.DEBUG == True:
				print "有值".decode('utf8')
			else:
				pass
			damageObj.delete()
			if settings.DEBUG == True:
				print "删除成功".decode('utf8')
			else:
				pass
		for xx in data_list:
			local = xx["damage_locationid"]
			catalog = xx["damage_catalogid"]
			sub = xx["damage_sublocationid"]
			cursor = connection.cursor()            #获得一个游标(cursor)对象
			sqlstring = 'insert into transport_damage_tem (damage_id,damage_buildnumber_id,damage_constructtypeid_id,damage_locationid_id,damage_catalogid_id,damage_sublocationid_id,damage_number,damage_degree,damage_parameteradjust,damage_description,damage_isfirst) values("%s",%d,%d,%d,%d,%d,"%s","%s",%f,"%s","%s")' %(request.session.get('building_buildnumber'),b.id,request.session.get("structtypeid"),local,catalog,sub,xx["damage_number"],xx["damage_degree"],float(xx["damage_parameteradjust"]),xx["damage_description"],xx["damage_isfirst"])
			cursor.execute(sqlstring)    #执行sql语句
			if settings.DEBUG == True:
				print "saved + 1"   
			else:
				pass
		if settings.DEBUG == True:
			print "**"*30
		else:
			pass
		return HttpResponse("success")
	except:
		#如果临时建筑物表中没有此buidingid的建筑物，则说明已经完成鉴定的存储，是跳转checkup6的
		return HttpResponse("over")

def checkup6(request):
	context = RequestContext(request)
	context_dict = {}
	if settings.DEBUG == True:
			print "enter checkup6 GET"
	else:
		pass
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
	except:
		try:
			buidObj = building_information.objects.get(building_buildnumber = request.session.get('building_buildnumber'))
		except:
			return HttpResponseRedirect('/t/checkup3')
	try:
			# environmentObj = environment_tem.objects.get(environment_buildnumber__building_userid__user_id = request.session.get('user_id'))
			environmentObj = environment_tem.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
	except:
		try:
			environmentObj = environment.objects.get(environment_buildnumber__building_buildnumber = request.session.get('building_buildnumber'))
		except:
			return HttpResponseRedirect('/t/checkup4')
	try:
		identify_resultObj = identify_result.objects.get(result_buildnumber__building_buildnumber = request.session.get("building_buildnumber"))
	except:
		return HttpResponseRedirect('/t/checkup5')
	try:
		context_dict["structtypename"] = request.session.get("structtypename")
		structtype = request.session.get("structtype")#获取结构类型编号
	except:
		return HttpResponseRedirect('/t/checkup2')
	# resultObj = identify_result.objects.get(result_buildnumber__building_buildnumber = request.session.get("building_buildnumber"))
	context_dict["resultObj"] = identify_resultObj
	return render_to_response('transport/checkup6.html',context_dict,context)


#统计页面
def count(request):
	context = RequestContext(request)
	context_dict = {}
	sqlstring = "SELECT DISTINCT a.building_buildnumber,e.eq_earthquakename,b.result_securitycategory,b.result_totaldamageindex,a.building_admregioncode,a.building_buildname,a.building_province,a.building_househostname,f.construct_typename,a.building_buildyear,(case a.building_fortificationinfo when '1' then '未经抗震设防' else '抗震设防' end) as building_fortificationinfo,(case building_fortificationdegree  when 6 then '6度设防'	when 7 then '7度设防' when 8 then '8度设防'	WHEN 9 then '9度设防' when 10 then '采用非正规抗震措施' else '未设防' end) as building_fortificationdegree,e.eq_epicentralintensity,DATE_FORMAT( b.result_assetdate,'%Y-%m-%d'),a.building_longitude,a.building_latitude,a.building_buildarea,a.building_uplayernum,d.building_usagename,c.user_id,c.user_realname,c.user_title,c.user_workunit,b.result_damagedegree from transport_building_information a ,transport_identify_result b,transport_sys_user c,transport_building_usage d,transport_eqinfo e,transport_building_structure f where c.user_id = '"+request.session.get("user_id")+"' and b.result_buildnumber_id = a.id and a.building_userid_id = c.id and a.building_buildusage_id = d.id and a.building_earthquakeid_id = e.id and f.id = a.building_constructtypeid_id  ORDER BY -a.buidling_updatetime"
	# if request.method == "GET":
		# qstring = request.GET.get("qstring1","")
		# # if qstring == "":
		# # 	resultObj = identify_result.objects.filter().order_by("-result_assetdate")
		# # else:
		# if settings.DEBUG == True:
		# 	print "#"*30
		# else:
		# 	pass
		# if settings.DEBUG == True:
		# 	print qstring
		# else:
		# 	pass
		# # qstring = qstring.replace("@@@","%")
		# sqlstring = sqlstring +qstring+") ORDER BY -a.buidling_updatetime"
		# if settings.DEBUG == True:
		# 	print sqlstring
		# else:
		# 	pass
	cursor = connection.cursor()            #获得一个游标(cursor)对象
	cursor.execute(sqlstring)
	if settings.DEBUG == True:
		print sqlstring
	else:
		pass
	resultObj = cursor.fetchall() 
	if settings.DEBUG == True:
		print "*"*50
	else:
		pass
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
	earthObj = EQInfo.objects.all().values('eq_earthquakename').distinct()
	context_dict["earthquake"] = earthObj
	return render_to_response('transport/count.html',context_dict,context)

def countAjax(request):
	context = RequestContext(request)
	context_dict = {}
	if settings.DEBUG == True:
		print "enter countAjax"
	else:
		pass
	pagenum = request.POST.get("page",1)
	sqlstring = "SELECT DISTINCT a.building_buildnumber,e.eq_earthquakename,b.result_securitycategory,b.result_totaldamageindex,a.building_admregioncode,a.building_buildname,a.building_province,a.building_househostname,f.construct_typename,a.building_buildyear,(case a.building_fortificationinfo when '1' then '未经抗震设防' else '抗震设防' end) as building_fortificationinfo,(case building_fortificationdegree  when 6 then '6度设防'	when 7 then '7度设防' when 8 then '8度设防'	WHEN 9 then '9度设防' when 10 then '采用非正规抗震措施' else '未设防' end) as building_fortificationdegree,e.eq_epicentralintensity,CAST(date_format(result_assetdate,'%Y-%m-%d') as char),a.building_longitude,a.building_latitude,a.building_buildarea,a.building_uplayernum,d.building_usagename,c.user_id,c.user_realname,c.user_title,c.user_workunit,b.result_damagedegree from transport_building_information a ,transport_identify_result b,transport_sys_user c,transport_building_usage d,transport_eqinfo e,transport_building_structure f where c.user_id = '"+request.session.get("user_id")+"' and b.result_buildnumber_id = a.id and a.building_userid_id = c.id and a.building_buildusage_id = d.id and a.building_earthquakeid_id = e.id and f.id = a.building_constructtypeid_id "
	if request.method == "POST":
		qstring = request.POST.get("qstring1","")
		
		if qstring == "":
			resultObj = identify_result.objects.filter()
		else:
			if settings.DEBUG == True:
				print "#"*30
			else:
				pass
			if settings.DEBUG == True:
				print qstring
			else:
				pass
			# qstring = qstring.replace("@@@","%")
			sqlstring = sqlstring +qstring+") ORDER BY -a.buidling_updatetime"
			if settings.DEBUG == True:
				print sqlstring
			else:
				pass
		cursor = connection.cursor()            #获得一个游标(cursor)对象
		cursor.execute(sqlstring)
		if settings.DEBUG == True:
			print sqlstring
		else:
			pass
		resultObj = cursor.fetchall() 
		if settings.DEBUG == True:
			print "*"*50
		else:
			pass
		leng = len(resultObj)
		# pageleng = 1
	if leng*10/10-((leng/10)*10)>0:
		pageleng = leng/10+1
	else:
		pageleng = leng/10
	if settings.DEBUG == True:
		print leng
	else:
		pass
	if settings.DEBUG == True:
		print pageleng
	else:
		pass
	if settings.DEBUG == True:
		print pagenum
	else:
		pass
	if pagenum == 1:
		if settings.DEBUG == True:
			print "here is page 1"
		else:
			pass
		return HttpResponse(json.dumps(resultObj[0:10])+"pageleng:"+str(pageleng)+"nowpage:"+str(pagenum))
	else:
		if settings.DEBUG == True:
			print "bu shi di yi ye "
		else:
			pass
		pagepre = (int(pagenum)-1)*10
		if settings.DEBUG == True:
			print "pagepre is ",pagepre
		else:
			pass
		pagenex = (int(pagenum))*10
		if settings.DEBUG == True:
			print "pagenex is ",pagenex
		else:
			pass
		return HttpResponse(json.dumps(resultObj[pagepre:pagenex])+"pageleng:"+str(pageleng)+"nowpage:"+str(pagenum))

#导出excel
def countExportXls(request):
	context = RequestContext(request)
	context_dict = {}
	if settings.DEBUG == True:
		print "enter countAjax"
	else:
		pass
	try:
		sqlstring = "SELECT DISTINCT a.building_buildnumber,e.eq_earthquakename,b.result_securitycategory,b.result_totaldamageindex,a.building_admregioncode,a.building_buildname,a.building_province,a.building_househostname,f.construct_typename,a.building_buildyear,(case a.building_fortificationinfo when '1' then '未经抗震设防' else '抗震设防' end) as building_fortificationinfo,(case a.building_fortificationdegree  when 6 then '6度设防'	when 7 then '7度设防' when 8 then '8度设防'	WHEN 9 then '9度设防' when 10 then '采用非正规抗震措施' else '未设防' end) as building_fortificationdegree,e.eq_epicentralintensity,CAST(date_format(result_assetdate,'%Y-%m-%d') as char),a.building_longitude,a.building_latitude,a.building_buildarea,a.building_uplayernum,d.building_usagename,c.user_id,c.user_realname,c.user_title,c.user_workunit,b.result_damagedegree from transport_building_information a ,transport_identify_result b,transport_sys_user c,transport_building_usage d,transport_eqinfo e,transport_building_structure f where c.user_id = '"+request.session.get("user_id")+"' and b.result_buildnumber_id = a.id and a.building_userid_id = c.id and a.building_buildusage_id = d.id and a.building_earthquakeid_id = e.id and f.id = a.building_constructtypeid_id "
		qstring = request.GET.get("qstring1","")
		if qstring == "":
			resultObj = identify_result.objects.filter()
		else:
			if settings.DEBUG == True:
				print "#"*30
			else:
				pass
			if settings.DEBUG == True:
				print qstring
			else:
				pass
			# qstring = qstring.replace("@@@","%")
			sqlstring = sqlstring +qstring+") ORDER BY -a.buidling_updatetime"
			if settings.DEBUG == True:
				print sqlstring
			else:
				pass
		cursor = connection.cursor()            #获得一个游标(cursor)对象
		cursor.execute(sqlstring)
		if settings.DEBUG == True:
			print sqlstring
		else:
			pass
		resultObj = cursor.fetchall() 
		response = countExportEls(request,resultObj)
		return response
	except:
		return HttpResponse("error")


#地图数据接口
def countMap(request):
	context = RequestContext(request)
	context_dict = {}
	sqlstring = "select distinct a.building_longitude as longitude,a.building_latitude as latitude,b.result_securitycategory as safe,f.construct_typename as struct ,f.id as icon,a.building_buildyear as years ,concat(a.building_province,a.building_city,a.building_district,a.building_locationdetail) address from transport_building_information a ,transport_identify_result b,transport_sys_user c,transport_building_usage d,transport_eqinfo e,transport_building_structure f where c.user_id = '"+request.session.get("user_id")+"' and b.result_buildnumber_id = a.id  and a.building_earthquakeid_id = e.id and f.id = a.building_constructtypeid_id and c.id = a.building_userid_id  "
	if request.method == "POST":
		qstring = request.POST.get("qstring1","")
		if len(qstring) <15:
			if settings.DEBUG == True:
				print qstring
			else:
				pass
		else:
			qstring = qstring.replace("@@@","%")
			sqlstring = sqlstring +qstring+")"
			if settings.DEBUG == True:
				print sqlstring 
			else:
				pass
	cursor = connection.cursor()            #获得一个游标(cursor)对象
	cursor.execute(sqlstring)
	resultObj = dictfetchall(cursor)
	if settings.DEBUG == True:
		print "%"*60
	else:
		pass
	return HttpResponse(json.dumps(resultObj))
#统计图表接口_sj
def countCharts_sj(request):
	try:
		context = RequestContext(request)
		context_dict = {}
		sj_sqlstring = "select count(*) as '栋数',DATE_FORMAT(building_createdate,'%Y-%m' ) as '月份' from transport_building_information a,transport_identify_result b,transport_building_usage c,transport_sys_user d,transport_building_structure e,transport_eqinfo f where a.building_earthquakeid_id=f.id and a.building_constructtypeid_id=e.id and d.user_id = '"+request.session.get("user_id")+"' and a.building_userid_id = d.id   and a.id = b.result_buildnumber_id and c.id = a.building_buildusage_id  "
		if request.method == "POST":
			qstring = request.POST.get("qstring1","")
			if len(qstring) <15:
				if settings.DEBUG == True:
					print qstring
				else:
					pass
			else:
				sj_sqlstring = sj_sqlstring +qstring
				if settings.DEBUG == True:
					print sj_sqlstring 
				else:
					pass
		cursor = connection.cursor()            #获得一个游标(cursor)对象
		cursor.execute(sj_sqlstring+" GROUP BY DATE_FORMAT(building_createdate,'%Y-%m' )")
		resultObj = sj_fetchall(cursor)
		if settings.DEBUG == True:
			print "%"*60
		else:
			pass
	except Exception,e:
		if settings.DEBUG == True:
			print "error",e
		else:
			pass
	return HttpResponse(json.dumps(resultObj))
#统计图表接口_use
def countCharts_use(request):
	context = RequestContext(request)
	context_dict = {}
	sj_sqlstring = "select sum(a.building_buildarea) as 面积,count(*) as '栋数',case a.building_buildusage_id when 1 then '住宅' when 2 then '政府' WHEN 3 then '商业' when 4 then '站点' when 5 then '工业厂房' WHEN 6 then '公共集会场所' when 7 then '医疗卫生系统' when 8 then '生命线' WHEN 9 then '文化教育系统' else '其它' end from transport_building_information a,transport_identify_result b,transport_building_usage c,transport_sys_user d,transport_building_structure e,transport_eqinfo f where a.building_earthquakeid_id=f.id and a.building_constructtypeid_id=e.id and d.user_id = '"+request.session.get("user_id")+"' and a.building_userid_id = d.id   and a.id = b.result_buildnumber_id and c.id = a.building_buildusage_id "
	if request.method == "POST":
		qstring = request.POST.get("qstring1","")
		if len(qstring) <15:
			if settings.DEBUG == True:
				print qstring
			else:
				pass
		else:
			sj_sqlstring = sj_sqlstring +qstring
			if settings.DEBUG == True:
				print qstring 
			else:
				pass
	cursor = connection.cursor()            #获得一个游标(cursor)对象
	cursor.execute(sj_sqlstring+" GROUP BY case a.building_buildusage_id when 1 then '住宅' when 2 then '政府' WHEN 3 then '商业' when 4 then '站点' when 5 then '工业厂房' WHEN 6 then '公共集会场所' when 7 then '医疗卫生系统' when 8 then '生命线' WHEN 9 then '文化教育系统' else '其它' end")
	resultObj = use_fetchall(cursor)
	if settings.DEBUG == True:
		print "%"*60
	else:
		pass
	return HttpResponse(json.dumps(resultObj))

#统计图表接口_破坏等级
def countCharts_degree(request):
	context = RequestContext(request)
	context_dict = {}
	sj_sqlstring = "select sum(a.building_buildarea) as 面积,count(*) as '栋数',b.result_damagedegree from transport_building_information a,transport_identify_result b,transport_building_usage c,transport_sys_user d,transport_building_structure e,transport_eqinfo f where a.building_earthquakeid_id=f.id and a.building_constructtypeid_id=e.id and d.user_id = '"+request.session.get("user_id")+"' and a.building_userid_id = d.id   and a.id = b.result_buildnumber_id and c.id = a.building_buildusage_id "
	if request.method == "POST":
		qstring = request.POST.get("qstring1","")
		if len(qstring) <15:
			if settings.DEBUG == True:
				print qstring
			else:
				pass
		else:
			sj_sqlstring = sj_sqlstring +qstring
			if settings.DEBUG == True:
				print qstring 
			else:
				pass
	cursor = connection.cursor()            #获得一个游标(cursor)对象
	cursor.execute(sj_sqlstring+" GROUP BY b.result_damagedegree")
	resultObj = sf_fetchall(cursor)
	if settings.DEBUG == True:
		print "%"*60
	else:
		pass
	return HttpResponse(json.dumps(resultObj))


#统计图表接口_设防
def countCharts_sf(request):
	context = RequestContext(request)
	context_dict = {}

	sj_sqlstring = "select sum(a.building_buildarea) as 面积,case a.building_fortificationdegree	WHEN 6 then '6度设防'	when 7 then '7度设防'  when 8 then '8度设防'	WHEN 9 then '9度设防'	when 10 then '采用非正规抗震措施（民居、自建房等）' else '未设防'end ,count(*) as '栋数' from transport_building_information a,transport_identify_result b,transport_building_usage c,transport_sys_user d,transport_building_structure e,transport_eqinfo f where a.building_earthquakeid_id=f.id and a.building_constructtypeid_id=e.id and d.user_id = '"+request.session.get("user_id")+"' and  a.building_userid_id = d.id   and a.id = b.result_buildnumber_id and c.id = a.building_buildusage_id "
	if request.method == "POST":
		qstring = request.POST.get("qstring1","")
		if len(qstring) <15:
			if settings.DEBUG == True:
				print qstring
			else:
				pass
		else:
			sj_sqlstring = sj_sqlstring +qstring
	cursor = connection.cursor()            #获得一个游标(cursor)对象
	cursor.execute(sj_sqlstring+" GROUP BY case a.building_fortificationdegree WHEN 6 then '6度设防'	when 7 then '7度设防' when 8 then '8度设防'	WHEN 9 then '9度设防' when 10 then '采用非正规抗震措施（民居、自建房等）' else '未设防'end")
	resultObj = sf_fetchall(cursor)
	if settings.DEBUG == True:
		print "%"*60
	else:
		pass
	return HttpResponse(json.dumps(resultObj))
#chu li user
def user(request):
	context = RequestContext(request)
	context_dict = user_query(request)
	return render_to_response('transport/user.html',context_dict,context)

def useredit(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method == 'POST':
		if settings.DEBUG == True:
			print request.POST
		else:
			pass
		if settings.DEBUG == True:
			print "ti jiao le xiu gai xin xi"
		else:
			pass
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
			context_dict["savesuc"] = "修改成功！"
	context_dict["user"] = user_query(request)

	majorObj = user_major.objects.all()
	if majorObj:
		context_dict["majorObj"] = majorObj
	departObj = user_depart.objects.all()
	if departObj:
		context_dict["departObj"] = departObj
	titleObj = user_title.objects.all()
	if titleObj:
		context_dict["titleObj"] = titleObj	
	return render_to_response('transport/edituser.html',context_dict,context)



def usereditpass(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method == "GET":
		try:
			propassObj = t_passpro.objects.get(passpro_user__user_name = request.session.get("username"))
			context_dict["proObj"] = propassObj
			return render_to_response('transport/editpass.html',context_dict,context)
		except:
			context_dict["show"] = "请先设置密保！"
			return render_to_response('transport/editpass.html',context_dict,context)
	elif request.method == "POST":
		user_password = request.POST.get("old_password")
		if user_password != None:
			try:
				client_obj = sys_user.objects.get(user_name = request.session.get('username'),user_password = user_password)
			except:
				client_obj = 0
			if client_obj:
				new_user_password = request.POST.get("new_password")
				qrnew_user_password = request.POST.get("qrnew_password")
				if new_user_password == qrnew_user_password:
					client_obj.user_password = new_user_password
					client_obj.save()
					context_dict["show"] = "修改成功！"
					context_dict["passPro"] = False
					context_dict["proObj"] = t_passpro.objects.get(passpro_user__user_name = request.session.get("username"))
					return render_to_response('transport/editpass.html',context_dict,context)
				else:
					context_dict["result"] = "两次密码输入不一致！"
			elif user_password == "":
				context_dict["result"] = "请输入密码！"
			else:
				context_dict["result"] = "密码错误！"
			context_dict["passPro"] = True
			return render_to_response('transport/editpass.html',context_dict,context)
		else:
			answer1 = request.POST.get("answer1")
			answer2 = request.POST.get("answer2")
			answer3 = request.POST.get("answer3")
			try:
				propassObj = t_passpro.objects.get(passpro_user__user_name = request.session.get("username"),passpro_answer1 = answer1,passpro_answer2 = answer2,passpro_answer3 = answer3)
				context_dict["passPro"] = True
				return render_to_response('transport/editpass.html',context_dict,context)
			except:
				context_dict["show"] = "密保答案不正确！"
				context_dict["passPro"] = False
				context_dict["proObj"] = t_passpro.objects.get(passpro_user__user_name = request.session.get("username"))
				return render_to_response('transport/editpass.html',context_dict,context)
	return render_to_response('transport/editpass.html',context_dict,context)
	


def userpropass(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method == "GET":
		try:
			propassObj = t_passpro.objects.get(passpro_user__user_name = request.session.get("username"))
			context_dict["nopro"] = False
			context_dict["proObj"] = propassObj
		except:
			context_dict["nopro"] = True
		return render_to_response('transport/propass.html',context_dict,context)
	else:
		try:
			User = sys_user.objects.get(user_name = request.session.get("username"))
		except:
			context_dict["show"] = "用户名不合法"
			return render_to_response('transport/message.html',context_dict,context)
		question1 = request.POST.get("question1")
		if not question1 == None:
			question2 = request.POST.get("question2")
			question3 = request.POST.get("question3")
			answer1 = request.POST.get("answer1")
			answer2 = request.POST.get("answer2")
			answer3 = request.POST.get("answer3")
			if question1 == question2 or question1 == question3 or question2 == question3:
				context_dict["show"] = "密保问题不能重复！"
				context_dict["nopro"] = True
				return render_to_response('transport/propass.html',context_dict,context)
			if answer3 =="" or answer2 =="" or answer1=="":
				context_dict["show"] = "密保答案不能为空！"
				context_dict["nopro"] = True
				return render_to_response('transport/propass.html',context_dict,context)
			try:
				propassObj = t_passpro.objects.get(passpro_user__user_name = request.session.get("username"))
				propassObj.passpro_question1 = question1
				propassObj.passpro_question2 = question2
				propassObj.passpro_question3 = question3
				propassObj.passpro_answer1 = answer1
				propassObj.passpro_answer2 = answer2
				propassObj.passpro_answer3 = answer3
				propassObj.save()
			except:	
				propassObj = t_passpro(
					passpro_user = User,
					passpro_question1 = question1,
					passpro_question2 = question2,
					passpro_question3 = question3,
					passpro_answer1 = answer1,
					passpro_answer2 = answer2,
					passpro_answer3 = answer3,
					)
				propassObj.save()
			context_dict["show"] = "密保保存成功"
			context_dict["proObj"] = t_passpro.objects.get(passpro_user__user_name = request.session.get("username"))
			return render_to_response('transport/propass.html',context_dict,context)
		else:#没有问题选项则认为是验证密保
			answer1 = request.POST.get("answer1")
			answer2 = request.POST.get("answer2")
			answer3 = request.POST.get("answer3")
			try:
				propassObj = t_passpro.objects.get(passpro_user__user_name = request.session.get("username"),passpro_answer1 = answer1,passpro_answer2 = answer2,passpro_answer3 = answer3)
				context_dict["nopro"] = True
			except:
				context_dict["show"] = "密保答案不正确！"
				context_dict["nopro"] = False
				context_dict["proObj"] = t_passpro.objects.get(passpro_user__user_name = request.session.get("username"))
			return render_to_response('transport/propass.html',context_dict,context)

def usermessage(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method == "POST":
		try:
			messageUser = sys_user.objects.get(user_name = request.session.get("username"))
		except:
			context_dict["Error"] = "用户名不合法"
			return render_to_response('transport/message.html',context_dict,context)
		messageTitle = request.POST.get("message_title","")
		messageContent = request.POST.get("message_content","")
		if messageTitle == "" or messageContent == "":
			context_dict["Error"] = "标题或内容不能为空"
			return render_to_response('transport/message.html',context_dict,context)
		try:

			messageObj = t_message(
				message_user = messageUser,
				message_title = messageTitle,
				message_content = messageContent,
				)
			messageObj.save()
			context_dict["Error"] = "留言成功！"
			return render_to_response('transport/message.html',context_dict,context)
		except Exception,e:
			print "error",e
			context_dict["Error"] = e
			return render_to_response('transport/message.html',context_dict,context)
	return render_to_response('transport/message.html',context_dict,context)


def showhelp(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('transport/showhelp.html',context_dict,context)


def delete_build(request):
	context = RequestContext(request)
	context_dict = {}
	if settings.DEBUG == True:
		print "delete function*******************************************"
	else:
		pass
	if request.method == 'GET':
		idlist = request.GET.get("id_list")
		try:
			idlist = idlist.split(",")
			for item in idlist:
				if settings.DEBUG == True:
					print item
				else:
					pass
				resultObj = identify_result.objects.get(result_buildnumber__building_buildnumber = item)
				resultObj.delete()
				context_dict["is_delete"] = "yes"
		except Exception,e:
			if settings.DEBUG == True:
				print "error,",e
			else:
				pass
		
		return HttpResponseRedirect('/t/count?is_delete=true')
	else:
		return HttpResponseRedirect('/t/count')




def export_xls(request):
	if settings.DEBUG == True:
		print "******************************************************"
	else:
		pass

	wb=Workbook()
	if settings.DEBUG == True:
		print "################################"
	else:
		pass
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

def logopdf(request):
	context = RequestContext(request)
	context_dict = {}
	context_dict["url"] = os.path.dirname(__file__)[0:-10]+"/static/file/simsun.ttc"
	buildid = request.session.get('building_buildnumber')
	if not buildid:
		buildid = request.GET.get("buildid")
	build_obj = building_information.objects.get(building_buildnumber = buildid)
	if build_obj:
		context_dict['build_obj'] = build_obj
	result = identify_result.objects.get(result_buildnumber__building_buildnumber = buildid)
	if result:
		context_dict['result'] = result
	return render_to_response('transport/pdf.html',context_dict,context)
	
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
	try:
		if settings.DEBUG == True:
			print "*"*20,request.get_host()
		else:
			pass
		logohtml = urllib2.urlopen('http://'+request.get_host()+'/t/logopdf?buildid='+request.session.get('building_buildnumber')).read()
		result = file(os.path.dirname(__file__)[0:-10]+'/templates/'+request.session.get("building_buildnumber")+'image.pdf', 'wb') 
		if settings.DEBUG == True:
			print "create PDF file success1"
		else:
			pass
		pdf = pisa.CreatePDF(logohtml, result)
		if settings.DEBUG == True:
			print "create PDF file success"
		else:
			pass
		result.close()
		logodata1 = readFile(os.path.dirname(__file__)[0:-10]+'/templates/'+request.session.get("building_buildnumber")+'image.pdf')
		response = HttpResponse(logodata1,content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="'+request.session.get("building_buildnumber")+'image.pdf"'	
		os.remove(os.path.dirname(__file__)[0:-10]+'/templates/'+request.session.get("building_buildnumber")+'image.pdf')
		return response
	except Exception,e:
		if settings.DEBUG == True:
			print "error",e
		else:
			pass
		return HttpResponse(e)

	
def dlcompdf(request):
	try:
		if settings.DEBUG == True:
			print "*"*20,request.get_host()
		else:
			pass
		htmlcontent = urllib2.urlopen('http://'+request.get_host()+'/t/pdfdataReplace?buildid='+request.session.get('building_buildnumber')).read()
		result = file(os.path.dirname(__file__)[0:-10]+'/templates/'+request.session.get("building_buildnumber")+'.pdf', 'wb') 
		if settings.DEBUG == True:
			print "create PDF file success"
		else:
			pass
		pdf = pisa.CreatePDF(htmlcontent.replace("ttttt","<br>"), result)
		if settings.DEBUG == True:
			print "create PDF file success"
		else:
			pass
		result.close()
		data1 = readFile(os.path.dirname(__file__)[0:-10]+'/templates/'+request.session.get("building_buildnumber")+'.pdf')
		response = HttpResponse(data1,content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="'+request.session.get("building_buildnumber")+'.pdf"'	
		os.remove(os.path.dirname(__file__)[0:-10]+'/templates/'+request.session.get("building_buildnumber")+'.pdf')
		return response

	except Exception,e:
		if settings.DEBUG == True:
			print "error",e
		else:
			pass
		return HttpResponse(e)


def pdfdataReplace(request):
	context = RequestContext(request)
	context_dict = {}
	context_dict["url"] = os.path.dirname(__file__)[0:-10]+"/static/file/simsun.ttc"
	buildid = request.session.get('building_buildnumber')
	if not buildid:
		buildid = request.GET.get("buildid")
		
		#context_dict['build'] = request.session.get["building_buildnumber"]
	build_obj = building_information.objects.get(building_buildnumber = buildid)
	if build_obj:
		context_dict['build_obj'] = build_obj
		context_dict['usage'] = building_usage.objects.get(building_usageid = build_obj.building_buildusage)
	environmentObj = environment.objects.get(environment_buildnumber__building_buildnumber = buildid)
	cdyx = environmentObj.environment_earthquakeeff.split(",")
	djzk = environmentObj.environment_foundation.split(",")
	if "CDYXQT" in environmentObj.environment_earthquakeeff:
		context_dict["cdyxqita"] = ((cdyx[-1])[3:-2]).decode('unicode_escape')
	if "DJZKQT" in environmentObj.environment_foundation:
		context_dict["djzkqita"] = ((djzk[-1])[3:-2]).decode('unicode_escape')
	damageObj = damage.objects.filter(damage_buildnumber__building_buildnumber = buildid)
	# else:
	# 	build_obj = building_information.objects.get(building_buildnumber = buildid)
	# 	if build_obj:
	# 		context_dict['build_obj'] = build_obj
	# 		context_dict['usage'] = building_usage.objects.get(building_usageid = build_obj.building_buildusage)
	# 	environmentObj = environment.objects.get(environment_buildnumber__building_buildnumber = buildid)
	# 	damageObj = damage.objects.filter(damage_buildnumber__building_buildnumber = buildid)
	if environmentObj:
		context_dict['building_environment'] = environmentObj
	if damageObj:
		context_dict['xdamage'] = damageObj
	if settings.DEBUG == True:
		print "%"*60
	else:
		pass
	if settings.DEBUG == True:
		print buildid
	else:
		pass
	sql="select distinct a.damage_locationid_id,b.location_name from transport_damage a,transport_buildlocation b where a.damage_locationid_id = b.id and damage_id = '%s'" % buildid
	cursor=connection.cursor()
	cursor.execute(sql)
	blogs = cursor.fetchall()
	dicts = []
	for item in blogs:
		location = {}
		sql = "select distinct a.damage_catalogid_id,b.catalog_name from transport_damage a,transport_sublocationcatalog b  where b.id=a.damage_catalogid_id  and damage_id = '%s' and damage_locationid_id = %d" % (buildid,item[0])
		cursor=connection.cursor()
		cursor.execute(sql)
		location["name"] = insertTTTTT(4,item[1]) 
		blogscata = cursor.fetchall()
		sql = "select count(*) from transport_damage  where damage_id = '%s' and damage_locationid_id = %d" % (buildid,item[0])
		cursor=connection.cursor()
		cursor.execute(sql)
		blogscataCount = cursor.fetchall()
		location["length"] = blogscataCount[0][0]
		catalist = []
		for cata in blogscata:
			dict_cata = {}
			cataid = int(cata[0])
			dict_cata["name"] = insertTTTTT(9,cata[1]) 
			sql = "select count(*) from transport_damage where damage_id = '%s' and damage_locationid_id = %d and damage_catalogid_id = %d " % (buildid,item[0],cataid)
			cursor=connection.cursor()
			cursor.execute(sql)
			sublocalCount = cursor.fetchall()
			dict_cata["length"] = sublocalCount[0][0]
			sql = "select distinct a.damage_sublocationid_id,b.sublocal_name from transport_damage a,transport_sublocal b where a.damage_sublocationid_id = b.id and damage_id = '%s' and damage_locationid_id = %d and damage_catalogid_id = %d " % (buildid,item[0],cataid)
			cursor=connection.cursor()
			cursor.execute(sql)
			sublocals = cursor.fetchall()
			sublocallist = []
			for sublocal in sublocals:
				dict_sublocal = {}
				dict_sublocal["name"] = insertTTTTT(17,sublocal[1]) 
				sql = "select count(*) from transport_damage  where damage_id = '%s' and damage_locationid_id = %d and damage_catalogid_id = %d and damage_sublocationid_id = %d " % (buildid,item[0],cataid,sublocal[0])
				cursor=connection.cursor()
				cursor.execute(sql)
				sublocalsCount = cursor.fetchall()
				dict_sublocal["length"] = sublocalsCount[0][0]
				sql = "select damage_number,damage_degree,damage_parameteradjust,damage_description,damage_remark from transport_damage where damage_id = '%s' and damage_locationid_id = %d and damage_catalogid_id = %d and damage_sublocationid_id = %d " % (buildid,item[0],cataid,sublocal[0])
				cursor=connection.cursor()
				cursor.execute(sql)
				sublocaldetail = cursor.fetchall()
				sublocaldetaillist = []
				for detail in sublocaldetail:
					dictdetail = {}
					if detail[0] == "0":
						dictdetail["number"] = "个别"
					elif detail[0] == "1":
						dictdetail["number"] = "少数"
					elif detail[0] == "2":
						dictdetail["number"] = "多数"
					else:
						dictdetail["number"] = ""
					if detail[1] == "0":
						dictdetail["degree"] = "轻微"
					elif detail[1] == "1":
						dictdetail["degree"] = "中等"
					elif detail[1] == "2":
						dictdetail["degree"] = "严重"
					else:
						dictdetail["degree"] = ""
					dictdetail["adjust"] = detail[2]
					dictdetail["description"] = detail[3]
					dictdetail["remark"] = detail[4]
					if not dictdetail["number"] == "":
						sublocaldetaillist.append(dictdetail)
					else:
						pass
				# if len(sublocaldetaillist) != 0:	
				dict_sublocal["detail"] = sublocaldetaillist
				sublocallist.append(dict_sublocal)
			# if len(sublocallist) != 0:
			dict_cata["sublocal"] = sublocallist
			catalist.append(dict_cata)
		# if len(catalist) != 0:
		location["cata"] = catalist
		dicts.append(location)
		context_dict["dicts"] = dicts
	# return HttpResponse(dicts)
	if not sys.platform == "win32":
		return render_to_response('transport/compdfLinux.html',context_dict,context) 
	else:
		return render_to_response('transport/compdf.html',context_dict,context) 


#读取页面提交数据存要生成的报告中
def pdfdata(request):
	context = RequestContext(request)
	context_dict = {}
	buildid = request.session.get('building_buildnumber')
	if not buildid:
		buildid = request.GET.get("buildid")
		
		#context_dict['build'] = request.session.get["building_buildnumber"]
	build_obj = building_information.objects.get(building_buildnumber = buildid)
	if build_obj:
		context_dict['build_obj'] = build_obj
		context_dict['usage'] = building_usage.objects.get(building_usageid = build_obj.building_buildusage)
	environmentObj = environment.objects.get(environment_buildnumber__building_buildnumber = buildid)
	damageObj = damage.objects.filter(damage_buildnumber__building_buildnumber = buildid)
	# else:
	# 	build_obj = building_information.objects.get(building_buildnumber = buildid)
	# 	if build_obj:
	# 		context_dict['build_obj'] = build_obj
	# 		context_dict['usage'] = building_usage.objects.get(building_usageid = build_obj.building_buildusage)
	# 	environmentObj = environment.objects.get(environment_buildnumber__building_buildnumber = buildid)
	# 	damageObj = damage.objects.filter(damage_buildnumber__building_buildnumber = buildid)
	if environmentObj:
		context_dict['building_environment'] = environmentObj
	cdyx = environmentObj.environment_earthquakeeff.split(",")
	djzk = environmentObj.environment_foundation.split(",")
	if "CDYXQT" in environmentObj.environment_earthquakeeff:
		context_dict["cdyxqita"] = ((cdyx[-1])[3:-2]).decode('unicode_escape')
	if "DJZKQT" in environmentObj.environment_foundation:
		context_dict["djzkqita"] = ((djzk[-1])[3:-2]).decode('unicode_escape')
	if damageObj:
		context_dict['xdamage'] = damageObj
	if settings.DEBUG == True:
		print "%"*60
	else:
		pass
	if settings.DEBUG == True:
		print buildid
	else:
		pass
	sql="select distinct a.damage_locationid_id,b.location_name from transport_damage a,transport_buildlocation b where a.damage_locationid_id = b.id and damage_id = '%s'" % buildid
	cursor=connection.cursor()
	cursor.execute(sql)
	blogs = cursor.fetchall()
	dicts = []
	for item in blogs:
		location = {}
		sql = "select distinct a.damage_catalogid_id,b.catalog_name from transport_damage a,transport_sublocationcatalog b  where b.id=a.damage_catalogid_id  and damage_id = '%s' and damage_locationid_id = %d" % (buildid,item[0])
		cursor=connection.cursor()
		cursor.execute(sql)
		location["name"] = item[1]
		
		blogscata = cursor.fetchall()
		sql = "select count(*) from transport_damage  where damage_id = '%s' and damage_locationid_id = %d" % (buildid,item[0])
		cursor=connection.cursor()
		cursor.execute(sql)
		blogscataCount = cursor.fetchall()
		location["length"] = blogscataCount[0][0]
		catalist = []
		for cata in blogscata:
			dict_cata = {}
			cataid = int(cata[0])
			dict_cata["name"] = cata[1]
			sql = "select count(*) from transport_damage where damage_id = '%s' and damage_locationid_id = %d and damage_catalogid_id = %d " % (buildid,item[0],cataid)
			cursor=connection.cursor()
			cursor.execute(sql)
			sublocalCount = cursor.fetchall()
			dict_cata["length"] = sublocalCount[0][0]
			sql = "select distinct a.damage_sublocationid_id,b.sublocal_name from transport_damage a,transport_sublocal b where a.damage_sublocationid_id = b.id and damage_id = '%s' and damage_locationid_id = %d and damage_catalogid_id = %d " % (buildid,item[0],cataid)
			cursor=connection.cursor()
			cursor.execute(sql)
			sublocals = cursor.fetchall()
			sublocallist = []
			for sublocal in sublocals:
				dict_sublocal = {}
				dict_sublocal["name"] = sublocal[1]
				sql = "select count(*) from transport_damage  where damage_id = '%s' and damage_locationid_id = %d and damage_catalogid_id = %d and damage_sublocationid_id = %d " % (buildid,item[0],cataid,sublocal[0])
				cursor=connection.cursor()
				cursor.execute(sql)
				sublocalsCount = cursor.fetchall()
				dict_sublocal["length"] = sublocalsCount[0][0]
				sql = "select damage_number,damage_degree,damage_parameteradjust,damage_description,damage_remark from transport_damage where damage_id = '%s' and damage_locationid_id = %d and damage_catalogid_id = %d and damage_sublocationid_id = %d " % (buildid,item[0],cataid,sublocal[0])
				cursor=connection.cursor()
				cursor.execute(sql)
				sublocaldetail = cursor.fetchall()
				sublocaldetaillist = []
				for detail in sublocaldetail:
					dictdetail = {}
					if detail[0] == "0":
						dictdetail["number"] = "个别"
					elif detail[0] == "1":
						dictdetail["number"] = "少数"
					elif detail[0] == "2":
						dictdetail["number"] = "多数"
					else:
						dictdetail["number"] = ""
					if detail[1] == "0":
						dictdetail["degree"] = "轻微"
					elif detail[1] == "1":
						dictdetail["degree"] = "中等"
					elif detail[1] == "2":
						dictdetail["degree"] = "严重"
					else:
						dictdetail["degree"] = ""
					dictdetail["adjust"] = detail[2]
					dictdetail["description"] = detail[3]
					dictdetail["remark"] = detail[4]
					if not dictdetail["number"] == "":
						sublocaldetaillist.append(dictdetail)
					else:
						pass
				# if len(sublocaldetaillist) != 0:	
				dict_sublocal["detail"] = sublocaldetaillist
				sublocallist.append(dict_sublocal)
			dict_cata["sublocal"] = sublocallist
			catalist.append(dict_cata)
		location["cata"] = catalist
		dicts.append(location)
		context_dict["dicts"] = dicts
	return render_to_response('transport/compdf.html',context_dict,context) 


def test(request):
	return HttpResponse(os.path.dirname(__file__)[0:-10])


def getUserPos(request):
	if request.method=="POST":
		try:
			locationObj = userLocation.objects.get(loc_user__user_id = request.POST.get("userid"))
			pos = {}
			res = []
			pos["lng"] = locationObj.loc_longitude
			pos["lat"] = locationObj.loc_latitude
			res.append(pos)
			return HttpResponse(json.dumps(res))
		except Exception,e:
			if settings.DEBUG == True:
				print "error is ",e
			else:
				pass
			return HttpResponse("error")



def addImage(request,position):
	if request.method == "POST":
		if settings.DEBUG == True:
			print "enter post add image"
		else:
			pass
		try:
			if position =="front":
				buildImageObj = buildFrontImage(
					buildid = request.session.get("building_buildnumber"),
					frontimage = request.FILES['imagefile'],
					desc = request.POST.get("neirong"),
					name = request.POST.get("imagename"),
					)
			elif position =="back":
				buildImageObj = buildBackImage(
					buildid = request.session.get("building_buildnumber"),
					backimage = request.FILES['imagefile'],
					desc = request.POST.get("neirong"),
					name = request.POST.get("imagename"),
					)
			elif position =="side":
				buildImageObj = buildSideImage(
					buildid = request.session.get("building_buildnumber"),
					sideimage = request.FILES['imagefile'],
					desc = request.POST.get("neirong"),
					name = request.POST.get("imagename"),
					)
			elif position =="floor":
				buildImageObj = buildFloorImage(
					buildid = request.session.get("building_buildnumber"),
					floorimage = request.FILES['imagefile'],
					desc = request.POST.get("neirong"),
					name = request.POST.get("imagename"),
					)
			elif position =="inner":
				try:
					os.remove(os.path.dirname(__file__)[0:-10]+'/media/'+str(buildImageObj.innerimage))
				except Exception,e:
					if settings.DEBUG == True:
						print "error is ",e
					else:
						pass
				buildImageObj.innerimage = request.FILES['imagefile']
			buildImageObj.save()
		except Exception,e:
			if settings.DEBUG == True:
				print "error",e
			else:
				pass
			
		try:
			if position =="front":
				buildImageObj = buildFrontImage.objects.filter(buildid = request.session.get("building_buildnumber")).order_by("-id")[0]
				imgsrc = buildImageObj.frontimage
				imgname = buildImageObj.name
				imgdesc = buildImageObj.desc
			elif position =="back":
				buildImageObj = buildBackImage.objects.filter(buildid = request.session.get("building_buildnumber")).order_by("-id")[0]
				imgsrc = buildImageObj.backimage
				imgname = buildImageObj.name
				imgdesc = buildImageObj.desc
			elif position =="side":
				buildImageObj = buildSideImage.objects.filter(buildid = request.session.get("building_buildnumber")).order_by("-id")[0]
				imgsrc = buildImageObj.sideimage
				imgname = buildImageObj.name
				imgdesc = buildImageObj.desc
			elif position =="floor":
				buildImageObj = buildFloorImage.objects.filter(buildid = request.session.get("building_buildnumber")).order_by("-id")[0]
				imgsrc = buildImageObj.floorimage
				imgname = buildImageObj.name
				imgdesc = buildImageObj.desc
		except Exception,e:
			if settings.DEBUG == True:
				print "error",e
			else:
				pass
		return HttpResponse("<script>window.parent.uploadSuccess('%s','%s','%s','%s');</script>" % (position,imgsrc,imgname,imgdesc))




def searcharea(request):
	if request.method == 'POST':
		province = request.POST.get("province")
		areaObj = region.objects.filter( region_desc__contains = province)[0]
		if areaObj:
			area = areaObj.region_location
			return HttpResponse(area)
		else:
			return  HttpResponse("error")

	else:
		return HttpResponse("only support post")

def deleteimg(request):
	context = RequestContext(request)
	if request.method == "POST":
		try:
			sr1 = request.POST.get("sr1")
			posi1 = request.POST.get("posi1")
			if posi1 == "front":
				if settings.DEBUG == True:
					print sr1
				else:
					pass
				sqlstring = "DELETE from transport_buildfrontimage where frontimage = '%s'" % sr1
				cursor = connection.cursor()            #获得一个游标(cursor)对象
				cursor.execute(sqlstring)
				os.remove(os.path.dirname(__file__)[0:-10]+'/media/'+sr1)
				return HttpResponse("success")
			if posi1 == "back":
				if settings.DEBUG == True:
					print sr1
				else:
					pass
				sqlstring = "DELETE from transport_buildbackimage where backimage = '%s'" % sr1
				cursor = connection.cursor()            #获得一个游标(cursor)对象
				cursor.execute(sqlstring)
				os.remove(os.path.dirname(__file__)[0:-10]+'/media/'+sr1)
				return HttpResponse("success")
			if posi1 == "side":
				if settings.DEBUG == True:
					print sr1
				else:
					pass
				sqlstring = "DELETE from transport_buildsideimage where sideimage = '%s'" % sr1
				cursor = connection.cursor()            #获得一个游标(cursor)对象
				cursor.execute(sqlstring)
				os.remove(os.path.dirname(__file__)[0:-10]+'/media/'+sr1)
				return HttpResponse("success")
			if posi1 == "floor":
				if settings.DEBUG == True:
					print sr1
				else:
					pass
				sqlstring = "DELETE from transport_buildfloorimage where floorimage = '%s'" % sr1
				cursor = connection.cursor()            #获得一个游标(cursor)对象
				cursor.execute(sqlstring)
				os.remove(os.path.dirname(__file__)[0:-10]+'/media/'+sr1)
				return HttpResponse("success")
		except Exception,e:
			if settings.DEBUG == True:
				print "exception",e
			else:
				pass
			return HttpResponse(e)