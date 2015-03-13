#coding:utf-8
from django.test import TestCase
from models import *
import string,random
from datetime import datetime
from xml.etree import ElementTree
from django.template import RequestContext
import requests
import re



def SendRandomCode(u_tel):	
	url = 'http://www.mxtong.net.cn/GateWay/Services.asmx/DirectSend'	
	code = RandCode()
	content = '您的验证码为'+code+'，请妥善保管，请勿向任何人泄漏。[地震所]'	
	payload = {'UserID':'965125','Account':'admin','Password':'965125','Phones':u_tel,
				'Content':content,'SendTime':'','SendType':'1','PostFixNumber':''}	
	r = requests.get(url,params=payload)	
	#xml = ElementTree.fromstring(r.content)
	#RetCode = xml.find("ROOT").find("RetCode").text
	#print RetCode
	search = re.search('<RetCode>(?P<status>\w+)</RetCode>',r.content)
	RetCode = search.groupdict()['status']	
	if RetCode == 'Sucess':
		if CheckExist(sys_user,{'user_tel':u_tel}):
			randomCode_obj = sys_user.objects.get(user_tel__exact = u_tel)
			randomCode_obj.user_pac = code
			randomCode_obj.user_updatetime = datetime.now()
			randomCode_obj.save()
			return True
		else:
			return False		
	else:		
		return False



def CheckExist(model,kwargs):
	objects = model.objects.filter(**kwargs)
	if objects:
		return True
	return False


def CheckRandomCode(u_tel,code):
	randomCode_obj = sys_user.objects.filter(user_tel__exact = u_tel)
	if randomCode_obj:			
		if randomCode_obj[0].user_pac == code:				
			return True
		else:			
			return False
	else:		
		return False



def RandCode():
	return string.join(random.sample(['1','2','3','4','5','6','7','8','9','0'], 6)).replace(' ','')