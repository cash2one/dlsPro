window.onbeforeunload = function (e) {
        // return e.returnValue = '确认关闭？！！';


    }
    window.onunload = function () {
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
      $.ajax({
      	url: "/t/check5save",
      	data: {name:shuju},
      	async:false,
      	type:"POST"
    });
    }
