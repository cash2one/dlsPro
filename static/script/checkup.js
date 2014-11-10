function searchearth()
{
	var obj = document.getElementsByName("search_tiaojian")[0];
	var index = obj.selectedIndex; // 选中索引
	//var text = obj.options[index].text; // 选中文本
	var value = obj.options[index].value; // 选中值
	var zhi = document.getElementsByName("search_value")[0].value;
	location.href = "/t/checkup?value="+value+"&zhi="+zhi;
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
    for(var i=0;i<l.length;i++)
    {
        var c = l[i].childNodes;//分类名
        alert(l[i].length);
    }
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
