#coding:utf-8
from django.contrib import admin
from transport.models import user_role,sys_user,role,EQInfo,building_usage,building_information,region,building_structure,environment,damage,result


class sys_userAdmin(admin.ModelAdmin):
	fields = ['user_name','user_password','user_isenabled','user_realname','user_profession','user_zipcode','user_org','user_deputy','user_address','user_telnum','user_email','user_accountcreatetime','user_updatetime']
	list_display = ['user_name','user_password','user_isenabled','user_realname','user_profession','user_zipcode','user_org','user_deputy','user_address','user_telnum','user_email','user_accountcreatetime','user_updatetime']
	search_fields = ['user_name']


class user_roleAdmin(admin.ModelAdmin):
	fields = ['user_name','role_name']
	list_display = ['user_name','role_name']
	search_fields = ['user_name']


class roleAdmin(admin.ModelAdmin):
	fields = ['role_name','role_desc','role_function','role_dataaccess']
	list_display = ['role_name','role_desc','role_function','role_dataaccess']
	search_fields = ['role_name']


class EQInfoAdmin(admin.ModelAdmin):
	fields = ['eq_id','eq_num','eq_name','eq_date','eq_time','eq_location','eq_lon','eq_lat','eq_ms','eq_depth','eq_maxintensity','eq_focalmechanism','eq_desc','create_time','user']
	list_display = ['eq_id','eq_num','eq_name','eq_date','eq_time','eq_location','eq_lon','eq_lat','eq_ms','eq_depth','eq_maxintensity','eq_focalmechanism','eq_desc','create_time','user']
	search_fields = ['eq_name']
#building_information
class building_informationAdmin(admin.ModelAdmin):
	fields = ['building_id','building_block','building_name','building_host','building_year','building_area','building_layernumupground','building_layernumunderground','building_layerofnum','building_longitude','building_latitude','building_location','building_admindivcode','building_regionname','building_fortificationIntensity','building_strcture','usage_name','eq_num','user_id','createTime','updateTime']
	list_display =  ['building_id','building_block','building_name','building_host','building_year','building_area','building_layernumupground','building_layernumunderground','building_layerofnum','building_longitude','building_latitude','building_location','building_admindivcode','building_regionname','building_fortificationIntensity','building_strcture','usage_name','eq_num','user_id','createTime','updateTime']
	search_fields = ['building_name']


class building_usageAdmin(admin.ModelAdmin):
	fields = ['usage_id','usage_name','usage_desc']
	list_display =  ['usage_id','usage_name','usage_desc']
	search_fields = ['usage_name']

class regionAdmin(admin.ModelAdmin):
	fields = ['region_id','region_name','region_desc']
	list_display =  ['region_id','region_name','region_desc']
	search_fields = ['region_name']

class building_structureAdmin(admin.ModelAdmin):
	fields = ['strutype_id','strutype_name','strutype_desc','strutype_enname','strutype_examplephoto']
	list_display =   ['strutype_id','strutype_name','strutype_desc','strutype_enname','strutype_examplephoto']
	search_fields = ['strutype_name']

class environmentAdmin(admin.ModelAdmin):
	fields = ['environment_id','environment_fieldeffect','environment_fieldnote','building_id']
	list_display =  ['environment_id','environment_fieldeffect','environment_fieldnote','building_id']
	search_fields = ['environment_fieldeffect']

class resultAdmin(admin.ModelAdmin):
	fields = ['result_id','result_isusable','result_damageindex','result_damagelevel','result_evaluatedate','user_id','building_id']
	list_display =  ['result_id','result_isusable','result_damageindex','result_damagelevel','result_evaluatedate','user_id','building_id']
	search_fields = ['result_id']


admin.site.register(sys_user,sys_userAdmin)
admin.site.register(user_role,user_roleAdmin)
admin.site.register(EQInfo,EQInfoAdmin)
admin.site.register(building_information,building_informationAdmin)
admin.site.register(building_usage,building_usageAdmin)
admin.site.register(region,regionAdmin)
admin.site.register(building_structure,building_structureAdmin)
admin.site.register(environment,environmentAdmin)
admin.site.register(role,roleAdmin)
# admin.site.register(damage,damageAdmin)
admin.site.register(result,resultAdmin)