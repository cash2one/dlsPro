$(document).ready(function(){

	
	$("#newpass").select();
	$("#newpass").blur(function(){
		var n=$("#newpass").val();
		if(n == "")
		{
			$("#newpass1").text("重置密码不能为空");
			$("#newpass1").show();
		}
		else
		{
			$("#newpass1").text("ok");
			$("#newpass1").hide();
		}
		if(n.length>30)
		{
			$("#newpass1").text("密码太长！");
			$("#newpass1").show();
		}
		else
		{
			$("#newpass1").text("ok");
			$("#newpass1").hide();
		}
		if(n.length<4)
		{
			$("#newpass1").text("密码太短，至少六位");
			$("#newpass1").show();
		}
		else
		{
			$("#newpass1").text("ok");
			$("#newpass1").hide();
		}
		$("#conpass").select();
	});
	$("#conpass").blur(function(){
		if($("#conpass").val()!=$("#newpass").val())
		{
			$("#conpass1").text("两次的密码不一致");
			$("#conpass1").show();
		}
		else
		{
			$("#conpass1").text("ok");
			$("#conpass1").hide();
		}
	});
	$(".reg_btn").click(function(){
		if($("#newpass1").text()=="ok"&&$("#conpass1").text()=="ok")
		{
			return true;
		}
		else{
			return false;
		}
	});

});