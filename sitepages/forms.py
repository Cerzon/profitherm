from django.forms import Form, ModelForm, CharField, TimeField, inlineformset_factory
from django.core import validators
from .models import CalculationOrder, Feedback, Attachment, FrequentlyAskedQuestion

class CalculationOrderForm(ModelForm):
    user_phone = CharField(validators=[
        validators.RegexValidator(
            regex='^\+?\d?( ?\(? ?|-?)\d{3}( ?\)? ?|\-?)\d{3}( |\-)?\d{2}( |\-)?\d{2}$')])

    class Meta():
        model = CalculationOrder
        exclude = ['date_created']


class FeedbackForm(ModelForm):
    class Meta():
        model = Feedback
        fields = ['user_name', 'user_email', 'publish_email', 'title', 'content']


class FrequentlyAskedQuestionForm(ModelForm):
    class Meta():
        model = FrequentlyAskedQuestion
        fields = ['user_name', 'user_email', 'answer_email', 'question_text']


class CallbackForm(Form):
    user_phone = CharField(
        max_length=24,
        validators=[
            validators.RegexValidator(
                regex='^\+?\d?( ?\(? ?|-?)\d{3}( ?\)? ?|\-?)\d{3}( |\-)?\d{2}( |\-)?\d{2}$')])
    call_time = TimeField()

    def send_email(self):
        pass


FileUploadFormSet = inlineformset_factory(CalculationOrder, Attachment, fields=('afile',), extra=5)
