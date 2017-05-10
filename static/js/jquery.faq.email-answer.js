$(document).ready(function(){
    $('#id_answer_email').attr('disabled', 'disabled');
    $('#id_user_email').on('keyup', function(){
        var $email = $(this).val();
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if (re.test($email)) {
            $('#id_answer_email').removeAttr('disabled');
        }
        else {
            $('#id_answer_email').prop('checked', false);
            $('#id_answer_email').attr('disabled', 'disabled');
        }
    });
});