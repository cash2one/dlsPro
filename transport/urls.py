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
	url(r'^index$', views.index, name='index'),
	#处理 checkup
	url(r'^checkup$', views.checkup, name='checkup'),
	url(r'^check_eq$', views.check_eq, name='checkup_eq'),
	url(r'^checkup2$', views.checkup2, name='checkup2'),
	url(r'^checkup3$', views.checkup3, name='checkup3'),
	url(r'^checkup4$', views.checkup4, name='checkup4'),
	url(r'^checkup5$', views.checkup5, name='checkup5'),
	url(r'^check5save$', views.check5save, name='check5save'),
	url(r'^checkup6$', views.checkup6, name='checkup6'),
	#处理 count
	url(r'^count$', views.count, name='count'),
	url(r'^countAjax$', views.countAjax, name='countAjax'),
	url(r'^countMap$', views.countMap, name='countMap'),
	url(r'^countCharts_sj$', views.countCharts_sj, name='countCharts_sj'),
	url(r'^countCharts_use$', views.countCharts_use, name='countCharts_use'),
	url(r'^countCharts_sf$', views.countCharts_sf, name='countCharts_sf'),
	url(r'^ditu$', views.ditu, name='ditu'),

	#处理 user
	url(r'^user$', views.user, name='user'),
	url(r'^edituser$', views.edituser, name='edituser'),
	url(r'^editpass$', views.editpass, name='editpass'),
	url(r'^propass$', views.propass, name='propass'),
	url(r'^message$', views.message, name='message'),
	#帮助
	url(r'^help$', views.help, name='help'),
	url(r'^helpcontent.html$', views.helpcontent, name='helpcontent'),
	#编辑
	url(r'^edit/*$', views.build_result_edit, name='edit'),
	#delete
	url(r'^delete_build.*$', views.delete_build, name='delete'),


	url(r'^export_xls.*$', views.export_xls, name='export_xls'),
	url(r'^downloadpdf$', views.downloadpdf, name='downloadpdf'),
	url(r'^readFile$', views.readFile, name='readFile'),
	# url(r'^pdf_head$', views.pdf_head, name='pdf_head'),
	url(r'^dlcompdf$', views.dlcompdf, name='dlcompdf'),
	url(r'^pdfdata$', views.pdfdata, name='pdfdata'),
	url(r'^changedata$', views.changedata, name='changedata'),
	#实验
	#实验
	url(r'^test$', views.test, name='test'),
	)