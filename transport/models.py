#coding:utf-8
from django.db import models
# import simplejson as json
# Create your models here.
'''
用户信息表 T-UserInfo
'''
class sys_user(models.Model):
	user_id = models.CharField(max_length=32,verbose_name='用户编号',unique=True)
	user_realname = models.CharField(max_length=20,verbose_name='姓名')
	user_idcard = models.CharField(max_length=20,verbose_name='身份证号',blank=True)
	user_major = models.CharField(max_length=50,verbose_name='专业',blank=True)
	user_workunit = models.CharField(max_length=50,verbose_name='单位',blank=True)
	user_title = models.CharField(max_length=20,verbose_name='职称',blank=True)
	user_address = models.CharField(max_length=50,verbose_name='通信地址',blank=True)
	user_postcode = models.CharField(max_length=6,verbose_name='邮政编码',blank=True)
	user_email = models.CharField(max_length=30,verbose_name='邮件地址',blank=True)
	user_tel = models.CharField(max_length=15,verbose_name='电话号码',blank=True)
	user_pac = models.CharField(max_length=32,verbose_name='激活码',blank=True)
	user_state = models.CharField(max_length=10,verbose_name='用户状态')
	user_name = models.CharField(max_length=20,verbose_name='登录用户名')
	user_password = models.CharField(max_length=32,verbose_name='登录密码')
	user_remark = models.CharField(max_length=50,verbose_name='备注',blank=True)

	def __unicode__(self):
		return self.user_realname

	class Meta:
		verbose_name = '用户信息'
		verbose_name_plural = '用户信息'

'''
地震信息表 T-Earthquake
'''
class EQInfo(models.Model):
	eq_earthquakeid = models.CharField(max_length=30,verbose_name='地震编号',unique=True)
	eq_earthquakename = models.CharField(max_length=30,verbose_name='地震名称')
	eq_date = models.DateField(verbose_name='发震日期',blank=True)
	eq_time = models.TimeField(verbose_name='发震时间',blank=True)
	eq_location = models.CharField(max_length=100,verbose_name='发生地点',blank=True)
	eq_focallongitude = models.FloatField(verbose_name='震源经度',blank=True)
	eq_focallatitude = models.FloatField(verbose_name='震源纬度',blank=True)
	eq_magnitude = models.IntegerField(verbose_name='震级(里氏)',blank=True)
	eq_focaldepth = models.IntegerField(verbose_name='震源深度（KM）',blank=True)
	eq_epicentralintensity = models.CharField(max_length=10,verbose_name='中心烈度',blank=True)
	eq_remark = models.CharField(max_length=30,verbose_name='备注',blank=True)

	def __unicode__(self):
		return self.eq_earthquakename

	class Meta:
		verbose_name = '地震信息'
		verbose_name_plural = '地震信息'


'''
建筑物的结构类型表 T_BuildingConstructionType
'''
class building_structure(models.Model):
	construct_typeid = models.CharField(max_length=20,verbose_name='类型id',unique=True)
	construct_typename = models.CharField(max_length=30,verbose_name='类型名称')
	construct_typedes = models.TextField(verbose_name='类型描述',blank=True)
	construct_remark = models.CharField(max_length=50,verbose_name='备注',blank=True)
	
	def __unicode__(self):
		return self.construct_typename

	class Meta:
		verbose_name = '结构类型'
		verbose_name_plural = '结构类型'


'''
参数地区表 T_ParamAreas
'''
class region(models.Model):
	region_areanumber = models.CharField(max_length=32,verbose_name='地区编号',unique=True)
	region_areaname = models.CharField(max_length=20,verbose_name='区域名称')
	region_arealocation = models.CharField(max_length=100,verbose_name='地理位置')
	region_areadesc = models.CharField(max_length=50,verbose_name='区域描述',blank=True)
	region_remark = models.CharField(max_length=50,verbose_name='备注',blank=True)


	def __unicode__(self):
		return self.region_areaname

	class Meta:
		verbose_name = '地区'
		verbose_name_plural = '地区'





'''
鉴定建筑物基础信息表 T_AssBuildInfo
'''
class building_information(models.Model):
	building_buildnumber = models.CharField(max_length=30,verbose_name='建筑物编号',unique=True)
	building_number = models.IntegerField(verbose_name='栋数')
	building_buildname = models.CharField(max_length=200,verbose_name='建筑物名称',blank=True)
	building_uplayernum = models.IntegerField(verbose_name='建筑物主题层数(地上)',blank=True)
	building_downlayernum = models.IntegerField(verbose_name='建筑物主题层数(地下)',blank=True)
	building_partlayernum = models.IntegerField(verbose_name='局部层数',blank=True)
	building_househostname =  models.CharField(max_length=100,verbose_name='房主姓名',blank=True)
	building_buildyear =  models.CharField(max_length=40,verbose_name='建成年份',blank=True)
	building_buildarea = models.CharField(max_length=64,verbose_name='建筑面积',blank=True)#本该是long
	building_constructtypeid = models.ForeignKey(building_structure,verbose_name='结构类型代码')
	building_buildusage = models.CharField(max_length=20,verbose_name='建筑物用途',blank=True)
	building_longitude = models.FloatField( verbose_name='中心经度',blank=True)
	building_latitude = models.FloatField( verbose_name='中心纬度',blank=True)
	building_province = models.CharField(max_length=60,verbose_name='地点：省份',blank=True)
	building_city = models.CharField(max_length=100,verbose_name='地点：市',blank=True)
	building_district = models.CharField(max_length=100,verbose_name='地点：区县',blank=True)
	building_locationdetail = models.CharField(max_length=50,verbose_name='地点：详情',blank=True)
	building_admregioncode = models.CharField(max_length=100,verbose_name='行政区编号',blank=True)
	building_areanumber = models.ForeignKey(region,verbose_name='参数地区选择')
	building_fortificationinfo = models.CharField(max_length=80,verbose_name='抗震设防状况',blank=True)
	building_fortificationdegree = models.CharField(max_length=25,verbose_name='抗震设防烈度',blank=True)
	building_earthquakeid = models.ForeignKey(EQInfo,verbose_name='所属地震')
	building_userid = models.ForeignKey(sys_user,verbose_name='测评人员')
	building_remark = models.CharField(max_length=50,verbose_name='备注',blank=True)

	def __unicode__(self):
		return self.building_buildname

	class Meta:
		verbose_name = '建筑物基本信息'
		verbose_name_plural = '建筑物基本信息'




'''
预期地震/环境信息表 T_PreEarthEnviroInfo
'''
class environment(models.Model):
	environment_buildnumber = models.ForeignKey(building_information,verbose_name='建筑物编号',unique=True)
	environment_foundation = models.CharField(max_length=40,verbose_name='地基状况',blank=True)
	environment_adjoinbuild = models.CharField(max_length=20,verbose_name='毗邻建筑',blank=True)
	environment_seismicintensity = models.CharField(max_length=40,verbose_name='既发生地震烈度',blank=True)
	environment_smallaffect = models.CharField(max_length=40,verbose_name='小震作用',blank=True)
	environment_bigaffect= models.CharField(max_length=40,verbose_name='大震作用',blank=True)
	environment_remark = models.CharField(max_length=50,verbose_name='备注',blank=True)

	def __unicode__(self):
		return self.environment_buildnumber

	class Meta:
		verbose_name = '环境信息'
		verbose_name_plural = '环境信息'


'''
建筑物部位子因素表 T_BuildingSubLocation
'''
class sublocal(models.Model):
	sublocal_sublocationid = models.CharField(max_length=32,verbose_name='部位子因素id',unique=True)
	sublocal_constructtypeid = models.ForeignKey(building_structure,verbose_name='所属类型ID')
	sublocal_locationname = models.CharField(max_length=30,verbose_name='部位名称')
	sublocal_sublocationcatalog = models.CharField(max_length=30,verbose_name='子因素分类')
	sublocal_sublocationname = models.CharField(max_length=100,verbose_name='部位子因素')
	sublocal_helpid = models.CharField(max_length=32,verbose_name='帮助地址',blank=True)
	sublocal_seqnumber = models.CharField(max_length=32,verbose_name='顺序',blank=True)
	sublocal_remark = models.CharField(max_length=50,verbose_name='备注',blank=True)

	def __unicode__(self):
		return self.sublocal_sublocationid

	class Meta:
		verbose_name = '部位子因素信息'
		verbose_name_plural = '部位子因素信息'
'''
建筑物部位 
'''
class buildlocation(models.Model):
	loc_id = models.CharField(max_length=32,verbose_name='部位id',unique=True)
	loc_constructid = models.ForeignKey(building_structure,verbose_name='部位子因素id' )
	loc_name = models.CharField(max_length=32,verbose_name='部位名称')
	loc_desc = models.CharField(max_length=320,verbose_name='部位描述')
	loc_seq = models.CharField(max_length=320,verbose_name='部位顺序')
	loc_remark = models.CharField(max_length=320,verbose_name='备注')
	def __unicode__(self):
		return self.loc_name

	class Meta:
		verbose_name = '建筑物部位'
		verbose_name_plural = '建筑物部位'



'''
建筑物细部震损信息表 T_DamageInfo
'''
class damage(models.Model):
	damage_buildnumber = models.ForeignKey(building_information,verbose_name='建筑物编号',unique=True)
	damage_constructtypeid = models.ForeignKey(building_structure,verbose_name='建筑物结构类型')
	damage_locationid = models.ForeignKey(buildlocation,verbose_name='部位ID')
	damage_sublocationid = models.ForeignKey(sublocal,verbose_name='部位子因素')
	damage_number = models.CharField(max_length=20,verbose_name='数量',blank=True)
	damage_degree = models.CharField(max_length=20,verbose_name='程度',blank=True)
	damage_sublocationfactor = models.FloatField(verbose_name='部位因子',blank=True)
	damage_description = models.CharField(max_length=200,verbose_name='描述',blank=True)
	damage_remark = models.CharField(max_length=50,verbose_name='备注',blank=True)


	def __unicode__(self):
		return self.damage_buildnumber

	class Meta:
		verbose_name = '建筑物细部震损信息'
		verbose_name_plural = '建筑物细部震损信息'


'''
鉴定结果表 T_Results
'''
class result(models.Model):
	result_buildnumber = models.ForeignKey(building_information,verbose_name='建筑物编号',unique=True)
	result_securitycategory = models.CharField(max_length=8,verbose_name='安全类别')
	result_totaldamageindex = models.CharField(max_length=200,verbose_name='整体震损指数',blank=True)
	result_damagedegree = models.CharField(max_length=8,verbose_name='破坏等级',blank=True)
	result_assetdate = models.DateField(verbose_name='鉴定日期')
	result_remark = models.CharField(max_length=50,verbose_name='备注',blank=True)

	def __unicode__(self):
		return self.result_securitycategory

	class Meta:
		verbose_name = '建筑物安全鉴定结果信'
		verbose_name_plural = '建筑物安全鉴定结果信'


'''
管理用户表 T_Admin
'''
class t_admin(models.Model):
	admin_adminid = models.CharField(max_length=32,verbose_name='用户编号',unique=True)
	admin_adminloginname = models.CharField(max_length=20,verbose_name='登陆用户名')
	admin_adminloginpwd = models.CharField(max_length=32,verbose_name='登录密码')
	admin_adminname = models.CharField(max_length=10,verbose_name='用户姓名',blank=True)
	admin_remark = models.CharField(max_length=50,verbose_name='备注',blank=True)

	def __unicode__(self):
		return self.admin_adminname
	 
	class Meta:
		verbose_name = '管理用户信息'
		verbose_name_plural = '管理用户信息'




'''
信息选项表 T_OptionList
'''
class option(models.Model):
	option_opttagname = models.CharField(max_length=10,verbose_name='选项名称',unique=True)
	option_opttagvalue = models.CharField(max_length=30,verbose_name='选项内容')
	option_remark = models.CharField(max_length=50,verbose_name='备注',blank=True)

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
	news_addperson = models.CharField(max_length=10,verbose_name='添加人员',blank=True)
	news_remark = models.CharField(max_length=50,verbose_name='备注',blank=True)

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
	helpti_seqnumber = models.CharField(max_length=50,verbose_name='显示顺序',blank=True)
	helpti_remark = models.CharField(max_length=50,verbose_name='备注',blank=True)

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
	helpco_helpcontent = models.TextField(verbose_name='帮助内容',blank=True)
	helpco_remark = models.CharField(max_length=50,verbose_name='备注',blank=True)

	def __unicode__(self):
		return helpco_helptitleid

	class Meta:
		verbose_name = '帮助文档内容信息'
		verbose_name_plural = '帮助文档内容信息'

