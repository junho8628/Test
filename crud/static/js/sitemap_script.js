jQuery(document).ready(function(){    
    
    //새로고침시 처음화면으로 이동
    $(document).keydown(function(e){
        if(e.keyCode==116){
            document.location.href="http://127.0.0.1:5000/";
            return false;
        }
    });
    //input 값 localStorage에 저장
    window.a=function() {
        localStorage.in_txt = $('#input_search').val();
    }
    //localStorage에 저장된 값을 input 에 넣기
    function set_val(){
        var now_url = window.location.href;
        if(now_url == 'http://127.0.0.1:5000/search'){
            $('#input_search').val(localStorage.in_txt);
        }
        
    }


    window.onload=set_val();

    'use strict'
  
    $('[data-toggle="tooltip"]').tooltip();
      
    // set active contact from list to show in desktop view by default
    if(window.matchMedia('(min-width: 992px)').matches) {
      $('#one_depth .media:first-of-type').addClass('active');
    }
      
      
    const contactSidebar = new PerfectScrollbar('.contact-sidebar-body', {
      suppressScrollX: true
    });
      
    new PerfectScrollbar('.contact-content-body', {
      suppressScrollX: true
   });
      
    new PerfectScrollbar('.contact-content-sidebar', {
      suppressScrollX: true
    });
      
    $('.contact-navleft .nav-link').on('shown.bs.tab', function(e) {
      contactSidebar.update()
    })
      
    // UI INTERACTION
    $(document).on('click','.contact-list .media',function(e){
      e.preventDefault();
      
      if($(this).parent().attr('id')=="one_depth"){
        $('.contact-list .media').removeClass('active');
        $(this).addClass('active');
      }
      if($(this).parent().attr('id')=="two_depth"){
        $('#two_depth .media,#three_depth .media').removeClass('active');
        $(this).addClass('active');
      }
      if($(this).parent().attr('id')=="three_depth"){
        $('#three_depth .media').removeClass('active');
        $(this).addClass('active');
      }

      var cValue = $(this).find('li').val();
      $('#contactName').find('li').val(cValue);
      
      var cName = $(this).find('h6').text();
      $('#contactName').find('li').text(cName);

      var cdescribe = $(this).find('.tx-12').text();
      $('#contactDescribe').text(cdescribe);

      var cAvatar = $(this).find('.avatar').clone();
      
      cAvatar.removeClass (function (index, className) {
        return (className.match (/(^|\s)avatar-\S+/g) || []).join(' ');
      });
      cAvatar.addClass('avatar-xl');
      
      $('#contactAvatar .avatar').replaceWith(cAvatar);
      
      
      // showing contact information when clicking one of the list
      // for mobile interaction only
      if(window.matchMedia('(max-width: 991px)').matches) {
        $('body').addClass('contact-content-show');
        $('body').removeClass('contact-content-visible');
      
        $('#mainMenuOpen').addClass('d-none');
        $('#contactContentHide').removeClass('d-none');
      }
    })
      
      
    // going back to contact list
    // for mobile interaction only
    $('#contactContentHide').on('click touch', function(e){
      e.preventDefault();
      
      $('body').removeClass('contact-content-show contact-options-show');
      $('body').addClass('contact-content-visible');
      
      $('#mainMenuOpen').removeClass('d-none');
      $(this).addClass('d-none');
    });
      
    $('#contactOptions').on('click', function(e){
      e.preventDefault();
      $('body').toggleClass('contact-options-show');
    })
      
    $(window).resize(function(){
      $('body').removeClass('contact-options-show');
    })
    
    $(document).on('click','#one_depth .media',function(e){
      //2depth
      e.preventDefault();
      var onedepth_val = $(this).find('li').val();
      $('#two_depth').empty();
      $('#three_depth').empty();
      $.ajax({
        type:'POST',
        url:'http://127.0.0.1:5000/click',
        data : 
          {'pid' : onedepth_val} ,
        dataType:'JSON',
        success:function(result){
          var obj = JSON.parse(JSON.stringify(result))
          for (i=0; i<Object.keys(obj).length; i++) {
            var list_two = document.createElement('div');
            list_two.setAttribute('class','media');
            list_two.setAttribute('id','two_depth_list');
            list_two.innerHTML = "<div class='media-body mg-l-10'><h6 class='tx-13 mg-b-3'><li value="+obj[i].id+">"+ obj[i].title +"</h6>"+
            "<span class='tx-12'>"+obj[i].describe+"</span></div><nav><a href=''><svg xmlns='http://www.w3.org/2000/svg' width='24' height='24'"+
            "viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' class='feather feather-star'>"+
            "<polygon points='12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2'></polygon></svg></a></nav>";
            document.getElementById('two_depth').appendChild(list_two);
          }
        }
      });
    })
    $(document).on('click','#two_depth .media',function(e){
      //3depth
      e.preventDefault();
      var twodepth_val = $(this).find('li').val();
      $('#three_depth').empty();
      $.ajax({
        type:'POST',
        url:'http://127.0.0.1:5000/click',
        data : 
          {'pid' : twodepth_val} ,
        dataType:'JSON',
        success:function(result){
          var obj = JSON.parse(JSON.stringify(result))
          for (i=0; i<Object.keys(obj).length; i++) {
            var list_two = document.createElement('div');
            list_two.setAttribute('class','media');
            list_two.setAttribute('id','three_depth_list');
            list_two.innerHTML = "<div class='media-body mg-l-10'><h6 class='tx-13 mg-b-3'><li value="+obj[i].id+">"+ obj[i].title +"</h6>"+
            "<span class='tx-12'>"+obj[i].describe+"</span></div><nav><a href=''><svg xmlns='http://www.w3.org/2000/svg' width='24' height='24'"+
            "viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' class='feather feather-star'>"+
            "<polygon points='12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2'></polygon></svg></a></nav>";
            document.getElementById('three_depth').appendChild(list_two);
          }
        }
      });
    })

    $(document).on('click','#gourl',function(e){
      e.preventDefault();
      var urlid=$('#contactName').find('li').val();
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
    })
    $(document).on('click','#submit-btn',function(e){
      e.preventDefault();
      $('#first-page,#listView').removeClass('active');
      $('#second-page,#contactLogs').addClass('active');
      $('#search_depth').empty();
      var search_txt=$("#submit-txt").val();
      $.ajax({
        type:'POST',
        url:'http://127.0.0.1:5000/search',
        data : 
          {'txtsearch' : search_txt} ,
        dataType:'JSON',
        success:function(result){
          var obj = JSON.parse(JSON.stringify(result))
          for (i=0; i<Object.keys(obj).length; i++) {
            var search_list = document.createElement('div');
            search_list.setAttribute('class','media');
            search_list.setAttribute('id','search_depth_list');
            search_list.innerHTML = "<div class='media-body mg-l-10'><h6 class='tx-13 mg-b-3'><li value="+obj[i].id+">"+ obj[i].title +"</h6>"+
            "<span class='tx-12'>"+obj[i].describe+"</span></div><nav><a href=''><svg xmlns='http://www.w3.org/2000/svg' width='24' height='24'"+
            "viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' class='feather feather-star'>"+
            "<polygon points='12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2'></polygon></svg></a></nav>";
            document.getElementById('search_depth').appendChild(search_list);
          }
        }
      })
    })
    $('#submit-txt').keydown(function(key){
      if(key.keyCode==13){
        $('#submit-btn').click();
      }
    })
});