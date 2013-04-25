$(function(){

    $(".index_sp").click(function(){ 
        $item = $(this)
        $itemid = $item.attr("data-id") 
		res = $.ajax({
			url:"/shopping/"+$itemid,type:"get",dataType:"json",data:{"type":"json"},
                success:function (data) {
				    $.facebox($(data.html));			
			        }/*,error:function (XMLHttpRequest, textStatus, errorThrown){
				alert(XMLHttpRequest);
				alert(textStatus);
				alert(errorThrown);
				alert(this);
			} */
		})
    })
})
