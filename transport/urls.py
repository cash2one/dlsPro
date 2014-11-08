# coding=utf-8
from django.conf.urls import patterns, url
from transport import views

urlpatterns = patterns('',
	
	url(r'^register$', views.register, name='register'),

	url(r'^register_info1/$',views.register_info1,name='register_info1'),
	url(r'^register_info2/$',views.register_info2,name='register_info2'),
	url(r'^register_activate1$',views.activate1,name='activate1'),
	url(r'^register_activate2$',views.activate2,name='activate2'),
	url(r'^exit$', views.exit, name='exit'),
	url(r'^$', views.login, name='login'),
	url(r'^login_va/$', views.login_va, name='login_va'),
	url(r'^index$', views.index, name='index'),
	#chu li checkup
	url(r'^checkup$', views.checkup, name='checkup'),
	url(r'^check_eq$', views.check_eq, name='checkup_eq'),
	url(r'^checkup2$', views.checkup2, name='checkup2'),
	url(r'^checkup3$', views.checkup3, name='checkup3'),
	url(r'^checkup4$', views.checkup4, name='checkup4'),
	url(r'^checkup5$', views.checkup5, name='checkup5'),
	url(r'^checkup6$', views.checkup6, name='checkup6'),
	#chu li count
	url(r'^count$', views.count, name='count'),
	url(r'^ditu$', views.ditu, name='ditu'),
	#chu li user
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
	)