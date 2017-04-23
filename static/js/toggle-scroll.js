$(document).ready(function(){
    $('.scroll').children('footer').children('a').on('click', function(e){
        e.preventDefault();
        e.stopPropagation();
        toggleScroll($(this).closest('article.scroll'));
    });
});

function toggleScroll($scroll) {
    var $scrolled = $($scroll).children('section.scrolled');
    var $unscrolled = $($scroll).children('section.unscrolled');
    if ($($scroll).children('footer').hasClass('scrolled')) {
        $($scroll).children('footer').addClass('unscrolled').removeClass('scrolled');
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
}
