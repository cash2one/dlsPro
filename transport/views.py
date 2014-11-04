# coding=utf-8
from django.db import connection,transaction
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from transport.models import sys_user,result,building_information,EQInfo
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
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
			print 'login failed'
			context_dict['error'] = '用户不存在'
			return render_to_response('transport/login.html',context_dict,context)

	return render_to_response('transport/login.html',context_dict,context)

def index(request):
	context = RequestContext(request)
	context_dict = user_query(request)
	return render_to_response('transport/index.html',context_dict,context)



def checkup(request):
	context = RequestContext(request)
	context_dict = {}
	EQ_obj = EQInfo.objects.all()
	p = Paginator(EQ_obj,5)

	page_num  = request.GET.get("page",1)
	try:
		item = p.page(page_num)
	except PageNotAnInteger:
		item = p.page(1)
	except EmptyPage:
		item = p.page(p.num_pages)
	context_dict["item"] = item
	context_dict["obj"] = item[0]
	return render_to_response('transport/checkup.html',context_dict,context)

def check_eq(request):
	context_dict = {}
	print "jin ru check_eq function "
	eq_id = request.GET.get("eq_id")
	print eq_id
	EQ_obj = EQInfo.objects.get(eq_id = eq_id)
	print "jin ru check_eq function "
	# cursor = connection.cursor()            #获得一个游标(cursor)对象
	# cursor.execute("select * from transport_eqinfo where eq_id =%s"%eq_id )
	# print "keyibu"
	# raw = cursor.fetchone()
	# print raw
	str1 = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s'%(EQ_obj.eq_id,EQ_obj.eq_name,EQ_obj.eq_date,EQ_obj.eq_time,EQ_obj.eq_depth,EQ_obj.eq_ms,EQ_obj.eq_lon,EQ_obj.eq_lat,EQ_obj.eq_maxintensity,EQ_obj.eq_focalmechanism,EQ_obj.eq_desc)

	print EQ_obj
	return HttpResponse(str1)
	

def checkup2(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('transport/checkup2.html',context_dict,context)
def checkup3(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('transport/checkup3.html',context_dict,context)
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


#chu li count
def count(request):
	context = RequestContext(request)
	context_dict = {}
	build_id = result.objects.filter()
	b_id = build_id[0].building_id
	print b_id
	obj = building_information.objects.filter(building_name=b_id)
	print obj[0].building_name

	cursor = connection.cursor()            #获得一个游标(cursor)对象
	cursor.execute('select * from transport_result a ,transport_building_information b where a.building_id_id = b.id')
	raw = cursor.fetchall()                 #返回结果行 或使用 #raw = cursor.fetchall()
	p = Paginator(raw,2)

	page_num  = request.GET.get("page",1)
	try:
		item = p.page(page_num)
	except PageNotAnInteger:
		item = p.page(1)
	except EmptyPage:
		item = p.page(p.num_pages)


	print len(raw[0])
	print "xxxxx"
	t = len(raw[0])
	l = 0
	for l in range(0,len(raw)):
		for i in raw[l]:
			print i
		print "xxxxx"
	print raw[0][1]
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
		client_obj = sys_user.objects.get(user_name=request.session.get("username"))
		if client_obj:
			client_obj.user_realname = userrealname
			client_obj.user_email = email
			client_obj.user_zipcode = zipcode
			client_obj.user_telnum = telnum
			client_obj.user_profession = profession
			client_obj.user_org = danwei
			client_obj.user_deputy = title
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
			context_dict["result"] = "success saved"
		elif user_password == "":
			context_dict["result"] = "qingshurumima"
		else:
			context_dict["result"] = "wrong password"
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
	print request.GET.get("id_list")
	return HttpResponseRedirect('/t/count?is_delete=True')


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
