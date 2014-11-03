/*
 * 自己写一个标注类MMarker，继承自BMap.Marker，采用的是原型链继承方式
 * no-标注编号,这个编号是跟从后台传过来的数据解析成的数组d的下标示一致的
 */
function MMarker(no,point,opts) {
		this.no = no;
		BMap.Marker.call(this,point,opts);
	}
	MMarker.prototype = new BMap.Marker();
	MMarker.prototype.constructor = MMarker;


var info = new BMap.InfoWindow("",{width:240,height:160,enableMessage:false});//显示框
var map ;
var d;//存储从服务器传过来的数据
var index;

/*
 *显示信息窗口
 *e-事件参数
*/
function showInfo(e) {
	 index = e.target.no;//获取标注编号,由于和数组d的下标是一一对应的，所以可以直接通过index取数据
	//传个hmtl的参数
	
	info.setContent("安全类别:" + d[index].safe + "<br>经度: " + d[index].longitude + "<br>纬度 :" + d[index].latitude
			+"<br>结构类型:" + d[index].struct + "<br>建成年份:" + d[index].years + "<br>地点:" + d[index].address 
            +"<br>设防状况:" + d[index].protect);
	//info.setContent("eeee")
	//<a target='_self' href='map/infomation.html?marker=" + param + "'>详细信息>></a>//跳转到html页面
	map.openInfoWindow(info,e.point);
}

/*
 *不同的级别显示不同的标注图片
 *level-等级
 *no-标注编号
*/

 function setIconColor(point,level,no) {
	var marker = null;//标注
	var myIcon = null;//标注图片
	var path =null;
	if(level>4)
	{
     path = "images/pic3" + level + ".png";
	}
	else
	{
	 path = "images/pic3" + level + "r.png";
	}
    myIcon = new BMap.Icon(path, new BMap.Size(30, 30));
	
	marker = new MMarker(no,point,{icon: myIcon});//创建标注，并用自己的图片替换掉系统默认的标注图片
	marker.addEventListener("click", showInfo);//给标记添加事件

	return marker;//返回标注
 }

 


function f(data) {
	//解析从服务器端传过来的JSON数据，存进数组d
    d = [
		{"longitude":104.164452,"latitude":30.825297,"icon":1,"safe":"安全","struct":"多层砌体结构","years":"1978-1989","address":"成都市新都区","protect":"6度防护"},
		{"longitude":103.638979,"latitude":30.986914,"icon":2,"safe":"安全","struct":"单层钢筋混凝土厂房","years":"1978-1989","address":"成都市都江堰市","protect":"7度防护"},
		{"longitude":103.576888,"latitude":31.497697,"icon":3,"safe":"安全","struct":"多层和高层钢筋混凝土结构","years":"1978-1989","address":"成都市汶川县","protect":"3度防护"},
		{"longitude":104.167967,"latitude":35.831644,"icon":4,"safe":"安全","struct":"单层砖柱厂房","years":"1978-1989","address":"兰州市榆中县","protect":"6度防护"},
		{"longitude":84.94196,"latitude":45.607607,"icon":5,"safe":"安全","struct":"底层框架结构","years":"1978-1989","address":"新疆克拉玛依市","protect":"6度防护"},
		{"longitude":120.356757,"latitude":22.639286,"icon":6,"safe":"安全","struct":"木结构建筑","years":"1978-1989","address":"台湾省高雄市","protect":"6度防护"},
		{"longitude":91.031466,"latitude":29.672775,"icon":7,"safe":"安全","struct":"内框架结构","years":"1978-1989","address":"西藏拉萨","protect":"6度防护"},
		{"longitude":106.411606,"latitude":38.416741,"icon":8,"safe":"安全","struct":"土石结构建筑物","years":"1978-1989","address":"银川市","protect":"6度防护"},		
		
		{"longitude":103.6,"latitude":28.1,"icon":1,"safe":"安全","struct":"多层砌体结构","years":"1978-1989","address":"云南省昭通市永善县","protect":"6度防护"},
		{"longitude":124.1,"latitude":44.6,"icon":2,"safe":"安全","struct":"单层钢筋混凝土厂房","years":"1978-1989","address":"吉林省松原市前郭尔罗斯蒙古族自治县","protect":"7度防护"},
		{"longitude":101.5,"latitude":37.7,"icon":3,"safe":"安全","struct":"多层和高层钢筋混凝土结构","years":"1978-1989","address":"甘肃省张掖市肃南裕固族自治县、青海省海北藏族自治州门源回族自治县交界","protect":"3度防护"},
		{"longitude":95.9,"latitude":37.831644,"icon":4,"safe":"安全","struct":"单层砖柱厂房","years":"1978-1989","address":"青海省海西蒙古族藏族自治州","protect":"6度防护"},
		{"longitude":86.5196,"latitude":31.607607,"icon":5,"safe":"安全","struct":"底层框架结构","years":"1978-1989","address":"西藏自治区那曲地区尼玛县","protect":"6度防护"},
		{"longitude":121.77,"latitude":36.839286,"icon":6,"safe":"安全","struct":"木结构建筑","years":"1978-1989","address":"山东省威海市乳山市","protect":"6度防护"},
		{"longitude":110.831466,"latitude":30.972775,"icon":7,"safe":"安全","struct":"内框架结构","years":"1978-1989","address":"湖北省宜昌市秭归县","protect":"6度防护"},
		{"longitude":82.411606,"latitude":36.416741,"icon":8,"safe":"安全","struct":"土石结构建筑物","years":"1978-1989","address":"新疆维吾尔自治区和田地区于田县","protect":"6度防护"}
		
		
		
		];
 
    map = new BMap.Map("allmap");
	// 百度地图API功能
	map.centerAndZoom(new BMap.Point(116.404, 39.915),5);
	map.addControl(new BMap.NavigationControl());//地图平移缩放控件
	map.addControl(new BMap.OverviewMapControl());//缩略图
	map.addControl(new BMap.ScaleControl()); //比例尺
	map.enableScrollWheelZoom();//鼠标滑轮缩放
	
	var marker = null;
	//var markers = [];
	var pt = null;
	var i = 0;
	 
	for (; i < d.length; i++) {
	   pt = new BMap.Point(d[i].longitude, d[i].latitude);
	   marker = setIconColor(pt,d[i].icon,i);//i表示标注的编号，pt是点，1代表采用的图例

	   map.addOverlay(marker);  
	}

}

