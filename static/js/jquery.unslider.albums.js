$(document).ready(function(){
    $('.album-cover').each(function(){
        var $delay = +$(this).data('delay');
        $(this).unslider({
            autoplay : true,
            delay : $delay,
            keys : false,
            nav : false,
            arrows : false,
            animation : 'fade'
        });
    });
});
