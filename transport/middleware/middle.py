from django.http import HttpResponseRedirect    
from django.contrib.auth import SESSION_KEY    
from urllib import quote 
from django.template import RequestContext
from django.shortcuts import render_to_response

class SetRemoteAddrFromForwardedFor(object):
    def process_request(self, request):
    		path = request.path
		if path != "/t/" and path != "/t/login_va/" and not path.startswith("/admin/"):
			try:	
				username = request.session.get("username")
				print "sun pengfeieS"
				print username
			except:
				username = 0
			if username:
				print "yi deng lu"
			else:
           		 # HttpResponseRedirect("http://www.baidu.com")
				return HttpResponseRedirect("/t")