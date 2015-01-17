$(document).ready(function(){
	var conName = $(".udetail input[data='answer1']").attr("name");
		var con = $(".udetail input[data='answer1']").parents("p").prev("p").children("label").next().html();
		if(con.indexOf("生日") == "-1"){
		}
		else{
			$(".udetail input[data='answer1']").after($("#cloneInput :input").clone(true));
			$(".udetail input[data='answer1']").next("input").attr("style","");
			$(".udetail input[data='answer1']").next("input").attr("id",conName);
			$(".udetail input[data='answer1']").next("input").attr("name",conName);
			$(".udetail input[data='answer1']").remove();
		}

		var conName = $(".udetail input[data='answer2']").attr("name");
		var con = $(".udetail input[data='answer2']").parents("p").prev("p").children("label").next().html();
		if(con.indexOf("生日") == "-1"){
		}
		else{
			$(".udetail input[data='answer2']").after($("#cloneInput :input").clone(true));
			$(".udetail input[data='answer2']").next("input").attr("style","");
			$(".udetail input[data='answer2']").next("input").attr("id",conName);
			$(".udetail input[data='answer2']").next("input").attr("name",conName);
			$(".udetail input[data='answer2']").remove();
		}

		var conName = $(".udetail input[data='answer3']").attr("name");
		var con = $(".udetail input[data='answer3']").parents("p").prev("p").children("label").next().html();
		if(con.indexOf("生日") == "-1"){
		}
		else{
			$(".udetail input[data='answer3']").after($("#cloneInput :input").clone(true));
			$(".udetail input[data='answer3']").next("input").attr("style","");
			$(".udetail input[data='answer3']").next("input").attr("id",conName);
			$(".udetail input[data='answer3']").next("input").attr("name",conName);
			$(".udetail input[data='answer3']").remove();
		}
	});