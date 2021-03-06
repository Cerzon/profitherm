$(document).ready(function() {
    $('#get-callback').on('click', function(event){
        event.preventDefault();
        $('#ptcb-overlay, #ptcb-window, #ptcb-loader, #ptcb-close').show();
        $.ajax({
            url : "/callback/",
            type : "GET",
            data : {},
            success : displayResponse
        });
    });
    $('#ptcb-close').on('click', function(){
        $('#ptcb-content').empty();
        $('#ptcb-overlay, #ptcb-window, #ptcb-content, #ptcb-loader, #ptcb-close').hide();
    });
});

function displayResponse(data) {
    $('#ptcb-content').children().remove();
    $('#ptcb-content').append($(data));
    $('#ptcb-loader').hide();
    $('#ptcb-content').show();
    $('#callback-form').on('submit', function(event){
        event.preventDefault();
        postCallback();
    });
}

function postCallback() {
    $('#ptcb-content').hide();
    $('#ptcb-loader').show();
    $.ajax({
        url : "/callback/",
        type : "POST",
        data : $('#callback-form').serialize(),
        success : displayResponse
    });
}