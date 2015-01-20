$(document).ready(function(){
	$.post("/n/shownews",
		{qstring1:"qstring",},
		function(data){
			var d = eval(data);
			for(i=0; i<d.length; i++){
				$(".news .list").append("<dt><a target='_blank' href='/n/newsdetail?newsid="+d[i].newsid+"'>"+d[i].newstitle+"</a></dt><dd>"+d[i].adddate+"</dd>");
			}
		}
		)

	// 友情链接
	$(".footer #about1 .links").click(function(){
		var i = $(".footer #about2").css("display");
		if(i == "none"){
			$(".footer #about2").css("display","block");
		}
		else{
			$(".footer #about2").css("display","none");
		}
	});

	$(".footer #about2 #link").click(function(){
		var c = $(this).attr("class");
		var ii = $(".footer #"+c).css("display");
		if(ii == "none"){
			$(".footer #"+c).css("display","block");
			$(".footer #"+c).prevAll(".sonabout").css("display","none");
			$(".footer #"+c).nextAll(".sonabout").css("display","none");
		}else{
			$(".footer #"+c).css("display","none");
		}
	});
});