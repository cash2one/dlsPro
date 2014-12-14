var gotLocation = 0;
var map = new BMap.Map("allmap");
$(document).ready(function(){
		$("#map_confirm").click(function(){
			if(window.gotLocation == 1)
				$("#myModal").modal("hide");
			else
				alert("请选择位置后在确定！");
		});
		$("#showMap").click(function(){

					
					//增加地图控件
					// var top_right_navigation = new BMap.NavigationControl({anchor: BMAP_ANCHOR_TOP_LEFT, type: BMAP_NAVIGATION_CONTROL_ZOOM}); //右上角，仅包含平移和缩放按钮
			  		// map.addControl(top_right_navigation);
			  		map.addControl(new BMap.NavigationControl());//地图平移缩放控件
					// map.addControl(new BMap.OverviewMapControl());//缩略图
					map.addControl(new BMap.ScaleControl()); //比例尺
					map.enableScrollWheelZoom();//鼠标滑轮缩放
					//var point = new BMap.Point(116.331398,39.897445);
					//map.centerAndZoom(point,12);
					//根据IP获取城市，并且设置城市中心点
					var myCity = new BMap.LocalCity();
					myCity.get(function moveToCity(result){
						var center = result.center;
						map.centerAndZoom(center,12);
					});
	  

					//设置地图的点击事件
					map.addEventListener("click",function(e){
						//map.setCenter(e.point);
						var marker = new BMap.Marker(e.point);
						map.clearOverlays();    //清除地图上所有覆盖物
						map.addOverlay(marker);

						$("#long").val(e.point.lng);
						$("#lati").val(e.point.lat);
						//逆解析地址
						var gc = new BMap.Geocoder();
						gc.getLocation(e.point,function(rs){
							var addComp = rs.addressComponents;
							var address = addComp.province +  addComp.city +  addComp.district +  addComp.street;
							$("#suggestId").val(address);
							$("#sskin_se").val(addComp.province);
							$("#sskin_si").val(addComp.city);
							$("#sskin_qu").val(addComp.district);
							$("#sskin_xi").val(addComp.street);
							// $("#or_start").val(address);
						// 	function code(){
						// 	var pp = local.getResults().getPoi(0).postcode ;    //获取第一个智能搜索的结果
						// 	if(pp)
						// 	{
						// 		$("#xzqbm").val(pp);
						// 	}else
						// 	{
						// 		$("#xzqbm").val("");
						// 	}
						// }
						// var local = new BMap.LocalSearch(map, { //智能搜索
						//   onSearchComplete: code
						// });
						// // local.search(address);
						});
						window.gotLocation = 1;
					});



					function G(id) {
						return document.getElementById(id);
					}

					var ac = new BMap.Autocomplete({    //建立一个自动完成的对象
						"input" : "suggestId",
						"location" : map//,
						//"onSearchComplete":mySearch
					});
					//ac.setInputValue("请输入装车地址并从下拉框选择准确位置");
					//function mySearch(result){
					//	alert(result.getNumPois());
					//}

					ac.addEventListener("onhighlight", function(e) {  //鼠标放在下拉列表上的事件
						var str = "";
						var _value = e.fromitem.value;
						var value = "";
						if (e.fromitem.index > -1) {
							value = _value.province +  _value.city +  _value.district +  _value.street +  _value.business;
						}    
						str = "FromItem<br />index = " + e.fromitem.index + "<br />value = " + value;
						
						value = "";
						if (e.toitem.index > -1) {
							_value = e.toitem.value;
							value = _value.province +  _value.city +  _value.district +  _value.street +  _value.business;
						}    
						str += "<br />ToItem<br />index = " + e.toitem.index + "<br />value = " + value;
						G("searchResultPanel").innerHTML = str;

					});

					var myValue;
					ac.addEventListener("onconfirm", function(e) {    //鼠标点击下拉列表后的事件
					var _value = e.item.value;
						myValue = _value.province +  _value.city +  _value.district +  _value.street +  _value.business;
						G("searchResultPanel").innerHTML ="onconfirm<br />index = " + e.item.index + "<br />myValue = " + myValue;
						//输入框回显
						$("#suggestId").val(myValue);
						// $("#or_start").val(myValue);
						setPlace();
					});





					function setPlace(){
						map.clearOverlays();    //清除地图上所有覆盖物
						function myFun(){
							var pp = local.getResults().getPoi(0).point;    //获取第一个智能搜索的结果
							map.centerAndZoom(pp, 16);
							map.addOverlay(new BMap.Marker(pp));    //添加标注
							$("#long").val(pp.lng);
							$("#lati").val(pp.lat);
							var gc = new BMap.Geocoder();
							gc.getLocation(pp,function(rs){
								var addComp = rs.addressComponents;
								var address = addComp.province +  addComp.city +  addComp.district +  addComp.street;
								$("#suggestId").val(address);
								$("#sskin_se").val(addComp.province);
								$("#sskin_si").val(addComp.city);
								$("#sskin_qu").val(addComp.district);
								$("#sskin_xi").val(addComp.street);
							});
							window.gotLocation = 1;
						}
						var local = new BMap.LocalSearch(map, { //智能搜索
						  onSearchComplete: myFun
						});
						local.search(myValue);
					}
			});
})
function showMyPos(userId)
{
	var pos;
	$.post("/t/getUserPos",
        {userid:userId,},
        function(data){
        if(data!="error")
        {
            pos = eval(data);
            var p = new BMap.Point(pos[0].lon, pos[0].lat);
            var gc = new BMap.Geocoder();
				gc.getLocation(p,function(rs){
					var addComp = rs.addressComponents;
					var address = addComp.province +  addComp.city +  addComp.district +  addComp.street;
					$("#long").val(pos[0].lon);
					$("#lati").val(pos[0].lat);
					$("#suggestId").val(address);
					$("#sskin_se").val(addComp.province);
					$("#sskin_si").val(addComp.city);
					$("#sskin_qu").val(addComp.district);
					$("#sskin_xi").val(addComp.street);
				});
        }
        else{
            alert("无位置信息,请选择地图模式获取！");
        }
      });
         
}