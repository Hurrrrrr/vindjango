from django import forms
from .models import Answers

class AnswersForm(forms.ModelForm):
    class Meta:
        model = Answers
        fields = ['grape', 'country', 'region', 'appellation', 'vintage']

class MainPageForm(forms.Form):
    SCOPE_CHOICES = [
        (0, 'Narrow'),
        (1, 'Medium'),
        (2, 'Wide'),
        (3, 'Very Wide'),
    ]

    ACCURACY_CHOICES = [
        (5, 'Perfect'),
        (4, 'Very High'),
        (3, 'High'),
        (2, 'Medium'),
        (1, 'Low'),
        (0, 'Very Low'),
    ]

    scope = forms.ChoiceField(choices=SCOPE_CHOICES)
    accuracy = forms.ChoiceField(choices=ACCURACY_CHOICES)