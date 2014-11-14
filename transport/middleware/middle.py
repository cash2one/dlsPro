from django.http import HttpResponseRedirect    
from django.contrib.auth import SESSION_KEY    
from urllib import quote 
from django.template import RequestContext
from django.shortcuts import render_to_response

class SetRemoteAddrFromForwardedFor(object):
    def process_request(self, request):
    		path = request.path
		if path != "/t/" and path != "/t/login_va/" and path !="/t/register" and not path.startswith("/t/get_check_code_image") and not path.startswith('/t/authcode') and not path.startswith("/t/register") and not path.startswith("/admin/") and not path.startswith("/t/test"):
			try:
				#print path	
				username = request.session.get("username")
				#print "sun pengfeieS"
				print username
			except:
				username = 0
			if username:
				print "yi deng lu"
			else:
           		 # HttpResponseRedirect("http://www.baidu.com")
				return HttpResponseRedirect("/t")