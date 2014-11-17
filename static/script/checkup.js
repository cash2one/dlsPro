function searchearth()
{
	var obj = document.getElementsByName("search_tiaojian")[0];
	var index = obj.selectedIndex; // 选中索引
	//var text = obj.options[index].text; // 选中文本
	var value = obj.options[index].value; // 选中值
	var zhi = document.getElementsByName("search_value")[0].value;
	location.href = "/t/checkup?value="+value+"&zhi="+zhi;
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
        alert("正在鉴定,请耐心等待！");
        // alert(shuju);
       $.post("/t/checkup5",
        {name:shuju,},
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



$(document).ready(function ()
{
 $("#infolistbg :radio").change(function ()
{               
    var value=$(this).val();
    var xmlhttp;
    var json;
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
                bianhao[i].innerHTML = str[i];
                // alert(str[i]);
         
            }
    }
  }
    xmlhttp.open("GET","/t/check_eq?eq_id="+value,true);
    xmlhttp.send();       
});
});       
