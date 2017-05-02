$(document).ready(function() {
    $('#get-callback').on('click', function(e){
        e.preventDefault();
        $.ajax({
            url : "/callback/",
            type : "GET",
            data : {},
            success : function(data) {
                $('#ptcb-content').append($(data));
                $('#callback-form').on('submit', function(e){
                    e.preventDefault();
                    postCallback();
                });
                $('#ptcb-overlay, #ptcb-content, #ptcb-close').show();
            }
        });
    });
    $('#ptcb-close').on('click', function(){
        $('#ptcb-content').children('form').remove();
        $('#ptcb-overlay, #ptcb-content, #ptcb-close').hide();
    });
});

function postCallback() {
    console.log('callback form submit function');
}