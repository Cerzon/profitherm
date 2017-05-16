$(document).ready(function(){
    var $att_forms = [];
    var $form_ready = true;
    var $fake_change = false;
    var $forms_showed = 1;
    $('.inline-form').each(function(){
        $att_forms.push($(this).hide());
    });
    $att_forms.reverse().pop().show();
    $('.clear-field').on('click', function(e){
        e.stopPropagation();
        e.preventDefault();
        $fake_change = true;
        $fieldId = $(this).data('fieldId');
        $(this).hide();
        $($fieldId + '-filename').remove();
        $($fieldId).val('').show();
        if ($form_ready && $forms_showed > 1) {
            $att_forms.push($(this).closest('.inline-form').hide());
            $forms_showed -= 1;
            if (!Modernizr.flexbox) tuneHeight();
        }
        else {
            $form_ready = true;
        }
        if (!Modernizr.flexbox) {
            $($fieldId).wrap('<form></form>').closest('form').get(0).reset();
            $($fieldId).unwrap();
        }
        $fake_change = false;
    });
    $('.inline-form').children('input[type="file"]').on('change', function(){
        if (!$fake_change) {
            $('<span id="' + this.id + '-filename">' + $(this).val().split(/[\\/]/).pop() + '</span>').insertAfter(this);
            $(this).closest('.inline-form').children('a.clear-field').show();
            $(this).hide();
            if ($att_forms.length) {
                $att_forms.pop().show();
                $forms_showed += 1;
                if (!Modernizr.flexbox) tuneHeight();
            }
            if (!$att_forms.length) $form_ready = false;
        }
    });
});