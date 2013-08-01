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

    $(".index_dp").click(function(){ 
        $dp = $(this)
        $dpid = $dp.attr("data-id") 
		res = $.ajax({
			url:"/danpin/"+$dpid,type:"get",dataType:"json",data:{"type":"json"},
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

    $("#nav_index_mmml").click(function(e){
        $.scrollTo('#index_mmml', 500, {offset: {top:-60, left:0}} );    
    })
    $("#nav_index_czdp").click(function(e){
        $.scrollTo('#index_czdp', 500, {offset: {top:-60, left:0}} );    
    })
    $("#nav_index_mmt").click(function(e){
        $.scrollTo('#index_mmt', 500, {offset: {top:-60, left:0}} );    
    })

    if(window.location.hash=="#mulu"){
        $.scrollTo('#index_mmml', 500, {offset: {top:-60, left:0}} );
    }
    else if(window.location.hash=="#danpin"){
        $.scrollTo('#index_mmt', 500, {offset: {top:-60, left:0}} );
    }
    else if(window.location.hash=="#shihui"){
        $.scrollTo('#index_mmt', 500, {offset: {top:-60, left:0}} );
    }

})
