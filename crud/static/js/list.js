$(document).ready(function(){
    //2depth 출력
    $(document).on('click','#rounded-list>li',function(){ 
        var oneval = $(this).val();
        if($(this).attr("data-loaded")=='yes') {
            $.ajax({
                type:'POST',
                url:'http://127.0.0.1:5000/click',
                data : 
                    {'pid' : oneval} ,
                dataType:'JSON',
                success:function(result){
                    var obj = JSON.parse(JSON.stringify(result))
                    for (i=0; i<Object.keys(obj).length; i++) {
                        var list_two = document.createElement('li');
                        list_two.setAttribute('value',obj[i].id);
                        list_two.setAttribute('data-loaded','yes');
                        list_two.innerHTML = "<a href=''>"+ obj[i].title +
                        "<input class ='gobtn' type = 'button' name = 'urlbtn' value ='이동'><input class ='openbtn' type = 'button' name = 'describebtn' value ='설명'></a>"+
                        "<ol class = 'submenu2' id = "+obj[i].id+"> </ol>";
                        document.getElementById('onedepth_'+oneval).appendChild(list_two);
                    }
                }
            });
            $(this).attr("data-loaded","no");
        }
        else if($(this).attr("data-loaded")=='no'){
            $(this).find('ol').empty();
            $(this).attr("data-loaded","yes");
        }
        return false;
    });
     //3depth 출력
    $(document).on('click','.submenu>li',function(){
        if($(this).attr("data-loaded")=='yes') {
            var twoval = $(this).val();
            $.ajax({
                type:'POST',
                url:'http://127.0.0.1:5000/click',
                data : 
                    {'pid' : twoval} ,
                dataType:'JSON',
                success:function(result){
                    var obj = JSON.parse(JSON.stringify(result))
                    for (i=0; i<Object.keys(obj).length; i++) {
                        var list_three = document.createElement('li');
                        list_three.setAttribute('value',obj[i].id);
                        list_three.innerHTML = "<a href=''>"+ obj[i].title +
                        "<input class ='gobtn' type = 'button' name = 'urlbtn' value ='이동'><input class ='openbtn' type = 'button' name = 'describebtn' value ='설명'></a>";
                        document.getElementById(twoval).appendChild(list_three);
                    }
                }
            });
            $(this).attr("data-loaded","no");
        }else if($(this).attr("data-loaded")=='no'){
            $(this).find('ol').empty();
            $(this).attr("data-loaded","yes");
        }
        return false;
    });
    //url 이동
    $(document).on('click','.gobtn',function(){
        var urlid = $(this).parent().parent().val();
        go_url(urlid);
        return false;
    });
    // 팝업창 띄우기
    $(document).on('click','.openbtn',function(){
        var desid = $(this).parent().parent().val();
        open(desid);
        return false;
    });
    //url 함수
    function go_url(urlid){
        $.ajax({
                type:'POST',
                url:'http://127.0.0.1:5000/urlclick',
                data : 
                    {'urlid' : urlid} ,
                dataType:'JSON',
                success:function(result){
                    var basic_url = "https://dev.zioyou.com";
                    window.open(basic_url+result['url'],'newpop');
                }
            });
    }
    //팝업창 함수
    function open(desid){ 
        $.ajax({
            type:'POST',
            url:'http://127.0.0.1:5000/desclick',
            data : 
                {'desid' : desid} ,
            dataType:'JSON',
            success:function(result){
                var a = document.getElementById('desc');
                a.innerHTML="<h3>"+result['title']+"</h3><p>"+result['describe']+"</p><a href='' class='close close1'>"+
                    "<svg viewBox='0 0 24 24'>"+
                    "<path d='M14.1,12L22,4.1c0.6-0.6,0.6-1.5,0-2.1c-0.6-0.6-1.5-0.6-2.1,0L12,9.9L4.1,2C3.5,1.4,2.5,1.4,2,2C1.4,2.5,1.4,3.5,2,4.1"+
                    "L9.9,12L2,19.9c-0.6,0.6-0.6,1.5,0,2.1c0.3,0.3,0.7,0.4,1.1,0.4s0.8-0.1,1.1-0.4l7.9-7.9l7.9,7.9c0.3,0.3,0.7,0.4,1.1,0.4"+
                    "s0.8-0.1,1.1-0.4c0.6-0.6,0.6-1.5,0-2.1L14.1,12z'/></svg></a>";
                $("#modal").removeAttr("class").addClass("one");
                dele();
            }
        })
    }
     // 팝업창 닫기
    function dele(){
        $(".close").click(function(){
            $("#modal").addClass("out");
            return false;
        });
    }
    window.onkeydown = function(){
        var kcode = event.keyCode;
        if(kcode == 116) {
            history.replaceState({},null,location.pathname)
        }
    }
});