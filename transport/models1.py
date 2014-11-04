#coding:utf-8
from django.db import models
# import simplejson as json
# Create your models here.
'''
用户表
'''
class sys_user(models.Model):
	# user_id = models.CharField(max_length=64,verbose_name='用户编号')
	user_name = models.CharField(max_length=64,verbose_name='用户名',unique=True)
	user_password = models.CharField(max_length=64,verbose_name='用户密码')
	user_isenabled = models.IntegerField(verbose_name='账号是否可用')
	user_realname = models.CharField(max_length=64,verbose_name='真实姓名')
	user_profession = models.CharField(max_length=64,verbose_name='用户行业')
	user_deputy = models.CharField(max_length=64,verbose_name='用户职称')
	user_org = models.CharField(max_length=128,verbose_name='用户单位')
	user_address = models.CharField(max_length=512,verbose_name='用户通讯地址')
	user_zipcode = models.IntegerField(verbose_name='邮政编码')
	user_telnum = models.CharField(max_length=30,verbose_name='电话号码')
	user_email = models.EmailField(verbose_name='Email',unique=True)
	user_accountcreatetime = models.DateField(verbose_name='账户创建时间')
	user_updatetime =  models.DateField(verbose_name='账户时间')

	def __unicode__(self):
		return self.user_name

	class Meta:
		verbose_name = '用户信息'
		verbose_name_plural = '用户信息'




'''
角色信息表 
'''
class role(models.Model):
	# role_id = models.CharField(max_length=64,verbose_name='角色编号')
	role_name = models.CharField(max_length=64,verbose_name='角色名称',unique=True)
	role_desc = models.CharField(max_length=512,verbose_name='角色描述')
	role_function = models.CharField(max_length=64,verbose_name='功能权限')
	role_dataaccess = models.CharField(max_length=64,verbose_name='数据访问权限')

	def __unicode__(self):
		return self.role_name

	class Meta:
		verbose_name = '角色信息'
		verbose_name_plural = '角色信息'


'''
user_角色信息表 
'''
class user_role(models.Model):
	user_name = models.ForeignKey(sys_user,verbose_name='用户编号')
	role_name = models.ForeignKey(role,verbose_name='角色编号')

	def __unicode__(self):
		return self.user_name

	class Meta:
		verbose_name = '角色信息'
		verbose_name_plural = '角色信息'

'''
地震信息表 
'''
class EQInfo(models.Model):
	eq_id = models.CharField(max_length=64,unique=True)
	eq_num = models.CharField(max_length=64,verbose_name='地震编号')
	eq_name = models.CharField(max_length=64,verbose_name='地震名称')
	eq_date =  models.DateField(verbose_name='地震日期')
	eq_time =  models.DateField(verbose_name='地震时间')
	eq_location = models.CharField(max_length=64,verbose_name='发震地点')
	eq_lon = models.DecimalField(max_digits=15,decimal_places=5,verbose_name='震源经度')
	eq_lat = models.DecimalField(max_digits=15,decimal_places=5,verbose_name='震源纬度')
	eq_ms = models.DecimalField(max_digits=15,decimal_places=5,verbose_name='震级')
	eq_depth = models.DecimalField(max_digits=15,decimal_places=5,verbose_name='震源深度')
	eq_maxintensity = models.DecimalField(max_digits=15,decimal_places=5,verbose_name='中心烈度')
	eq_focalmechanism = models.CharField(max_length=1024,verbose_name='震源机制')
	eq_desc = models.CharField(max_length=64,verbose_name='备注说明')
	create_time = models.DateField(verbose_name='创建时间')
	user = models.ForeignKey(sys_user,verbose_name='用户名称')
	# user_name = models.ForeignKey(sys_user,verbose_name='用户名称')

	def __unicode__(self):
		return self.eq_name

	class Meta:
		verbose_name = '地震信息'
		verbose_name_plural = '地震信息'




'''
建筑物用途
'''
class building_usage(models.Model):
	usage_id = models.CharField(max_length=64,verbose_name='用途编号',unique=True)
	usage_name = models.CharField(max_length=64,verbose_name='建筑物用途')
	usage_desc = models.CharField(max_length=64,verbose_name='建筑物用途描述')


	def __unicode__(self):
		return self.usage_name

	class Meta:
		verbose_name = '建筑物用途'
		verbose_name_plural = '建筑物用途'



'''
结构类型
'''
class building_structure(models.Model):
	strutype_id = models.CharField(max_length=64,verbose_name='结构类型编号',unique=True)
	strutype_name = models.CharField(max_length=64,verbose_name='结构类型名称')
	strutype_desc = models.CharField(max_length=64,verbose_name='结构类型描述')
	strutype_enname = models.CharField(max_length=64,verbose_name='结构类型E文简称')
	strutype_examplephoto = models.ImageField(upload_to='./DisPro/static/img/')
	def __unicode__(self):
		return self.strutype_name

	class Meta:
		verbose_name = '结构类型'
		verbose_name_plural = '结构类型'



'''
建筑物基本信息
'''
class building_information(models.Model):
	building_id = models.CharField(max_length=64,verbose_name='建筑物编号',unique=True)
	building_block = models.IntegerField(verbose_name='建筑物栋数')
	building_name = models.CharField(max_length=64,verbose_name='建筑物名称')
	building_host =  models.CharField(max_length=64,verbose_name='房主')
	building_year =  models.CharField(max_length=64,verbose_name='建成年份')
	building_area = models.DecimalField(max_digits=15,decimal_places=5,verbose_name='建筑面积')
	building_layernumupground = models.DecimalField(max_digits=15,decimal_places=5,verbose_name='建筑物层数地上主体')
	building_layernumunderground = models.DecimalField(max_digits=15,decimal_places=5,verbose_name='建筑物层数地下主体')
	building_layerofnum = models.DecimalField(max_digits=15,decimal_places=5,verbose_name='建筑物层数局部层数')
	building_longitude = models.DecimalField(max_digits=15,decimal_places=5,verbose_name='中心经度')
	building_latitude = models.DecimalField(max_digits=15,decimal_places=5,verbose_name='中心纬度')
	building_location = models.CharField(max_length=64,verbose_name='建筑物地点')
	building_admindivcode = models.CharField(max_length=64,verbose_name='行政区编码')
	building_regionname = models.CharField(max_length=64,verbose_name='区域名称')
	building_fortificationIntensity = models.CharField(max_length=64,verbose_name='抗震设防状况')
	building_strcture = models.ForeignKey(building_structure,verbose_name='结构类型')
	usage_name = models.ForeignKey(building_usage,verbose_name='建筑物用途')#error??????
	eq_num = models.ForeignKey(EQInfo,verbose_name='地震编号')
	user_id = models.ForeignKey(sys_user,verbose_name='鉴定人员编号')
	createTime = models.DateField(verbose_name='创建时间')
	updateTime = models.DateField(verbose_name='最后更新时间')

	def __unicode__(self):
		return self.building_name

	class Meta:
		verbose_name = '建筑物基本信息'
		verbose_name_plural = '建筑物基本信息'


'''
地区
'''
class region(models.Model):
	region_id = models.CharField(max_length=64,verbose_name='区域编号',unique=True)
	region_name = models.CharField(max_length=64,verbose_name='区域名称')
	region_desc = models.CharField(max_length=64,verbose_name='区域描述')


	def __unicode__(self):
		return self.region_name

	class Meta:
		verbose_name = '地区'
		verbose_name_plural = '地区'




'''
环境信息
'''
class environment(models.Model):
	environment_id = models.CharField(max_length=64,verbose_name='编号',unique=True)
	environment_fieldeffect = models.CharField(max_length=64,verbose_name='场地影响')
	environment_fieldnote = models.CharField(max_length=512,verbose_name='场地影响备注')
	environment_foundationstatus = models.CharField(max_length=64,verbose_name='地基状况')
	environment_foundationnote = models.CharField(max_length=512,verbose_name='地基状况备注')
	environment_isadjacenteffect =  models.CharField(max_length=64,verbose_name='毗邻影响')
	environment_adjacentnote = models.CharField(max_length=512,verbose_name='毗邻影响备注')
	building_id = models.ForeignKey(building_information,verbose_name='建筑物id')

	def __unicode__(self):
		return self.environment_id

	class Meta:
		verbose_name = '环境信息'
		verbose_name_plural = '环境信息'


'''
细部震损数据表 
'''
class damage(models.Model):
	building_id = models.ForeignKey(building_information,verbose_name='建筑物id',unique=True)
	building_member = models.CharField(max_length=64,verbose_name='建筑物部位')
	building_memberfactor = models.CharField(max_length=512,verbose_name='建筑物部位因子')
	building_damagestatus = models.CharField(max_length=64,verbose_name='震损状态')
	building_prameteradjust = models.DecimalField(max_digits=15,decimal_places=5,verbose_name='参数微调')
	building_description = models.DecimalField(max_digits=15,decimal_places=5,verbose_name='描述')
	

	def __unicode__(self):
		return self.environment_id

	class Meta:
		verbose_name = '环境信息'
		verbose_name_plural = '环境信息'


'''
建筑物安全鉴定结果信息数据表 
'''
class result(models.Model):
	result_id = models.CharField(max_length=64,verbose_name='鉴定结果编号',unique=True)
	result_isusable = models.CharField(max_length=64,verbose_name='鉴定后是否可用')
	result_damageindex = models.DecimalField(max_digits=15,decimal_places=5,verbose_name='整体震损指数')
	result_damagelevel = models.CharField(max_length=64,verbose_name='破坏等级')
	result_evaluatedate = models.DateField(verbose_name='鉴定日期')
	user_id = models.ForeignKey(sys_user,verbose_name='鉴定人员编号')
	building_id = models.ForeignKey(building_information,verbose_name='建筑物编号')

	def __unicode__(self):
		return self.result_id

	class Meta:
		verbose_name = '建筑物安全鉴定结果信'
		verbose_name_plural = '建筑物安全鉴定结果信'
