# coding=utf-8
from django.conf.urls import patterns, url
from transport import views

urlpatterns = patterns('',
	
	url(r'^register$', views.register, name='register'),
	url(r'^user_name/$', views.uniname, name='uniname'),
#	url(r'^test/$', views.testajax, name='testajax'),
	url(r'^get_check_code_image/$',views.get_check_code_image,name='get_check_code_image'),
	url(r'^authcode/$',views.authcode,name='authcode'),
	url(r'^register_info1/$',views.register_info1,name='register_info1'),
	url(r'^register_info2/$',views.register_info2,name='register_info2'),
	url(r'^register_activate1$',views.activate1,name='activate1'),
	url(r'^exit$', views.exit, name='exit'),
	url(r'^$', views.login, name='login'),
	url(r'^login_va/$', views.login_va, name='login_va'),
	url(r'^adLogVal/$', views.adLogVal, name='adLogVal'),
	url(r'^ulogin/$', views.ulogin, name='ulogin'),
	url(r'^index$', views.index, name='index'),
	#处理 checkup
	url(r'^checkup$', views.checkup, name='checkup'),
	url(r'^checkEqMap$', views.checkEqMap, name='checkEqMap'),
	url(r'^check_eq$', views.check_eq, name='checkup_eq'),
	url(r'^checkup2$', views.checkup2, name='checkup2'),
	url(r'^checkup3$', views.checkup3, name='checkup3'),
	url(r'^checkup4$', views.checkup4, name='checkup4'),
	url(r'^checkup5$', views.checkup5, name='checkup5'),
	url(r'^check5save$', views.check5save, name='check5save'),
	url(r'^check5dir$', views.check5dir, name='check5dir'),
	url(r'^checkup6$', views.checkup6, name='checkup6'),
	url(r'^editCheckup3$', views.editCheckup3, name='editCheckup3'),
	
	#处理 count
	url(r'^count$', views.count, name='count'),
	url(r'^countAjax$', views.countAjax, name='countAjax'),
	url(r'^countExportXls$', views.countExportXls, name='countExportXls'),
	url(r'^countMap$', views.countMap, name='countMap'),
	url(r'^countCharts_sj$', views.countCharts_sj, name='countCharts_sj'),
	url(r'^countCharts_use$', views.countCharts_use, name='countCharts_use'),
	url(r'^countCharts_sf$', views.countCharts_sf, name='countCharts_sf'),
	url(r'^countCharts_degree$', views.countCharts_degree, name='countCharts_degree'),
	url(r'^ditu$', views.ditu, name='ditu'),

	#处理 user
	url(r'^user$', views.user, name='user'),
	url(r'^useredit$', views.useredit, name='useredit'),
	url(r'^usereditpass$', views.usereditpass, name='usereditpass'),
	url(r'^userpropass$', views.userpropass, name='userpropass'),
	url(r'^usermessage$', views.usermessage, name='usermessage'),
	#帮助
	url(r'^help$', views.help, name='help'),
	url(r'^helpcontent.html$', views.helpcontent, name='helpcontent'),
	#delete
	url(r'^delete_build*$', views.delete_build, name='delete'),


	url(r'^export_xls.*$', views.export_xls, name='export_xls'),
	url(r'^downloadpdf$', views.downloadpdf, name='downloadpdf'),
	url(r'^readFile$', views.readFile, name='readFile'),
	# url(r'^pdf_head$', views.pdf_head, name='pdf_head'),
	url(r'^dlcompdf$', views.dlcompdf, name='dlcompdf'),
	url(r'^pdfdata$', views.pdfdata, name='pdfdata'),
	url(r'^pdfdataReplace$', views.pdfdataReplace, name='pdfdataReplace'),
	#实验
	url(r'^showhelp$', views.showhelp, name='showhelp'),
	url(r'^test$', views.test, name='test'),
	#修改用户位置信息
	url(r'^modUserPos$', views.modUserPos, name='modUserPos'),
	#获取用户位置信息
	url(r'^getUserPos$', views.getUserPos, name='getUserPos'),
	#上传图片
	url(r'^addImage/(.*?)$', views.addImage, name='addImage'),
	#查询地区
	url(r'^searcharea$', views.searcharea, name='searcharea'),

	url(r'^logopdf$', views.logopdf, name='logopdf'),
	#删除图片
	url(r'^deleteimg$', views.deleteimg, name='deleteimg'),
	#找回密码
	url(r'^retrievePass$', views.retrievePass, name='retrievePass'),
	url(r'^forgotPass1$', views.forgotPass1, name='forgotPass1'),
	url(r'^forgotPass2$', views.forgotPass2, name='forgotPass2'),
	url(r'^forgotPassMail$', views.forgotPassMail, name='forgotPassMail'),
	url(r'^contactus$', views.contactus, name='contactus'),

	url(r'^danjiban$', views.danjiban, name='danjiban'),

	url(r'^onsystem$', views.onsystem, name='onsystem'),

	url(r'^shownews$', views.shownews, name='shownews'),
	url(r'^newsdetail$', views.newsdetail, name='newsdetail'),
	url(r'^mianze$', views.mianze, name='mianze'),
	)