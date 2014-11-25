$(document).ready(function(){
	$("#tsccvn").blur(function(){
		var v=$("#tsccvn").val();
		var t=/^\d{1,}$/;
		if(v==""){
			alert("建筑物栋数不能是空！");
		}
		else if(!t.test(v)){
			alert("建筑物栋数是数字！");
		}
	});
	$("#tsccvcs").blur(function(){
		var v=$("#tsccvcs").val();
		var t=/^\d{1,}$/;
		if(v==""){
			alert("建筑物层数不能是空！");
		}
		else if(!t.test(v)){
			alert("建筑物层数是数字！");
		}
	});
	$("#tsccvcx").blur(function(){
		var v=$("#tsccvcx").val();
		var t=/^\d{1,}$/;
		if(v==""){
			alert("建筑物层数不能是空！");
		}
		else if(!t.test(v)){
			alert("建筑物层数是数字！");
		}
	});
});