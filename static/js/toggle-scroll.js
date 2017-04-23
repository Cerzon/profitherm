$(document).ready(function(){
    $('.scroll-control').on('click', function(e){
        e.preventDefault();
        e.stopPropagation();
        toggleScroll($(this).closest('.scroll'));
    });
    $('.scroll-up-all').on('click', function(e){
        e.preventDefault();
        e.stopPropagation();
        toggleScroll($('.scroll-control').filter('.scroll-up').closest('.scroll'));
    });
    $('.unscroll-all').on('click', function(e){
        e.preventDefault();
        e.stopPropagation();
        toggleScroll($('.scroll-control').filter('.un-scroll').closest('.scroll'));
    });
});

function toggleScroll($scroll) {
    var $scrolled = $scroll.children('.scrolled');
    var $unscrolled = $scroll.children('.unscrolled');
    var $control = $scroll.find('.scroll-control');
    if ($control.hasClass('scroll-up')) {
        $control.addClass('un-scroll').removeClass('scroll-up');
    }
    else {
        $control.addClass('scroll-up').removeClass('un-scroll');
    }
    $control.text('');
    $unscrolled.slideUp(400, function(){
        $scrolled.slideDown(400, function(){
            if ($control.hasClass('un-scroll')) {
                $control.text('развернуть');
            }
            else {
                $control.text('свернуть');
            }
            $unscrolled.removeClass('unscrolled').addClass('scrolled');
        }).removeClass('scrolled').addClass('unscrolled');
    });
}
