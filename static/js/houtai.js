$(function(){
     
    $(".add").click(function(){ 
        $item = $(this)
        $itemid = $item.attr("data-id") 
		res = $.ajax({
			url:"/matchdata",type:"post",dataType:"json",data:{"action":"add","item":$itemid},
                success:function (data) {
				    $.facebox(data.html);
                    $item.parents("table").remove()
			        }/*,error:function (XMLHttpRequest, textStatus, errorThrown){
				alert(XMLHttpRequest);
				alert(textStatus);
				alert(errorThrown);
				alert(this);
			} */
		})
    })

    $(".match").click(function(){ 
        $pr= $(this)
        $prid = $pr.attr("data-id") 
        $itemid = $pr.parents("table").find(".add").attr("data-id")
		res = $.ajax({
			url:"/matchdata",type:"post",dataType:"json",data:{"action":"match","item":$itemid,"pr":$prid},
                success:function (data) {
				    $.facebox(data.html);
                    $pr.parents("table").remove()
			        }/*,error:function (XMLHttpRequest, textStatus, errorThrown){
				alert(XMLHttpRequest);
				alert(textStatus);
				alert(errorThrown);
				alert(this);
			} */
		})
    })

    $(".key_name").click(function(){
        $(this).next("table").toggle()    
    })

})

