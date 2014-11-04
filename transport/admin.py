#coding:utf-8
from django.contrib import admin
from transport.models import sys_user,EQInfo,building_structure,building_information,region,environment,damage,result,t_admin,sublocal,option,news,helptitle,helpco

class sys_userAdmin(admin.ModelAdmin):
	fields = ['user_id','user_realname','user_idcard','user_major','user_workunit','user_title','user_address','user_postcode','user_emall','user_tel','user_pac','user_state','user_name','user_password','user_remark']
	list_display = ['user_id','user_realname','user_idcard','user_major','user_workunit','user_title','user_address','user_postcode','user_emall','user_tel','user_pac','user_state','user_name','user_password','user_remark']
	search_fields = ['user_name']


class EQInfoAdmin(admin.ModelAdmin):
	fields = ['eq_earthquakeid','eq_earthquakename','eq_time','eq_location','eq_focallongitude','eq_focallatitude','eq_magnitude','eq_focaldepth','eq_epicentralIntensity','eq_remark']
	list_display = ['eq_earthquakeid','eq_earthquakename','eq_time','eq_location','eq_focallongitude','eq_focallatitude','eq_magnitude','eq_focaldepth','eq_epicentralIntensity','eq_remark']
	search_fields = ['eq_earthquakename']

#building_information
class building_informationAdmin(admin.ModelAdmin):
	fields = ['building_buildnumber','building_number','building_buildname','building_uplayernum','building_downlayernum','building_partlayernum','building_househostname','building_buildyear','building_buildarea','building_constructtypeid','building_buildusage','building_longitude','building_latitude','building_province','building_city','building_district','building_locationdetail','building_admregioncode','building_areanumber','building_fortificationinfo','building_fortificationdegree','building_earthquakeid','building_userid','building_remark']
	list_display =  ['building_buildnumber','building_number','building_buildname','building_uplayernum','building_downlayernum','building_partlayernum','building_househostname','building_buildyear','building_buildarea','building_constructtypeid','building_buildusage','building_longitude','building_latitude','building_province','building_city','building_district','building_locationdetail','building_admregioncode','building_areanumber','building_fortificationinfo','building_fortificationdegree','building_earthquakeid','building_userid','building_remark']
	search_fields = ['building_buildname']


class regionAdmin(admin.ModelAdmin):
	fields = ['region_areanumber','region_areaname','region_arealocation','region_areadesc','region_remark']
	list_display =  ['region_areanumber','region_areaname','region_arealocation','region_areadesc','region_remark']
	search_fields = ['region_areaname']

class building_structureAdmin(admin.ModelAdmin):
	fields = ['construct_typeid','construct_typename','construct_typedes','construct_remark']
	list_display =   ['construct_typeid','construct_typename','construct_typedes','construct_remark']
	search_fields = ['construct_typename']

class environmentAdmin(admin.ModelAdmin):
	fields = ['environment_buildnumber','environment_foundation','environment_adjoinbuild','environment_seismicintensity','environment_smallaffect','environment_bigaffect','environment_remark']
	list_display =  ['environment_buildnumber','environment_foundation','environment_adjoinbuild','environment_seismicintensity','environment_smallaffect','environment_bigaffect','environment_remark']
	search_fields = ['environment_buildnumber']

class resultAdmin(admin.ModelAdmin):
	fields = ['result_buildnumber','result_securitycategory','result_totaldamageindex','result_damagedegree','result_assetdate','result_remark']
	list_display =  ['result_buildnumber','result_securitycategory','result_totaldamageindex','result_damagedegree','result_assetdate','result_remark']
	search_fields = ['result_buildnumber']


class damageAdmin(admin.ModelAdmin):
	fields = ['damage_buildnumber','damage_constructtypeid','damage_locationid','damage_sublocationid',
	'damage_number','damage_degree','damage_sublocationfactor','damage_description','damage_remark']
	list_display = ['damage_buildnumber','damage_constructtypeid','damage_locationid','damage_sublocationid',
	'damage_number','damage_degree','damage_sublocationfactor','damage_description','damage_remark']
	search_fields = ['damage_buildnumber']

class t_adminAdmin(admin.ModelAdmin):
	fields = ['admin_adminid','admin_adminloginname','admin_adminloginpwd','admin_adminname','admin_remark']
	list_display = ['admin_adminid','admin_adminloginname','admin_adminloginpwd','admin_adminname','admin_remark']
	search_fields = ['admin_adminname']

class sublocalAdmin(admin.ModelAdmin):
	fields = ['sublocal_sublocationid','sublocal_constructTypeid','sublocal_locationname','sublocal_sublocationcatalog','sublocal_sublocationname'
	,'sublocal_helpid','sublocal_seqnumber','sublocal_remark']
	list_display = ['sublocal_sublocationid','sublocal_constructTypeid','sublocal_locationname','sublocal_sublocationcatalog','sublocal_sublocationname'
	,'sublocal_helpid','sublocal_seqnumber','sublocal_remark']
	search_fields = ['sublocal_sublocationid']

class optionAdmin(admin.ModelAdmin):
	fields = ['option_opttagname','option_opttagvalue','option_remark']
	list_display = ['option_opttagname','option_opttagvalue','option_remark']
	search_fields = ['option_opttagname']


class newsAdmin(admin.ModelAdmin):
	fields = ['news_newsid','news_newstitle','news_newscontent','news_adddate','news_addperson','news_remark']
	list_display = ['news_newsid','news_newstitle','news_newscontent','news_adddate','news_addperson','news_remark']
	search_fields = ['news_newstitle']

class helptitleAdmin(admin.ModelAdmin):
	fields = ['helpti_helptitleid','helpti_titlename','helpti_titleparentid','helpti_seqnumber','helpti_remark']
	list_display = ['helpti_helptitleid','helpti_titlename','helpti_titleparentid','helpti_seqnumber','helpti_remark']
	search_fields = ['helpti_helptitleid']

class helpcoAdmin(admin.ModelAdmin):
	fields = ['helpco_helptitleid','helpco_helpcontent','helpco_remark']
	list_display =  ['helpco_helptitleid','helpco_helpcontent','helpco_remark']
	search_fields = ['helpco_helptitleid']

admin.site.register(sys_user,sys_userAdmin)
admin.site.register(EQInfo,EQInfoAdmin)
admin.site.register(building_information,building_informationAdmin)
admin.site.register(region,regionAdmin)
admin.site.register(building_structure,building_structureAdmin)
admin.site.register(environment,environmentAdmin)
admin.site.register(result,resultAdmin)

admin.site.register(helpco,helpcoAdmin)
admin.site.register(helptitle,helptitleAdmin)
admin.site.register(news,newsAdmin)
admin.site.register(option,optionAdmin)
admin.site.register(sublocal,sublocalAdmin)
admin.site.register(t_admin,t_adminAdmin)
admin.site.register(damage,damageAdmin)