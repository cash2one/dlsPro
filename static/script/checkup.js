var eqidt;
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
function chooseeq(eqid)
{
    $.post("/t/checkup",
        {infolist:eqid,
        type :"ajax",
        },
        function(data){
        if(data=="success")
        {
            location.href = "/t/checkup2"
        }
    });
}
function showInfo(e) {
    index = e.target.no;//获取标注编号,由于和数组d的下标是一一对应的，所以可以直接通过index取数据
    //传个hmtl的参数
    info.setContent("<div style='font-weight:bold'>发震时刻:" + d[index].eqTime + "<br>经度: " + d[index].eqLongitude + "<br>纬度 :" + d[index].eqLatitude
            +"<br>地震名称:" + d[index].eqName + "<br>震级:" + d[index].eqMagnitude + "<br>参考位置:" + d[index].eqLocation 
            +"<br><p style='float:right'><a style='color:blue';float:right' href='javascript:void(0)' onclick='chooseeq(\""+d[index].eqId+"\")' >选择此地震</a></p>");
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
    if(level<3){
        path = "/static/img/sxm2.png";}
    else if(level<5){
        path = "/static/img/sxm3.png";}
    else {
        path = "/static/img/sxm1.png";}
    // if(level>4)
    // {
    //  path = "/static/img/pic3" + level + ".png";
    // }
    // else
    // {
    //  path = "/static/img/pic3" + level + "r.png";
    // }
    myIcon = new BMap.Icon(path, new BMap.Size(30, 30));
    
    marker = new MMarker(no,point,{icon: myIcon});//创建标注，并用自己的图片替换掉系统默认的标注图片
    marker.addEventListener("click", showInfo);//给标记添加事件

    return marker;//返回标注
 }

 


function check1(data) {
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
    var obj = document.getElementsByName("search_tiaojian")[0];
    var index = obj.selectedIndex; // 选中索引
    //var text = obj.options[index].text; // 选中文本
    var value = obj.options[index].value; // 选中值
    var zhi = document.getElementsByName("search_value")[0].value;
    // location.href = "/t/checkup?value="+value+"&zhi="+zhi;
    $.post("/t/checkEqMap",
        {value:value,
         zhi:zhi,
        },
        function(data){
        if(data.length>0)
        {
            var ind = data.indexOf("pageleng:");
            var data1 = data.substr(0,ind);
            var pagenumdata = data.substr(ind+9,data.length);//页数信息
            var pageleng = pagenumdata.substr(0,pagenumdata.indexOf("nowpage:"));
            var pagenow = pagenumdata.substr(pagenumdata.indexOf("nowpage:")+8,pagenumdata.length);
            d = eval(data1);
            // var ss = eval(data);
            // d = ss;
            for (i=0; i < d.length; i++) {  
            pt = new BMap.Point(d[i].eqLongitude, d[i].eqLatitude);
            // alert(d[i].address);
            marker = setIconColor(pt,d[i].eqMagnitude,i);//i表示标注的编号，pt是点，1代表采用的图例
            map.addOverlay(marker);  
            }
            $("#infolistbg tr:gt(0)").remove();
            for(var i =0;i<d.length;i++)
            {
                if(i==0){
                    $("#infolistbg").append("<tr><td class=\"f\"><input type=\"radio\" name=\"infolist\" checked=\"true\" value='"+d[i].eqId+"'/></td>");
                }
                else
                {
                    $("#infolistbg").append("<tr><td class=\"f\"><input type=\"radio\" name=\"infolist\" value='"+d[i].eqId+"'/></td>");
                }
                $("#infolistbg tr:last").append("<td>"+d[i].eqId+"</td>");
                $("#infolistbg tr:last").append("<td><a href=\"javascript:void(0)\" onclick=\"showModel('"+d[i].eqId+"')\">"+d[i].eqName+"</a></td>");
                $("#infolistbg tr:last").append("<td>"+d[i].eqTime+"</td>");
                // $("#infolistbg tr:last").append("<td></td>");
                $("#infolistbg tr:last").append("<td>"+d[i].eqDepth+"</td>");
                $("#infolistbg tr:last").append("<td>"+d[i].eqMagnitude+"</td>");
                $("#infolistbg tr:last").append("<td>"+d[i].eqLongitude+"</td>");
                $("#infolistbg tr:last").append("<td>"+d[i].eqLatitude+"</td>");
                $("#infolistbg tr:last").append("<td>"+d[i].eqLiedu+"</td>");
                $("#infolistbg").append("</tr>");
            }
            $("#pagestyle li").remove();
            if(pageleng>1&&pagenow>1){
                $("#pagestyle").append("<li> <a  title='上一页' href='javascript:void(0);' onclick='pageclick("+(pagenow-1)+")'><span>&lt;&lt;</span></a></li>");
            }
            for(var q = 1;q<=pageleng;q++)
            {
                if(q==pagenow)
                {
                    $("#pagestyle").append("<li>  <a  title='当前页:"+pagenow+"'><span>"+pagenow+"</span></a></li>");
                }
                else
                    $("#pagestyle").append("<li>  <a  href='javascript:void(0);' onclick='pageclick("+q+")' title='跳转到第"+q+"页'><span>"+q+"</span></a></li>");
            } 
            if(pagenow<pageleng)
            {
                var pagenex = parseInt(pagenow) + 1;
                $("#pagestyle").append("<li> <a  title='下一页' href='javascript:void(0);' onclick='pageclick("+(pagenex)+")'><span>&gt;&gt;</span></a></li>");
            }
        }
        else{
            alert(data);
        }
      });
}

function pageclick(pagenum)
{
    // alert(pagenum);
    var obj = document.getElementsByName("search_tiaojian")[0];
    var index = obj.selectedIndex; // 选中索引
    //var text = obj.options[index].text; // 选中文本
    var value = obj.options[index].value; // 选中值
    var zhi = document.getElementsByName("search_value")[0].value;
      $.post("/t/checkEqMap",
        {value:value,
         zhi:zhi,
        },
        function(data){
        if(data.length>0)
        {
            alert(data);
            // var data1;
            // data1 = eval(data);
            var ind = data.indexOf("pageleng:");
            var data1 = data.substr(0,ind);
            var pagenumdata = data.substr(ind+9,data.length);//页数信息
            var pageleng = pagenumdata.substr(0,pagenumdata.indexOf("nowpage:"));
            var pagenow = pagenumdata.substr(pagenumdata.indexOf("nowpage:")+8,pagenumdata.length);
            data1 = eval(data1);

            $("#infolistbg tr:gt(0)").remove();
            for(var i =0;i<d.length;i++)
            {
                if(i==0){
                    $("#infolistbg").append("<tr><td class=\"f\"><input type=\"radio\" name=\"infolist\" checked=\"true\" value='"+d[i].eqId+"'/></td>");
                }
                else
                {
                    $("#infolistbg").append("<tr><td class=\"f\"><input type=\"radio\" name=\"infolist\" value='"+d[i].eqId+"'/></td>");
                }
                $("#infolistbg tr:last").append("<td>"+d[i].eqId+"</td>");
                $("#infolistbg tr:last").append("<td><a href=\"javascript:void(0)\" onclick=\"showModel('"+d[i].eqId+"')\">"+d[i].eqName+"</a></td>");
                $("#infolistbg tr:last").append("<td>"+d[i].eqTime+"</td>");
                // $("#infolistbg tr:last").append("<td></td>");
                $("#infolistbg tr:last").append("<td>"+d[i].eqDepth+"</td>");
                $("#infolistbg tr:last").append("<td>"+d[i].eqMagnitude+"</td>");
                $("#infolistbg tr:last").append("<td>"+d[i].eqLongitude+"</td>");
                $("#infolistbg tr:last").append("<td>"+d[i].eqLatitude+"</td>");
                $("#infolistbg tr:last").append("<td>"+d[i].eqLiedu+"</td>");
                $("#infolistbg").append("</tr>");
            }
            $("#pagestyle li").remove();
            if(pageleng>1&&pagenow>1){
                $("#pagestyle").append("<li> <a  title='上一页' href='javascript:void(0);' onclick='pageclick("+(pagenow-1)+")'><span>&lt;&lt;</span></a></li>");
            }
            for(var q = 1;q<=pageleng;q++)
            {
                if(q==pagenow)
                {
                    $("#pagestyle").append("<li>  <a  title='当前页:"+pagenow+"'><span>"+pagenow+"</span></a></li>");
                }
                else
                    $("#pagestyle").append("<li>  <a  href='javascript:void(0);' onclick='pageclick("+q+")' title='跳转到第"+q+"页'><span>"+q+"</span></a></li>");
            } 
            if(pagenow<pageleng)
            {
                var pagenex = parseInt(pagenow) + 1;
                $("#pagestyle").append("<li> <a  title='下一页' href='javascript:void(0);' onclick='pageclick("+(pagenex)+")'><span>&gt;&gt;</span></a></li>");
            }

        }

    });
}
function checkup2commit()
{
    var obj = $(".sclazlist tr .hover");
     $.post("/t/checkup2",
        {name:obj.attr("data")},
        function(data){
        if(data=="success")
        {
            location.href = 'checkup3';
        }
        else{
            alert(data);
        }
      });
}
function checkpage(page)
{
	// alert(page);
	var obj = document.getElementsByName("search_tiaojian")[0];
	var index = obj.selectedIndex; // 选中索引
	//var text = obj.options[index].text; // 选中文本
	var value = obj.options[index].value; // 选中值
	var zhi = document.getElementsByName("search_value")[0].value;
	location.href = "/t/checkup"+page+"&value="+value+"&zhi="+zhi;
}
// checkup5提交按钮提取页面内容
function checkcommit()
{

    var l = $('[name="location"]');//部位
    var location_id;
    var cata_id;
    var sub_id;
    var json_obj="";
    for(var i=0;i<l.length;i++)
    {
        location_id = l[i].id;
        var c = $("#"+location_id).find(".catacontentmark");//分类名
        for(var j=0;j<c.length;j++)
        {
            cata_id = c[j].id;
            var s =  $("#"+cata_id).find(".dlisf");//细部名
            for(var y=0;y<s.length;y++)
            {
                sub_id = s[y].id;//每一个细部
                var item = $("#"+sub_id).find(".item");//item
                for (var q = 0; q<item.length; q++) {
                    //此处获取每一项的值。
                    var itemx = item[q];//第q个item
                    var test = itemx.getElementsByTagName("input");
                    var num_name = test[0].name;
                    var level_name = test[4].name;
                    var num = $(':radio[name='+num_name+']:checked').val();
                    var level = $(':radio[name='+level_name+']:checked').val();
                    var describe = test[6].value;
                    var weitiao = test[7].value;
                    if(q==0)
                    {
                        var ss = "{'damage_locationid':"+location_id.replace("location_","")+",'damage_catalogid':"+cata_id.replace("cata_","")+",'damage_sublocationid':"+sub_id.replace("dlisf","")+",'damage_number':'"+num+"','damage_degree':'"+level+"','damage_description':'"+describe+"','damage_parameteradjust':'"+weitiao+"','damage_isfirst':'yes'}*";
                    }else{
                        var ss = "{'damage_locationid':"+location_id.replace("location_","")+",'damage_catalogid':"+cata_id.replace("cata_","")+",'damage_sublocationid':"+sub_id.replace("dlisf","")+",'damage_number':'"+num+"','damage_degree':'"+level+"','damage_description':'"+describe+"','damage_parameteradjust':'"+weitiao+"','damage_isfirst':'no'}*";
                    }
                    json_obj = json_obj+ss;
                }
        
            }
            
        }
    }
    var shuju = json_obj.substring(0,json_obj.length-1);
    // var shuju = "["+json_obj.substring(0,json_obj.length-1)+"]";
        // alert("正在鉴定,请耐心等待！");
        // alert(shuju);
       $.post("/t/checkup5",
        {name:shuju,cache:$(".tip").html(),},
        function(data){
        if(data=="success")
        {
            location.href = 'checkup6';
        }
        else{
            alert(data);
        }
      });
}

function showModel(eqid)
{
    var value=eqid;
    var xmlhttp;
    var json;
    $("#myEqModal").modal({
        show:true,
        backdrop:true
       });
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else
     {// code for IE6, IE5
         xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function()
    {
    if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
         json=xmlhttp.responseText;
         // var json_obj = json.parseJSON();
         // var json_obj = JSON.parse(json);
         var str = json.split(",");
         // alert(str[0]);
         var bianhao = document.getElementsByName("bianhao");
         for(var i=0;i<bianhao.length;i++)
            {
                if(i==0)
                {
                    eqidt = str[i];
                }
                bianhao[i].innerHTML = str[i];
                // alert(str[i]);
            }
    }
  }
    xmlhttp.open("GET","/t/check_eq?eq_id="+value,true);
    xmlhttp.send();  
     
}





$(document).ready(function ()
{
    
    $("#addimage_confirm").click(function(){
        $("#addImage").modal("hide");
    });

    $("#eq_confirm").click(function(){
        $("input[name='infolist']").attr("checked","false");
        $("input[name='infolist'][value='"+eqidt+"']").attr("checked","true");
        $("#myEqModal").modal("hide");
    });
    // $('#form1').bind('submit', function(){
    //     $.ajax({
    //             cache: false,
    //             type: "POST",
    //             url:"/t/addImage/front",
    //             data:$('#form1').serialize(),// 你的formid
    //         });
    //     // return false;
    // });
    check1(1);

});       
 //将form转为AJAX提交
// function ajaxSubmit(frm, fn) {
//     var dataPara = getFormJson(frm);
//     $.ajax({
//         url: frm.action,
//         type: frm.method,
//         data: dataPara,
//         success: fn
//     });
// }

// //将form中的值转换为键值对。
// function getFormJson(frm) {

//     var o = {};
//     var a = $(frm).serialize();
//     alert(a);
//     $.each(a, function () {
//         if (o[this.name] !== undefined) {
//             if (!o[this.name].push) {
//                 o[this.name] = [o[this.name]];
//             }
//             o[this.name].push(this.value || '');
//         } else {
//             o[this.name] = this.value || '';
//         }
//     });
//     alert(o.action);
//     return o;
// }
 function callback(file_name){

          //设置刚上传的图片路径
        
    }