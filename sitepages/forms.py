from django.forms import ModelForm, inlineformset_factory
from .models import CalculationOrder, Feedback, Attachment, FrequentlyAskedQuestion

class CalculationOrderForm(ModelForm):
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


FileUploadFormSet = inlineformset_factory(CalculationOrder, Attachment, fields=('afile',), extra=5)
