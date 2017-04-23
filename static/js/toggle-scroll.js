$(document).ready(function(){
    $('.scroll').children('footer').children('a').on('click', function(e){
        e.preventDefault();
        e.stopPropagation();
        toggleScroll($(this).closest('article.scroll'));
    });
});

function toggleScroll($scroll) {
    var $scrolled = $scroll.children('section.scrolled');
    var $unscrolled = $scroll.children('section.unscrolled');
    var $footer = $scroll.children('footer');
    var $control = $footer.children('a');
    if ($footer.hasClass('scrolled')) {
        $footer.addClass('unscrolled').removeClass('scrolled');
    }
    else {
        $footer.addClass('scrolled').removeClass('unscrolled');
    }
    $control.text('');
    $unscrolled.slideUp(400, function(){
        $scrolled.slideDown(400, function(){
            if ($footer.hasClass('scrolled')) {
                $control.text('развернуть');
            }
            else {
                $control.text('свернуть');
            }
        }).removeClass('scrolled').addClass('unscrolled');
        $unscrolled.removeClass('unscrolled').addClass('scrolled');
    });
}
