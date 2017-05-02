$(document).ready(function() {
    $('#get-callback').on('click', function(e){
        e.preventDefault();
        $('#ptcb-overlay, #ptcb-window, #ptcb-content, #ptcb-loader, #ptcb-close').show();
        $.ajax({
            url : "/callback/",
            type : "GET",
            data : {},
            success : displayResponse
        });
    });
    $('#ptcb-close').on('click', function(){
        $('#ptcb-content').children().remove();
        $('#ptcb-overlay, #ptcb-window, #ptcb-content, #ptcb-loader, #ptcb-close').hide();
    });
});

function displayResponse(data) {
    $('#ptcb-content').children().remove();
    $('#ptcb-loader').hide();
    $('#ptcb-content').append($(data));
    $('#callback-form').on('submit', function(e){
        e.preventDefault();
        postCallback();
    });
}

function postCallback() {
    $('#callback-form').hide();
    $('#ptcb-loader').show();
    $.ajax({
        url : "/callback/",
        type : "POST",
        data : $('#callback-form').serialize(),
        success : displayResponse
    });
}