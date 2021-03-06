# coding=utf-8
from django.http import HttpResponseRedirect    
from django.contrib.auth import SESSION_KEY    
from urllib import quote 
from django.template import RequestContext
from django.shortcuts import render_to_response
from transport.models import sys_user
from datetime import *
import time

class SetRemoteAddrFromForwardedFor(object):
    def process_request(self, request):
    		path = request.path
    		context_dict = {}
		if not path.startswith("/n/")  and not  path.startswith("/t/phone/") and not path.startswith("/t/ulogin") and not path.startswith("/t/adLogVal") and not path.startswith("/t/modUserPos") and path != "/t/logopdf" and path != "/t/pdfdataReplace" and path !="" and path != "/t/" and path != "/t/login_va/" and path !="/t/register" and not path.startswith("/t/user_name") and not path.startswith("/t/get_check_code_image") and not path.startswith('/t/authcode') and not path.startswith("/t/register") and not path.startswith("/admin/") and not path.startswith("/t/test") and not path.startswith("/r/resetPass") and not path.startswith("/r/resetPass1"):
			#print path	
			if request.session.get("username"):
			#print "sun pengfeieS"
				username = request.session.get("username")
			else:
				context_dict['error'] = '请先登录！'
				return render_to_response('transport/login.html',context_dict)
			if username:
				try:
					userObj = sys_user.objects.get(user_name = username)
					lastalivetime = userObj.user_lastalivetime
					if lastalivetime:
						# print lastalivetime
						lastalivetime = str(lastalivetime)
						# print lastalivetime
						time_last = datetime.strptime(lastalivetime,'%Y-%m-%d %H:%M:%S')
						# print time_last
						# print "ss"
						time_now = datetime.now()
						time_now = str(time_now)[:19]
						# print time_now
						time_now = datetime.strptime(time_now,'%Y-%m-%d %H:%M:%S')
						jiange = time_now - time_last
						# 	jiange = time.strftime('%Y-%m-%d %X',time.localtime(time.time())) - lastalivetime
						# print jiange.seconds
						if jiange.seconds > 1200:
							context_dict = {}
							context_dict['error'] = '用户20分钟内未操作，请重新登陆！'
							request.session.clear()
							return render_to_response('transport/login.html',context_dict)
						else:
							userObj.user_lastalivetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
							userObj.save()
							#print "已登录".decode('utf8')
				except:
					pass
			else:
           		 # HttpResponseRedirect("http://www.baidu.com")
				return HttpResponseRedirect("/t")