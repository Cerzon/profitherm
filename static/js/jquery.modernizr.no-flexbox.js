$(document).ready(function(){
    if (!Modernizr.flexbox) {
        tuneHeight();
        $('mdrnz-no-flexbox').on('resize', tuneHeight);
    }
});

function tuneHeight() {
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