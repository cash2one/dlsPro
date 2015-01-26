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
     path = "/static/img/pic3" + level + ".png";
	}
	else
	{
	 path = "/static/img/pic3" + level + "r.png";
	}
    myIcon = new BMap.Icon(path, new BMap.Size(30, 30));
	
	marker = new MMarker(no,point,{icon: myIcon});//创建标注，并用自己的图片替换掉系统默认的标注图片
	marker.addEventListener("click", showInfo);//给标记添加事件

	return marker;//返回标注
 }

 


function f(data) {
	//解析从服务器端传过来的JSON数据，存进数组d

    map = new BMap.Map("allmap", {mapType:BMAP_HYBRID_MAP});
	// 百度地图API功能
	map.centerAndZoom(new BMap.Point(116.404, 39.915),5);
	map.addControl(new BMap.NavigationControl());//地图平移缩放控件
	map.addControl(new BMap.OverviewMapControl());//缩略图
	map.addControl(new BMap.ScaleControl()); //比例尺
	map.addControl(new BMap.MapTypeControl());
	map.enableScrollWheelZoom();//鼠标滑轮缩放
	
	var marker = null;
	//var markers = [];
	var pt = null;
	var i;

	var dd = $("#cxdivMap").children();
	var qstring=" and (";
	for(var i = 1;i<dd.length;i++)
	{
		var c = dd[i].childNodes;
		
		for(var j = 0;j<c.length;j++)
		{
			
			if(c[j].name == "xz")
			{
				if(c[j].value == "bq")
				{
					qstring+=" and "
				}else if(c[j].value == "hz")
				{
					qstring+=" or "
				}
			}
			if(c[j].name == "tj")
			{
				qstring+=c[j].value;
			}
			if(c[j].name == "tjtxt")
			{
				if(i==1){
					if($("#cxmsMap").val()=="jq")
						qstring+=" = "+"'"+c[j].value+"' ";
					else
						{
						qstring+=" like '@@@"+c[j].value+"%'";
						}
				}
				else
				{
					if(c[j+1].value=="jq")
						qstring+=" = "+"'"+c[j].value+"' ";
					else
						{
						qstring+=" like '@@@"+c[j].value+"%'";
						}
				}
			}
		}
		
	}

	$.post("/t/countMap",
    {qstring1:qstring,},
    function(data){
    if(data.length>0)
    {

    	var ss = eval(data);
    	d = ss;
    	for (i=0; i < d.length; i++) {
		   pt = new BMap.Point(d[i].longitude, d[i].latitude);
		   	// alert(d[i].address);
		   	marker = setIconColor(pt,d[i].icon,i);//i表示标注的编号，pt是点，1代表采用的图例
		   	map.addOverlay(marker);  
			}
    	// alert(d);
    }
    else{
        alert(data);
    }
  });
	

}

