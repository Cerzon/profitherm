$(document).ready(function(){
    if (!Modernizr.flexbox) {
        tuneHeight();
        $(window).on('resize', tuneHeight);
    }
});

$(document).load(function(){
    if (!Modernizr.flexbox) {
        tuneHeight();
    }
});

function tuneHeight() {
    $('#leftsidebar').innerHeight('auto');
    $('#rightsidebar').innerHeight('auto');
    $('main').innerHeight('auto');
    var $maxheight = $('#rightsidebar').innerHeight();
    var $nextone = $('main').innerHeight();
    if ($nextone > $maxheight) {
        $maxheight = $nextone;
    }
    if ($(window).width() > 1243) {
        $nextone = $('#leftsidebar').innerHeight();
        if ($nextone > $maxheight) {
            $maxheight = $nextone;
        }
        $('#leftsidebar').innerHeight($maxheight);
    }
    else {
        $('#leftsidebar').innerHeight('auto');
    }
    $('#rightsidebar').innerHeight($maxheight);
    $('main').innerHeight($maxheight);
}