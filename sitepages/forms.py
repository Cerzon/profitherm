from django import forms
from .models import CalculationOrder, Feedback

class CalculationOrderForm(forms.ModelForm):
    class Meta():
        model = CalculationOrder
        exclude = ['date_created']


class FeedbackForm(forms.ModelForm):
    class Meta():
        model = Feedback
        fields = ['user_name', 'user_email', 'title', 'content']
    