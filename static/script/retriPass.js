$(document).ready(function(){

	if($("#messageShow").length>0)
	{
    	$("#messageShow").fadeOut(2000);
		$("#messageShow").fadeOut("slow");
	}

	//密保
	$(".udetail .setinput").change(function(){
		var n = $(this).children('option:selected').attr("name");
		if(n == "birth"){
			var inputName = $(this).parents("p").next("p").children("input").attr("name");
			$(this).parents("p").next("p").children("input").remove();
			$(this).parents("p").next("p").children("label").after($("#cloneInput :input").clone(true));
			$(this).parents("p").next("p").children("input").attr("style","");
			$(this).parents("p").next("p").children("input").attr("id",inputName);
			$(this).parents("p").next("p").children("input").attr("name",inputName);
		}
		else{
			if($(this).parents("p").next("p").children("input").attr("data")=="validate")
			{
				var inputName = $(this).parents("p").next("p").children("input").attr("name");
				$(this).parents("p").next("p").children("div input").remove();
				$(this).parents("p").next("p").children("label").after("<input type=\"text\" name='"+inputName+"' class=\"b answer\" value='' id='"+inputName+"'/>");
			}
		}
	});

});