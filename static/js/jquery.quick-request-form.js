$(document).ready(function(){
    $('#quick-request').find('.loader-spinner').show();
    $.ajax({
        url : "/forms/quick-request/",
        type : "GET",
        data : {},
        success : showQuickRequest
    });
});

function showQuickRequest(data) {
    $('#quick-request-form').remove();
    $('#quick-request').append($(data));
    $('#quick-request').find('.loader-spinner').hide();
    $('#quick-request-form').on('submit', function(event){
        event.preventDefault();
        $('#quick-request-form').hide();
        $('#quick-request').find('.loader-spinner').show();
        $.ajax({
            url : "/forms/quick-request/",
            type : "POST",
            data : $('#quick-request-form').serialize(),
            success : showQuickRequest
        });
    });
    if (!Modernizr.flexbox) tuneHeight();
}