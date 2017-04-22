$(document).ready(function(){
    $('.scroll').children('footer').children('a').on('click', function(e){
        var $scroll = $(this).closest('article.scroll');
        var $scrolled = $($scroll).children('section.scrolled');
        var $unscrolled = $($scroll).children('section.unscrolled');
        var $timefirst = 600, $timesecond = 200;
        e.preventDefault();
        e.stopPropagation();
        if ($($scroll).children('footer').hasClass('scrolled')) {
            $($scroll).children('footer').addClass('unscrolled').removeClass('scrolled');
            $timefirst = 200;
            $timesecond = 600;
        }
        else {
            $($scroll).children('footer').addClass('scrolled').removeClass('unscrolled');
        }
        $($scroll).children('footer').children('a').text('');
        $($unscrolled).slideUp(400, function(){
            $($scrolled).slideDown(400, function(){
                if ($($scroll).children('footer').hasClass('scrolled')) {
                    $($scroll).children('footer').children('a').text('развернуть');
                }
                else {
                    $($scroll).children('footer').children('a').text('свернуть');
                }
            }).removeClass('scrolled').addClass('unscrolled');
            $($unscrolled).removeClass('unscrolled').addClass('scrolled');
        });
    });
});
