$(document).ready(function() {
    $('#get-callback').on('click', function(){
        $('body').append($('<div id="ptcb-overlay"><div id="ptcb-content"><div id="ptcb-close"></div></div></div>'));
        $.get("callback/", function(data){
            $('#ptcb-content').append($(data));
        });
    });
    $('#ptcb-close').on('click', function(){
        $('#ptcb-overlay').remove();
    });
});