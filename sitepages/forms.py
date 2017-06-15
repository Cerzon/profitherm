from django.forms import Form, ModelForm, CharField, IntegerField, FloatField, inlineformset_factory
from django.core import validators
from django.core.mail import send_mail, mail_admins, mail_managers
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
    user_name = CharField(required=False)


class CalculatorTubeDiameter(Form):
    pass


class CalculatorTubeFlowVelocity(Form):
    pass


class CalculatorTubePowerLimit(Form):
    pass


CalcOrderFileUploadFormSet = inlineformset_factory(CalculationOrder, Attachment, fields=('afile',), extra=5)
QuestionFileUploadFormSet = inlineformset_factory(FrequentlyAskedQuestion, Attachment, fields=('afile',), extra=5)
