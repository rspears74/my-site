var main = function(){
  $('.button1').hover(function(){
    $(this).toggleClass('active');
    $(this).children().toggleClass('txtactive');
  });
  $('.button1').mousedown(function(){
    $(this).addClass('clicked');
  });
  $('.button1').mouseup(function(){
    $(this).removeClass('clicked');
  });
  $('.button1').click(function(){
    $('.list').slideUp(250);
    $('.button1').removeClass('clicked');
    buttonid = $(this).attr('id');
    listid = "#" + buttonid.slice(0, -1);
    if($(listid).css('display') === 'none') {
      $(listid).slideToggle(250);
      $(this).addClass('clicked');
    };
  });
  $('.listcontainer').hover(function(){
    $(this).toggleClass('imgactive');
  });
  $('.btn2').hover(function(){
    $(this).toggleClass('btn2-active');
  });
};


$(document).ready(main);
