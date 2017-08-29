$(document).ready(function(){
    $('#quick-compute-request').find('.loader-spinner').show();
    $.ajax({
        url : "/forms/quick-compute/",
        type : "GET",
        data : {},
        success : showCompute
    });
});

function showCompute(data) {
    $('#quick-compute-request').find('form').remove();
    $('#quick-compute-request').append($(data));
    $('#quick-compute-request').find('.loader-spinner').hide();
}