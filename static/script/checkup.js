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