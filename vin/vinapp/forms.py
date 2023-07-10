from django import forms
from .models import Answers

class AnswersForm(forms.ModelForm):
    class Meta:
        model = Answers
        fields = ['grape', 'country', 'region', 'appellation', 'vintage']

class TastingNoteForm(forms.Form):
    SCOPE_CHOICES = [
        ('0', 'Narrow'),
        ('1', 'Medium'),
        ('2', 'Wide'),
        ('3', 'Very Wide'),
    ]

    ACCURACY_CHOICES = [
        ('0', 'Very Low'),
        ('1', 'Low'),
        ('2', 'Medium'),
        ('3', 'High'),
        ('4', 'Very High'),
        ('5', 'Perfect'),
    ]

    scope = forms.ChoiceField(choices=SCOPE_CHOICES)
    accuracy = forms.ChoiceField(choices=ACCURACY_CHOICES)