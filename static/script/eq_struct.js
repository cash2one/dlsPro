//通过DOM来显示数据
//定义各个图表的数据源
var sj_time;
var sj_block1;
function create(td_name,block,area) {
	//通过DOM方式把表格加到页面
	$tbody = $("<tbody></tbody>");
    for(var i = 0; i < block.length; i++) {
    	$name = $("<td>"+ td_name[i] + "</td>");
    	$tdb = $("<td>"+ block[i] + "</td>");
    	$tda = $("<td>"+ area[i] + "</td>");
    	$tr = $("<tr></tr>");
    	$tr.append($name);
    	$tr.append($tdb);
    	$tr.append($tda);
    	$tbody.append($tr);
    }

   return $tbody;
}

function create1(td_name,block) {
    //通过DOM方式把表格加到页面
    $tbody = $("<tbody></tbody>");
    for(var i = 0; i < block.length; i++) {
        $name = $("<td>"+ td_name[i] + "</td>");
        $tdb = $("<td>"+ block[i] + "</td>");

        $tr = $("<tr></tr>");
        $tr.append($name);
        $tr.append($tdb);

        $tbody.append($tr);
    }

   return $tbody;
}

//按建成年份统计
function yearscount() {
	var td_name = ['1978年以前', '1978-1989', '1989-2001', '2001-2010', '2010~'];
	var block = [34, 21, 32, 56, 12];
	var area = [342, 214, 322, 564, 124];
	
	var b_name = [['1978年以前',34],['1978-1989',21], ['1989-2001',32], ['2001-2010',56], ['2010~',12]];
	// var a_name = [['1978年以前',342],['1978-1989',214], ['1989-2001',322], ['2001-2010',564], ['2010~',124]];
	$('#container1').highcharts({
		chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false
    },
      colors:[
                'red',
                'blue',
                'yellow',
                'green', 
                '#FF00CC',
                           
                      ],
    title: {
        text: '建成时间所占比列'
    },
    tooltip: {
	    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                color: '#000000',
                connectorColor: '#000000',
                format: '<b>{point.name}</b>:{point.percentage:.1f} %'
            }
        }
    },
    credits: {
        text: '',
        href: ''
    }
    
    ,
        series: [ {
            type: 'pie',
            name: '房屋数量占比',
            data: b_name,
            center: [230, 80],
            size:120,
            showInLegend: true,
            dataLabels: {
                enabled: true
            }
        }
       /* 
        ,{
            type: 'pie',
            name: '房屋面积占比',
            center: [150, 50],
            size:100,
            data: a_name,
            showInLegend: false,
            dataLabels: {
                enabled: true
            }
        }
        */
        ]
    });
    $("#st1").children(":gt(0)").remove();	
    $("#st1").append(create(td_name,block,area));
}

// 
//设防状况
function shefang(qstring) {
	var td_name = ['未设防', '6度设防', '7度设防', '8度设防', '9度设防'];
	var block = [22, 21, 11, 36, 12];
	var area = [342, 214, 322, 564, 124];
    var blockSum = 0;
	var pie = [['未设防',34],['6度设防',21], ['7度设防',32], ['8度设防',56], ['9度设防',12]];
	 $.post("/t/countCharts_sf",
        {qstring1:qstring,},
        function(data){
        if(data.length>0)
        {
             data = eval(data);
             td_name = data[1];
             block = data[2];
             area = data[0];
             pie = data[3];
             for(var i =0;i<block.length;i++)
             {
                blockSum += block[i];
             }
	        $('#container3').highcharts({
	    	chart: {                                                          
        },                                                                
        title: {                                                          
            text: '设防状况统计'                                     
        },                                                                
        /*xAxis: {                                                          
            categories: td_name
        },*/                                                               
       tooltip: {                                                        
            formatter: function() {                                       
                var s;                                                    
                if (this.point.name) { // the pie chart                   
                    s = ''+                                               
                        this.point.name +': '+ changeTwoDecimal(this.y/blockSum*100) +"%";         
                } else {                                                  
                    s = ''+                                               
                        this.x  +': '+ this.y;                            
                }                                                         
                return s;                                                 
            }                                                             
        },                                                              
        // labels: {                                                         
        //     items: [{                                                     
        //         html: '所占比例',                          
        //         style: {                                                  
        //             left: '40px',                                         
        //             top: '8px',                                           
        //             color: 'black'                                        
        //         }                                                         
        //     }]                                                            
        // }
        //  ,
        plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                color: '#000000',
                connectorColor: '#000000',
                format: '<b>{point.name}</b>:{point.percentage:.1f} %'
            }
        }
    },
         credits: {
             text: '',
             href: ''
         },
          
         
            colors:[
                'red',
                'blue',
                'yellow',
                'green', 
                '#FF00CC',
                           
                      ],
	        series: [{
	            type: 'pie',
	            name: '栋数所占比',
	            data: pie,
	            center: [180, 80],                                            
	            size: 120,                                                    
	            showInLegend: true,                                          
	            dataLabels: {                                                 
	                enabled: true                                            
	            }                 
	        }/*,
        {
	             type: 'column',
	             name: '面积所占比',
	             data: block
	         }, */]
	        
	    }
        );

	$("#st3").children(":gt(0)").remove();
    $("#st3").append(create(td_name,block,area));
    }});
}

//破坏等级
function pohuai(qstring) {
	var td_name = ['基本完好', '轻微破坏', '中等破坏', '严重破坏', '毁坏'];
	var block = [24, 21, 12, 36, 12];
	var area = [32, 14, 22, 6, 12];
    var blockSum = 0;
    var areaSum = 0;
	var pie = [['基本完好',34],['轻微破坏',21], ['中等破坏',32], ['严重破坏',56], ['毁坏',12]];

     $.post("/t/countCharts_degree",
        {qstring1:qstring,},
        function(data){
        if(data.length>0)
        {
             data = eval(data);
             td_name = data[2];
             pie = data[3];
             block = data[1];
             area = data[0];
             for(var i =0;i<block.length;i++)
             {
                blockSum += block[i];
                areaSum += area[i];
             }

            $('#container4').highcharts({
             chart: {
                type:'column'
        },
        title: {
            text: ''
        },
        xAxis: {
            categories: td_name
        },
        // plotOptions: {
        //     column: {     
        //         dataLabels: {
        //             enabled: true,
        //             style: {
        //                 fontWeight: 'bold'
                       
        //             },
        //             formatter: function() {
        //                 return this.y/areaSum +'%';
        //             }
        //         }
        //     }
        // },
        // tooltip: {
        //  formatter: function() {
        //     var point = this.point,
        //         s = this.x +':<b>'+ this.y +'%</b><br/>';
        //     if (point.drilldown) {
        //         s +=  point.category ;
        //     } 
        //     return s;
        // }
        // },
        // labels: {
        //     items: [{
        //         html: '所占比例',
        //         style: {
        //             left: '40px',
        //             top: '8px',
        //             color: 'black'
        //         }
        //     }]
        // },
        // credits: {
        //     text: '',
        //     href: ''
        // }
        
        // ,
        series: [
        {
            color:'#66FF00',
            type: 'column',
            name: '栋数',
            data: block
        }, 
        {
            color:'#FF0033',
            type: 'column',
            name: '面积',
            data: area
        }]
    });

   $("#st4").children(":gt(0)").remove();
    $("#st4").append(create(td_name,block,area));
    }});

}
var block_use;
var area_use;
var block_useChart;
var area_useChart;
//用途
function use(qstring) {

    $.post("/t/countCharts_use",
        {qstring1:qstring,},
        function(data){
        if(data.length>0)
        {
             data = eval(data);
            td_name = data[2];
            block_use = data[1];
            area_use = data[0];
            block_useChart = new Array(block_use.length);
            area_useChart = new Array(area_use.length);
            var sumBlock = 0;
            var sumArea = 0;
            for(var i=0;i<block_use.length;i++)
                sumBlock = sumBlock + block_use[i];
            for(var i=0;i<block_use.length;i++) {
                block_useChart[i] = block_use[i]/sumBlock*100
                block_useChart[i] = changeTwoDecimal(block_useChart[i]);
            }
            for(var i=0;i<area_use.length;i++)
                sumArea = sumArea + area_use[i];
            for(var i=0;i<area_use.length;i++) {
                area_useChart[i] = area_use[i]/sumArea*100
                area_useChart[i] = changeTwoDecimal(area_useChart[i]);
            }
            // alert(area_useChart[1]);
            if(area_useChart[0]!=0){
             $('#container5').highcharts({
            chart: {
            type: 'column'
        },

        title: {
            text: ''
        },

        xAxis: {
            labels:{
              rotation: -45
           },
            categories: td_name
        },

        yAxis: {
            allowDecimals: false,
            min: 0,
            title: {
                text: '所占比例'
            }
        },

        tooltip: {
            formatter: function() {
                return '<b>'+ this.x +'</b><br/>'+
                    this.series.name +': '+ this.y +'%<br/>'
            }
        },

        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                     enabled: true,
                     style: {
                         fontWeight: 'bold'
                     },
                        formatter: function() {
                         return this.y +'%';
                     }
                 }
            }
        },

        
        credits: {
            text: '',
            href: ''
        }
        
        ,
        series: [{
            color:'#66FF00',
            name: '栋数',
            data: block_useChart,
            stack: '用途'
            
        }, {
            color:'#FF0033',
            name: '面积',
            data: area_useChart,
            stack: '用途'

        }]
        });
    }
    $("#st5").children(":gt(0)").remove();
     // $("#st5").remove();
    $("#st5").append(create(td_name,block_use,area_use));
        }
    });
	   
}

//鉴定时间
// var sj_time = ['2013-5', '2013-6', '2013-7', '2013-8', '2013-9', '2013-10','2013-11'];
// var sj_block1 = [22,4,10,8,56,90,67];


function jianding(qstring) {
    
    //var block2 = [45, 23,24,67,78,83,13,64,96,78,40,47];
    $.post("/t/countCharts_sj",
        {qstring1:qstring,},
        function(data){
        if(data.length>0)
        {
            data = eval(data);
            sj_block1 = data[0];
            sj_time = data[1];
            // alert(sj_block1);
            $('#container6').highcharts({
        title: {
            text: '鉴定时间统计',
            x: -20 //center
        },
       
        xAxis: {
        labels:{
              rotation: -45
           },
        
            categories: sj_time
        },
        yAxis: {
           title: {
                text: '栋数'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
       
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
          credits: {
            text: '',
            href: ''
        },
        series: [ {
            color:'red',
            name: '月份鉴定数量',
            data: sj_block1     
        }]

    });
       $("#st6").children(":gt(0)").remove();

       $("#st6").append(create1(sj_time,sj_block1));
        }
        else{
            alert(data);
        }
      });   
 }

//加载函数
//addLoadEvent(struct);
addLoadEvent(yearscount);
// addLoadEvent(indexLine);
addLoadEvent(shefang);
addLoadEvent(pohuai);
addLoadEvent(use);
addLoadEvent(jianding);
function loadCountChart()
{
    var qstring = getSearchData();
    yearscount(qstring);
    shefang(qstring);
    pohuai(qstring);
    use(qstring);
    jianding(qstring);
}
function getSearchData()
{
    var qstring="";
    if($("#eqName").val()!="地震名称"){
        qstring += " and f.eq_earthquakename like '%"+$("#eqName").val()+"%' "
    }
    if($("#s1").val()!="省份")
    {
        qstring += " and a.building_province like '%"+$("#s1").val()+"%' "
    }
    if($("#s2").val()!="地级市")
    {
        qstring += " and a.building_city like '%"+$("#s2").val()+"%' "
    }
    if($("#s3").val()!="区、县")
    {
        qstring += " and a.building_district like '%"+$("#s3").val()+"%' "
    }
    if($("#structChart").val()!="JGLX")
    {
        qstring += " and e.construct_typeid like '%"+$("#structChart").val()+"%' "
    }
    if($("#useChart").val()!="YT")
    {
        qstring += " and c.building_usageid = '"+$("#useChart").val()+"' "
    }
    if($("#djChart").val()!="")
    {
        qstring += " and b.result_damagedegree = '"+$("#djChart").val()+"' "
    }
    if($("#resultChart").val()!="")
    {
        qstring += " and b.result_securitycategory = '"+$("#resultChart").val()+"' "
    }
     if($("#sfChart").val()!="qb")
    {
        qstring += " and a.building_fortificationdegree = '"+$("#sfChart").val()+"'"
    }
    return qstring;
}
changeTwoDecimal= function changeTwoDecimal(floatvar)
{
var f_x = parseFloat(floatvar);
if (isNaN(f_x))
{
alert('function:changeTwoDecimal->parameter error');
return false;
}
var f_x = Math.round(floatvar*100)/100;
return f_x;
}
$(document).ready(function(){
    $("#bgcbox").change(function()
    {
        // alert($(this).is(":checked"));
        if($(this).prop("checked"))
        {
            $(".bgcbox").prop("checked",true);
        }
        else{
            $(".bgcbox").prop("checked",false);
            $(".tabletrtdcolor").removeClass();
        }
    });

});