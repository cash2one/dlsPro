#coding:utf-8
from django.db import models
# import simplejson as json
# Create your models here.



'''
管理用户表 T_Admin
'''
class t_admin(models.Model):
	admin_id = models.CharField(max_length=32,verbose_name='用户编号',unique=True)
	admin_loginname = models.CharField(max_length=20,verbose_name='登陆用户名')
	admin_loginpwd = models.CharField(max_length=32,verbose_name='登录密码')
	admin_name = models.CharField(max_length=10,verbose_name='用户姓名',blank=True,null=True)
	admin_remark = models.CharField(max_length=50,verbose_name='备注',blank=True,null=True)

	def __unicode__(self):
		return self.admin_name
	 
	class Meta:
		verbose_name = '管理用户信息'
		verbose_name_plural = '管理用户信息'


'''
用户信息表 T-UserInfo
'''
class sys_user(models.Model):
	user_id = models.CharField(max_length=32,verbose_name='用户编号',unique=True)
	user_role = models.CharField(max_length=32,verbose_name='用户角色')
	user_realname = models.CharField(max_length=20,verbose_name='姓名')
	user_idcard = models.CharField(max_length=20,verbose_name='身份证号',blank=True,null=True)
	user_major = models.CharField(max_length=50,verbose_name='专业',blank=True,null=True)
	user_workunit = models.CharField(max_length=50,verbose_name='单位',blank=True,null=True)
	user_title = models.CharField(max_length=20,verbose_name='职称',blank=True,null=True)
	user_address = models.CharField(max_length=50,verbose_name='通信地址',blank=True,null=True)
	user_postcode = models.CharField(max_length=6,verbose_name='邮政编码',blank=True,null=True)
	user_email = models.CharField(max_length=30,verbose_name='用户邮箱',blank=True,null=True)
	user_tel = models.CharField(max_length=15,verbose_name='电话号码',blank=True,null=True)
	user_pac = models.CharField(max_length=32,verbose_name='激活码',blank=True,null=True)
	user_state = models.CharField(max_length=10,verbose_name='用户状态')
	user_name = models.CharField(max_length=20,verbose_name='登录用户名')
	user_password = models.CharField(max_length=32,verbose_name='登录密码')
	user_remark = models.CharField(max_length=50,verbose_name='备注',blank=True,null=True)
	user_createtime = models.DateField(verbose_name="账户创建时间",blank=True,null=True)
	user_updatetime = models.DateField(verbose_name="最后修改时间",blank=True,null=True)
	user_currenthost = models.CharField(max_length="64",verbose_name="当前登录主机",blank=True,null=True)
	user_lastip = models.CharField(max_length="64",verbose_name="上次登陆IP",blank=True,null=True)
	user_ip = models.CharField(max_length="64",verbose_name="登陆IP",blank=True,null=True)
	user_logincount = models.CharField(max_length="32",verbose_name="登陆次数",blank=True,null=True)
	user_logintime = models.DateTimeField(verbose_name="用户登陆时间",blank=True,null=True)
	user_lastlogintime = models.DateTimeField(verbose_name="用户登陆时间",blank=True,null=True)
	user_lastalivetime = models.DateTimeField(verbose_name="用户最后活动时间",blank=True,null=True)
	user_loginaddress = models.CharField(max_length="32",verbose_name="登陆地点",blank=True,null=True)
	user_loginlastaddress = models.CharField(max_length="32",verbose_name="上次登录地点",blank=True,null=True)

	def __unicode__(self):
		return self.user_realname

	class Meta:
		verbose_name = '用户信息'
		verbose_name_plural = '用户信息'






'''
登陆统计表 T-logincount
'''
class loginCount(models.Model):
	login_user = models.ForeignKey(sys_user,verbose_name='登陆用户')
	login_ip = models.CharField(max_length=30,verbose_name='用户访问ip')
	login_location = models.CharField(max_length=30,verbose_name='用户登陆地点')
	login_time = models.DateTimeField(auto_now_add=True,verbose_name="用户登陆时间")
	login_date = models.DateField(auto_now_add=True,verbose_name="用户登陆时间")

	def __unicode__(self):
		return self.login_user

	class Meta:
		verbose_name = '用户登录信息记录'
		verbose_name_plural = '用户登录信息记录'
		ordering = ['-login_time']



'''
用户位置信息表 T-logincount
'''
class userLocation(models.Model):
	loc_user = models.ForeignKey(sys_user,verbose_name='用户')
	loc_longitude = models.FloatField(verbose_name='用户所在经度',blank=True,null=True)
	loc_latitude = models.FloatField(verbose_name='用户所在纬度',blank=True,null=True)
	last_time = models.DateField(auto_now=True,verbose_name="用户登陆时间")

	def __unicode__(self):
		return self.loc_user

	class Meta:
		verbose_name = '用户位置信息记录'
		verbose_name_plural = '用户位置信息记录'

'''
地震信息表 T-Earthquake
'''
class EQInfo(models.Model):
	eq_earthquakeid = models.CharField(max_length=30,verbose_name='地震编号',unique=True)
	eq_earthquakename = models.CharField(max_length=30,verbose_name='地震名称')
	eq_date = models.DateField(verbose_name='发震日期',blank=True,null=True)
	eq_time = models.TimeField(verbose_name='发震时间',blank=True,null=True)
	eq_location = models.CharField(max_length=100,verbose_name='发生地点',blank=True,null=True)
	eq_focallongitude = models.FloatField(verbose_name='震源经度',blank=True,null=True)
	eq_focallatitude = models.FloatField(verbose_name='震源纬度',blank=True,null=True)
	eq_magnitude = models.IntegerField(verbose_name='震级(里氏)',blank=True,null=True)
	eq_focaldepth = models.IntegerField(verbose_name='震源深度（KM）',blank=True,null=True)
	eq_epicentralintensity = models.CharField(max_length=10,verbose_name='震中烈度',blank=True,null=True)
	eq_focalmechanism = models.CharField(max_length=1024,verbose_name='震中烈度',blank=True,null=True)
	eq_createtime = models.DateField(verbose_name="创建时间")
	eq_adminid = models.ForeignKey(t_admin,verbose_name="创建人")
	eq_remark = models.CharField(max_length=30,verbose_name='备注',blank=True,null=True)

	def __unicode__(self):
		return self.eq_earthquakename

	class Meta:
		verbose_name = '地震信息'
		verbose_name_plural = '地震信息'




'''
参数地区表 T_ParamAreas
'''
class region(models.Model):
	region_number = models.CharField(max_length=32,verbose_name='地区编号',unique=True)
	region_name = models.CharField(max_length=20,verbose_name='区域名称')
	region_location = models.CharField(max_length=100,verbose_name='地理位置')
	region_desc = models.CharField(max_length=50,verbose_name='区域描述',blank=True,null=True)
	region_remark = models.CharField(max_length=50,verbose_name='备注',blank=True,null=True)


	def __unicode__(self):
		return self.region_location

	class Meta:
		verbose_name = '参数地区'
		verbose_name_plural = '参数地区'



'''
建筑物的结构类型表 T_BuildingConstructionType
'''
class building_structure(models.Model):
	construct_typeid = models.CharField(max_length=20,verbose_name='类型id',unique=True)
	construct_typename = models.CharField(max_length=30,verbose_name='类型名称')
	construct_typedes = models.TextField(verbose_name='类型描述',blank=True,null=True)
	construct_remark = models.CharField(max_length=1024,verbose_name='备注',blank=True,null=True)
	
	def __unicode__(self):
		return self.construct_typename

	class Meta:
		verbose_name = '结构类型'
		verbose_name_plural = '结构类型'



'''
建筑物用途表 T_BuildingUsage
'''
class building_usage(models.Model):
	building_usageid = models.CharField(max_length=32,verbose_name='用途编号',unique=True)
	building_usagename = models.CharField(max_length=20,verbose_name='用途名称')
	building_usagedesc = models.CharField(max_length=100,verbose_name='用途描述')

	def __unicode__(self):
		return self.building_usageid

	class Meta:
		verbose_name = '建筑物用途'
		verbose_name_plural = '建筑物用途'



'''
鉴定建筑物基础信息表 T_AssBuildInfo
'''
class building_information(models.Model):
	building_buildnumber = models.CharField(max_length=60,verbose_name='建筑物编号',unique=True)
	building_number = models.IntegerField(verbose_name='栋数')
	building_buildname = models.CharField(max_length=200,verbose_name='建筑物名称',blank=True,null=True)
	building_uplayernum = models.IntegerField(verbose_name='建筑物主题层数(地上)',blank=True,null=True)
	building_downlayernum = models.IntegerField(verbose_name='建筑物主题层数(地下)',blank=True,null=True)
	building_partlayernum = models.IntegerField(verbose_name='局部层数',blank=True,null=True)
	building_househostname =  models.CharField(max_length=100,verbose_name='房主姓名',blank=True,null=True)
	building_buildyear =  models.CharField(max_length=40,verbose_name='建成年份',blank=True,null=True)
	building_buildarea = models.CharField(max_length=64,verbose_name='建筑面积',blank=True,null=True)#本该是long
	building_constructtypeid = models.ForeignKey(building_structure,verbose_name='结构类型代码')
	building_buildusage = models.ForeignKey(building_usage,verbose_name='建筑物用途')
	building_longitude = models.FloatField( verbose_name='中心经度',blank=True,null=True)
	building_latitude = models.FloatField( verbose_name='中心纬度',blank=True,null=True)
	building_province = models.CharField(max_length=60,verbose_name='地点：省份',blank=True,null=True)
	building_city = models.CharField(max_length=100,verbose_name='地点：市',blank=True,null=True)
	building_district = models.CharField(max_length=100,verbose_name='地点：区县',blank=True,null=True)
	building_locationdetail = models.CharField(max_length=50,verbose_name='地点：详情',blank=True,null=True)
	building_admregioncode = models.CharField(max_length=100,verbose_name='行政区编号',blank=True,null=True)
	building_areanumber = models.ForeignKey(region,verbose_name='参数地区选择')
	building_fortificationinfo = models.CharField(max_length=80,verbose_name='抗震设防状况',blank=True,null=True)
	building_fortificationdegree = models.CharField(max_length=25,verbose_name='抗震设防烈度',blank=True,null=True)
	building_earthquakeid = models.ForeignKey(EQInfo,verbose_name='所属地震')
	building_userid = models.ForeignKey(sys_user,verbose_name='鉴定人员')
	building_remark = models.CharField(max_length=50,verbose_name='备注',blank=True,null=True)
	building_createdate = models.DateField(verbose_name="创建日期")
	building_createtime = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
	buidling_updatetime = models.DateTimeField(auto_now=True,verbose_name="最后更新时间")

	def __unicode__(self):
		return self.building_buildnumber

	class Meta:
		verbose_name = '建筑物基本信息'
		verbose_name_plural = '建筑物基本信息'
        # ordering = ['-building_createtime']




'''
鉴定建筑物基础信息临时表表 T_AssBuildInfo
'''
class building_information_tem(models.Model):
	building_buildnumber = models.CharField(max_length=60,verbose_name='建筑物编号',unique=True)
	building_number = models.IntegerField(verbose_name='栋数')
	building_buildname = models.CharField(max_length=200,verbose_name='建筑物名称',blank=True,null=True)
	building_uplayernum = models.IntegerField(verbose_name='建筑物主体层数(地上)',blank=True,null=True)
	building_downlayernum = models.IntegerField(verbose_name='建筑物主题层数(地下)',blank=True,null=True)
	building_partlayernum = models.IntegerField(verbose_name='局部层数',blank=True,null=True)
	building_househostname =  models.CharField(max_length=100,verbose_name='房主姓名',blank=True,null=True)
	building_buildyear =  models.CharField(max_length=40,verbose_name='建成年份',blank=True,null=True)
	building_buildarea = models.CharField(max_length=64,verbose_name='建筑面积',blank=True,null=True)#本该是long
	building_constructtypeid = models.ForeignKey(building_structure,verbose_name='结构类型代码')
	building_buildusage = models.ForeignKey(building_usage,verbose_name='建筑物用途')
	building_longitude = models.FloatField( verbose_name='中心经度',blank=True,null=True)
	building_latitude = models.FloatField( verbose_name='中心纬度',blank=True,null=True)
	building_province = models.CharField(max_length=60,verbose_name='地点：省份',blank=True,null=True)
	building_city = models.CharField(max_length=100,verbose_name='地点：市',blank=True,null=True)
	building_district = models.CharField(max_length=100,verbose_name='地点：区县',blank=True,null=True)
	building_locationdetail = models.CharField(max_length=50,verbose_name='地点：详情',blank=True,null=True)
	building_admregioncode = models.CharField(max_length=100,verbose_name='行政区编号',blank=True,null=True)
	building_areanumber = models.ForeignKey(region,verbose_name='参数地区选择')
	building_fortificationinfo = models.CharField(max_length=80,verbose_name='抗震设防状况',blank=True,null=True)
	building_fortificationdegree = models.CharField(max_length=25,verbose_name='抗震设防烈度',blank=True,null=True)
	building_earthquakeid = models.ForeignKey(EQInfo,verbose_name='所属地震')
	building_userid = models.ForeignKey(sys_user,verbose_name='鉴定人员')
	building_remark = models.CharField(max_length=50,verbose_name='备注',blank=True,null=True)
	building_createdate = models.DateField(auto_now_add=True,verbose_name="创建日期")

	def __unicode__(self):
		return self.building_buildnumber

	class Meta:
		verbose_name = '建筑物基本信息临时表'
		verbose_name_plural = '建筑物基本信息临时表'
        # ordering = ['-building_createtime']


'''
建筑物图片表 T-logincount
'''
class buildImage(models.Model):
	buildid = models.CharField(max_length=60,verbose_name='建筑物编号',unique=True)
	frontimage = models.ImageField(upload_to = 'buildimage/%Y/%m/%d',verbose_name='建筑物前面图',blank=True,null=True)
	backimage = models.ImageField(upload_to = 'buildimage/%Y/%m/%d',verbose_name='建筑物后面图',blank=True,null=True)
	leftimage = models.ImageField(upload_to = 'buildimage/%Y/%m/%d',verbose_name='建筑物左面图',blank=True,null=True)
	rightimage = models.ImageField(upload_to = 'buildimage/%Y/%m/%d',verbose_name='建筑物右面图',blank=True,null=True)
	topimage = models.ImageField(upload_to = 'buildimage/%Y/%m/%d',verbose_name='建筑物顶图',blank=True,null=True)
	innerimage = models.ImageField(upload_to = 'buildimage/%Y/%m/%d',verbose_name='建筑物内图',blank=True,null=True)

	def __unicode__(self):
		return self.buildid.building_buildname

	class Meta:
		verbose_name = '建筑物图片'
		verbose_name_plural = '建筑物图片'





'''
场地影响表—— T_Field_Effect
'''
class field_effect(models.Model):
	effect_id = models.CharField(max_length=40,verbose_name='影响编号',unique=True)
	effect_name = models.CharField(max_length=40,verbose_name='影响名称')
	effect_desc = models.CharField(max_length=40,verbose_name='影响描述')

	def __unicode__(self):
		return self.effect_name

	class Meta:
		verbose_name = '场地影响表'
		verbose_name_plural = '场地影响表'

'''
地基状况表—— foundation_status
'''
class foundation_status(models.Model):
	status_id = models.CharField(max_length=40,verbose_name='地基状况编号',unique=True)
	status_name = models.CharField(max_length=40,verbose_name='地基状况名称')
	status_desc = models.CharField(max_length=40,verbose_name='地基状况描述')

	def __unicode__(self):
		return self.status_name

	class Meta:
		verbose_name = '地基状况表'
		verbose_name_plural = '地基状况表'


'''
预期地震/环境信息表 T_PreEarthEnviroInfo
'''
class environment(models.Model):
	environment_buildnumber = models.ForeignKey(building_information,verbose_name='建筑物编号')
	environment_earthquakeeff = models.CharField(max_length=80,verbose_name='场地影响')
	environment_foundation = models.CharField(max_length=80,verbose_name='地基状况')
	environment_adjoinbuild = models.CharField(max_length=20,verbose_name='毗邻建筑',blank=True,null=True)
	environment_seismicintensity = models.CharField(max_length=40,verbose_name='既发生地震烈度',blank=True,null=True)
	environment_smallaffect = models.CharField(max_length=40,verbose_name='小震作用',blank=True,null=True)
	environment_bigaffect= models.CharField(max_length=40,verbose_name='大震作用',blank=True,null=True)
	environment_remark = models.CharField(max_length=50,verbose_name='备注',blank=True,null=True)
	environment_createtime = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
	
	def __unicode__(self):
		return self.environment_bigaffect

	class Meta:
		verbose_name = '环境信息'
		verbose_name_plural = '环境信息'
		ordering = ['-environment_createtime']



'''
预期地震/环境信息临时表 
'''
class environment_tem(models.Model):
	environment_buildnumber = models.ForeignKey(building_information_tem,verbose_name='建筑物编号')
	environment_earthquakeeff = models.CharField(max_length=80,verbose_name='场地影响')
	environment_foundation = models.CharField(max_length=80,verbose_name='地基状况')
	environment_adjoinbuild = models.CharField(max_length=20,verbose_name='毗邻建筑',blank=True,null=True)
	environment_seismicintensity = models.CharField(max_length=40,verbose_name='既发生地震烈度',blank=True,null=True)
	environment_smallaffect = models.CharField(max_length=40,verbose_name='小震作用',blank=True,null=True)
	environment_bigaffect= models.CharField(max_length=40,verbose_name='大震作用',blank=True,null=True)
	environment_remark = models.CharField(max_length=50,verbose_name='备注',blank=True,null=True)
	
	def __unicode__(self):
		return self.environment_bigaffect

	class Meta:
		verbose_name = '环境信息临时表'
		verbose_name_plural = '环境信息临时表'


'''
建筑物部位表 T_BuildingLocation
'''
class buildlocation(models.Model):
	location_id = models.CharField(max_length=32,verbose_name='部位ID',unique=True)
	location_constructtype = models.ForeignKey(building_structure,verbose_name='结构类型')
	location_name = models.CharField(max_length=30,verbose_name='部位名称')
	location_desc = models.CharField(max_length=30,verbose_name='部位描述')
	location_seqnumber = models.CharField(max_length=32,verbose_name='顺序',blank=True,null=True)
	location_remark = models.CharField(max_length=50,verbose_name='备注',blank=True,null=True)

	def __unicode__(self):
		return self.location_name

	class Meta:
		verbose_name = '建筑物部位信息'
		verbose_name_plural = '建筑物部位信息'


'''
建筑物部位子因素分类表 T_ SubLocationCatalog
'''
class SubLocationCatalog(models.Model):
	catalog_id = models.CharField(max_length=32,verbose_name='部位子因素id',unique=True)
	catalog_constructtypeid = models.ForeignKey(building_structure,verbose_name='所属类型ID')
	catalog_locationid = models.ForeignKey(buildlocation,verbose_name="部位名称")
	catalog_name = models.CharField(max_length=100,verbose_name='部位子因素')
	catalog_des = models.CharField(max_length=32,verbose_name='分类描述',blank=True,null=True)
	catalog_seqnumber = models.CharField(max_length=32,verbose_name='顺序',blank=True,null=True)
	catalog_remark = models.CharField(max_length=50,verbose_name='备注',blank=True,null=True)

	def __unicode__(self):
		return self.catalog_name

	class Meta:
		verbose_name = '建筑物部位子因素分类息'
		verbose_name_plural = '建筑物部位子因素分类信息'


'''
建筑物部位子因素表 T_BuildingSubLocation
'''
class sublocal(models.Model):
	sublocal_id = models.CharField(max_length=32,verbose_name='部位子因素id',unique=True)
	sublocal_constructtypeid = models.ForeignKey(building_structure,verbose_name='所属类型ID')
	sublocal_locationid = models.ForeignKey(buildlocation,verbose_name="部位名称")
	sublocal_sublocationcatalog = models.ForeignKey(SubLocationCatalog,verbose_name='子因素分类')
	sublocal_name = models.CharField(max_length=100,verbose_name='部位子因素')
	sublocal_helpid = models.CharField(max_length=32,verbose_name='帮助地址',blank=True,null=True)
	sublocal_seqnumber = models.CharField(max_length=32,verbose_name='顺序',blank=True,null=True)
	sublocal_remark = models.CharField(max_length=50,verbose_name='备注',blank=True,null=True)

	def __unicode__(self):
		return self.sublocal_name

	class Meta:
		verbose_name = '部位子因素信息'
		verbose_name_plural = '部位子因素信息'






'''
鉴定结果表 T_Results
'''
class identify_result(models.Model):
	result_buildnumber = models.ForeignKey(building_information,verbose_name='建筑物编号',unique=True)
	result_id = models.CharField(max_length=64,verbose_name="鉴定结果编号",blank=True,null=True)
	result_securitycategory = models.CharField(max_length=8,verbose_name='安全类别')
	result_assetdate = models.DateField(auto_now_add=True,verbose_name='鉴定日期')
	result_totaldamageindex = models.CharField(max_length=200,verbose_name='整体震损指数',blank=True,null=True)
	result_damagedegree = models.CharField(max_length=8,verbose_name='破坏等级',blank=True,null=True)
	result_remark = models.CharField(max_length=50,verbose_name='备注',blank=True,null=True)

	def __unicode__(self):
		return self.result_id

	class Meta:
		verbose_name = '建筑物安全鉴定结果表'
		verbose_name_plural = '建筑物安全鉴定结果表'


'''
建筑物震损信息表 T_DamageInfo
'''
class damage(models.Model):
	damage_id = models.CharField(max_length="32",verbose_name="编号")
	damage_buildnumber = models.ForeignKey(building_information,verbose_name='建筑物编号')
	damage_constructtypeid = models.ForeignKey(building_structure,verbose_name='建筑物结构类型')
	damage_locationid = models.ForeignKey(buildlocation,verbose_name='部位ID')
	damage_catalogid = models.ForeignKey(SubLocationCatalog,verbose_name='部位子因素分类')
	damage_sublocationid = models.ForeignKey(sublocal,verbose_name='部位子因素')
	damage_number = models.CharField(max_length=20,verbose_name='数量',blank=True,null=True)
	damage_degree = models.CharField(max_length=20,verbose_name='程度',blank=True,null=True)
	damage_parameteradjust = models.FloatField(verbose_name='参数微调',blank=True,null=True)
	damage_description = models.CharField(max_length=200,verbose_name='描述',blank=True,null=True)
	damage_remark = models.CharField(max_length=50,verbose_name='备注',blank=True,null=True)
	damage_isfirst = models.CharField(max_length=10,verbose_name='是否是第一个',blank=True,null=True)


	def __unicode__(self):
		return self.damage_id

	class Meta:
		verbose_name = '建筑物细部震损信息'
		verbose_name_plural = '建筑物细部震损信息'



'''
建筑物震损信息表 T_DamageInfo
'''
class damage_tem(models.Model):
	damage_id = models.CharField(max_length="32",verbose_name="编号")
	damage_buildnumber = models.ForeignKey(building_information_tem,verbose_name='建筑物编号')
	damage_constructtypeid = models.ForeignKey(building_structure,verbose_name='建筑物结构类型')
	damage_locationid = models.ForeignKey(buildlocation,verbose_name='部位ID')
	damage_catalogid = models.ForeignKey(SubLocationCatalog,verbose_name='部位子因素分类')
	damage_sublocationid = models.ForeignKey(sublocal,verbose_name='部位子因素')
	damage_number = models.CharField(max_length=20,verbose_name='数量',blank=True,null=True)
	damage_degree = models.CharField(max_length=20,verbose_name='程度',blank=True,null=True)
	damage_parameteradjust = models.FloatField(verbose_name='参数微调',blank=True,null=True)
	damage_description = models.CharField(max_length=200,verbose_name='描述',blank=True,null=True)
	damage_remark = models.CharField(max_length=50,verbose_name='备注',blank=True,null=True)
	damage_isfirst = models.CharField(max_length=10,verbose_name='是否是第一个',blank=True,null=True)

	def __unicode__(self):
		return self.damage_id

	class Meta:
		verbose_name = '建筑物细部震损信息'
		verbose_name_plural = '建筑物细部震损信息'



'''
信息选项表 T_OptionList
'''
class option(models.Model):
	option_opttagname = models.CharField(max_length=10,verbose_name='选项名称',unique=True)
	option_opttagvalue = models.CharField(max_length=30,verbose_name='选项内容')
	option_remark = models.CharField(max_length=50,verbose_name='备注',blank=True,null=True)

	def __unicode__(self):
		return self.option_opttagname

	class Meta:
		verbose_name = '信息选项'
		verbose_name_plural = '信息选项'


'''
新闻通知表 T_News
'''
class news(models.Model):
	news_newsid = models.CharField(max_length=32,verbose_name='新闻id',unique=True)
	news_newstitle = models.CharField(max_length=50,verbose_name='新闻标题')
	news_newscontent = models.TextField(verbose_name='新闻内容')
	news_adddate = models.DateField(verbose_name='添加时间')
	news_addperson = models.CharField(max_length=10,verbose_name='添加人员',blank=True,null=True)
	news_remark = models.CharField(max_length=50,verbose_name='备注',blank=True,null=True)

	def __unicode__(self):
		return self.news_newstitle

	class Meta:
		verbose_name = '新闻通知信息'
		verbose_name_plural = '新闻通知信息'

'''
帮助文档标题表 T_HelpTitle
'''
class helptitle(models.Model):
	helpti_helptitleid = models.CharField(max_length=32,verbose_name='标题ID',unique=True)
	helpti_titlename = models.CharField(max_length=20,verbose_name='标题名称')
	helpti_titleparentid = models.CharField(max_length=32,verbose_name='所属分类')
	helpti_seqnumber = models.CharField(max_length=50,verbose_name='显示顺序',blank=True,null=True)
	helpti_remark = models.CharField(max_length=50,verbose_name='备注',blank=True,null=True)

	def __unicode__(self):
		return self.helpti_titlename

	class Meta:
		verbose_name = '帮助文档标题信息'
		verbose_name_plural = '帮助文档标题信息'

'''
帮助文档内容表 T_HelpContent
'''
class helpco(models.Model):
	helpco_helptitleid = models.ForeignKey(helptitle,verbose_name='标题ID')
	helpco_helpcontent = models.TextField(verbose_name='帮助内容',blank=True,null=True)
	helpco_remark = models.CharField(max_length=50,verbose_name='备注',blank=True,null=True)

	def __unicode__(self):
		return helpco_helptitleid

	class Meta:
		verbose_name = '帮助文档内容信息'
		verbose_name_plural = '帮助文档内容信息'

