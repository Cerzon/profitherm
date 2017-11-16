from django.forms import Form, ModelForm, CharField, IntegerField, EmailField, Textarea, inlineformset_factory
from django.core import validators
from django.core.mail import send_mail, mail_admins, mail_managers
from .models import CalculationOrder, Feedback, Attachment, FrequentlyAskedQuestion, WaterTreatmentRequest

class CalculationOrderForm(ModelForm):
    user_phone = CharField(validators=[
        validators.RegexValidator(
            regex='^\+?\d?( ?\(? ?|-?)\d{3}( ?\)? ?|\-?)\d{3}( |\-)?\d{2}( |\-)?\d{2}$')])

    class Meta():
        model = CalculationOrder
        exclude = ['date_created']


class WaterTreatmentRequestForm(ModelForm):
    user_phone = CharField(required=False, validators=[
        validators.RegexValidator(
            regex='^\+?\d?( ?\(? ?|-?)\d{3}( ?\)? ?|\-?)\d{3}( |\-)?\d{2}( |\-)?\d{2}$')])

    class Meta():
        model = WaterTreatmentRequest
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
    user_name = CharField(required=False)


class QuickRequestForm(Form):
    heated_area = IntegerField()
    bathroom_amount = IntegerField(required=False)
    additional_info = CharField(widget=Textarea, required=False)
    user_email = EmailField()


CalcOrderFileUploadFormSet = inlineformset_factory(CalculationOrder, Attachment, fields=('afile',), extra=5)
QuestionFileUploadFormSet = inlineformset_factory(FrequentlyAskedQuestion, Attachment, fields=('afile',), extra=5)
WaterAnalysisFileUploadFormSet = inlineformset_factory(WaterTreatmentRequest, Attachment, fields=('afile',), extra=5)
