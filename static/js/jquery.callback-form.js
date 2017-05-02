$(document).ready(function() {
    $('#get-callback').on('click', function(e){
        e.preventDefault();
        $.get("callback/", function(data){
            $('#ptcb-content').append($(data));
        });
        $('#ptcb-overlay, #ptcb-content, #ptcb-close').show();
    });
    $('#ptcb-close').on('click', function(){
        $('#ptcb-content').children('form').remove();
        $('#ptcb-overlay, #ptcb-content, #ptcb-close').hide();
    });
});