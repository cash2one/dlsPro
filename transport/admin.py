#coding:utf-8
from django.contrib import admin
from transport.models import *

class t_adminAdmin(admin.ModelAdmin):
	fields = ['admin_id','admin_loginname','admin_loginpwd','admin_name','admin_remark']
	list_display = ['admin_id','admin_loginname','admin_loginpwd','admin_name','admin_remark']
	search_fields = ['admin_name']



class sys_userAdmin(admin.ModelAdmin):
	fields = ['user_id','user_realname','user_idcard','user_major','user_workunit','user_title','user_address','user_postcode','user_email','user_tel','user_pac','user_state','user_name','user_password','user_remark','user_createtime','user_updatetime','user_lastip','user_logincount']
	list_display = ['user_id','user_realname','user_idcard','user_major','user_workunit','user_title','user_address','user_postcode','user_email','user_tel','user_pac','user_state','user_name','user_password','user_remark','user_createtime','user_updatetime','user_lastip','user_logincount']
	search_fields = ['user_name']


class EQInfoAdmin(admin.ModelAdmin):
	fields = ['eq_earthquakeid','eq_earthquakename','eq_date','eq_time','eq_location','eq_focallongitude','eq_focallatitude','eq_magnitude','eq_focaldepth','eq_epicentralintensity','eq_focalmechanism','eq_createtime','eq_adminid','eq_remark']
	list_display =['eq_earthquakeid','eq_earthquakename','eq_date','eq_time','eq_location','eq_focallongitude','eq_focallatitude','eq_magnitude','eq_focaldepth','eq_epicentralintensity','eq_focalmechanism','eq_createtime','eq_adminid','eq_remark']
	search_fields = ['eq_earthquakename']

class regionAdmin(admin.ModelAdmin):
	fields = ['region_number','region_name','region_location','region_desc','region_remark']
	list_display =  ['region_number','region_name','region_location','region_desc','region_remark']
	search_fields = ['region_name']


class building_structureAdmin(admin.ModelAdmin):
	fields = ['construct_typeid','construct_typename','construct_typedes','construct_remark']
	list_display =   ['construct_typeid','construct_typename','construct_remark']
	search_fields = ['construct_typename']



class building_usageAdmin(admin.ModelAdmin):
	fields = ['building_usageid','building_usagename','building_usagedesc']
	list_display =  ['building_usageid','building_usagename','building_usagedesc']
	search_fields = ['building_usagename']



class building_informationAdmin(admin.ModelAdmin):
	fields = ['building_buildnumber','building_number','building_buildname','building_uplayernum','building_downlayernum','building_partlayernum','building_househostname','building_buildyear','building_buildarea','building_constructtypeid','building_buildusage','building_longitude','building_latitude','building_province','building_city','building_district','building_locationdetail','building_admregioncode','building_areanumber','building_fortificationinfo','building_fortificationdegree','building_earthquakeid','building_userid','building_remark','building_createtime','buidling_updatetime']
	list_display =  ['building_buildnumber','building_number','building_buildname','building_uplayernum','building_downlayernum','building_partlayernum','building_househostname','building_buildyear','building_buildarea','building_constructtypeid','building_buildusage','building_longitude','building_latitude','building_province','building_city','building_district','building_locationdetail','building_admregioncode','building_areanumber','building_fortificationinfo','building_fortificationdegree','building_earthquakeid','building_userid','building_remark','building_createtime','buidling_updatetime']
	search_fields = ['building_buildname']


class field_effectAdmin(admin.ModelAdmin):
	fields = ['effect_id','effect_name','effect_desc']
	list_display =  ['effect_id','effect_name','effect_desc']
	search_fields = ['effect_name']

class foundation_statusAdmin(admin.ModelAdmin):
	fields = ['status_id','status_name','status_desc']
	list_display =  ['status_id','status_name','status_desc']
	search_fields = ['status_name']


class environmentAdmin(admin.ModelAdmin):
	#fields = ['environment_buildnumber','environment_name','environment_earthquakeeff','environment_foundation','environment_adjoinbuild','environment_seismicintensity','environment_smallaffect','environment_bigaffect','environment_remark']
	list_display =  ['environment_buildnumber','environment_earthquakeeff','environment_foundation','environment_adjoinbuild','environment_seismicintensity','environment_smallaffect','environment_bigaffect','environment_remark']
	search_fields = ['environment_bigaffect']

class buildlocationAdmin(admin.ModelAdmin):
	fields = ['location_id','location_constructtype','location_name','location_desc','location_seqnumber','location_remark']
	list_display =  ['location_id','location_constructtype','location_name','location_desc','location_seqnumber','location_remark']
	search_fields = ['location_name']


class SubLocationCatalogAdmin(admin.ModelAdmin):
	fields = ['catalog_id','catalog_constructtypeid','catalog_locationid','catalog_name','catalog_des','catalog_seqnumber','catalog_remark']
	list_display = ['catalog_id','catalog_constructtypeid','catalog_locationid','catalog_name','catalog_des','catalog_seqnumber','catalog_remark']
	search_fields = ['catalog_name']


class sublocalAdmin(admin.ModelAdmin):
	fields = ['sublocal_id','sublocal_constructtypeid','sublocal_locationid','sublocal_sublocationcatalog','sublocal_name','sublocal_helpid','sublocal_seqnumber','sublocal_remark']
	list_display =  ['sublocal_id','sublocal_constructtypeid','sublocal_locationid','sublocal_sublocationcatalog','sublocal_name','sublocal_helpid','sublocal_seqnumber','sublocal_remark']
	search_fields = ['sublocal_id']






class damageAdmin(admin.ModelAdmin):
	fields = ['damage_id','damage_buildnumber','damage_constructtypeid','damage_locationid','damage_catalogid','damage_sublocationid','damage_number','damage_degree','damage_parameteradjust','damage_description','damage_remark','damage_isfirst']
	list_display = ['damage_id','damage_buildnumber','damage_constructtypeid','damage_locationid','damage_catalogid','damage_sublocationid','damage_number','damage_degree','damage_parameteradjust','damage_description','damage_remark','damage_isfirst']
	search_fields = ['damage_buildnumber']


class identify_resultAdmin(admin.ModelAdmin):
	fields = ['result_buildnumber','result_id','result_securitycategory','result_totaldamageindex','result_damagedegree','result_assetdate','result_remark']
	list_display =  ['result_buildnumber','result_securitycategory','result_totaldamageindex','result_damagedegree','result_assetdate','result_remark']
	search_fields = ['result_buildnumber']


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

class buildImageAdmin(admin.ModelAdmin):
	fields = ['buildid','frontimage','backimage','leftimage','rightimage','topimage','innerimage']
	list_display =  ['buildid','frontimage','backimage','leftimage','rightimage','topimage','innerimage']
	search_fields = ['buildid']

class areaAdmin(admin.ModelAdmin):



	fields = ['area_id','area_name','area_content']
	list_display = ['area_id','area_name','area_content']
	search_fields = ['area_name']


admin.site.register(sys_user,sys_userAdmin)
admin.site.register(EQInfo,EQInfoAdmin)
admin.site.register(building_information,building_informationAdmin)
admin.site.register(region,regionAdmin)
admin.site.register(building_structure,building_structureAdmin)
admin.site.register(building_usage,building_usageAdmin)
admin.site.register(environment,environmentAdmin)
admin.site.register(identify_result,identify_resultAdmin)

admin.site.register(SubLocationCatalog,SubLocationCatalogAdmin)
admin.site.register(buildlocation,buildlocationAdmin)
admin.site.register(foundation_status,foundation_statusAdmin)
admin.site.register(field_effect,field_effectAdmin)
admin.site.register(helpco,helpcoAdmin)
admin.site.register(helptitle,helptitleAdmin)
admin.site.register(news,newsAdmin)
admin.site.register(option,optionAdmin)
admin.site.register(sublocal,sublocalAdmin)
admin.site.register(t_admin,t_adminAdmin)
admin.site.register(damage,damageAdmin)
admin.site.register(buildImage,buildImageAdmin)
admin.site.register(area,areaAdmin)