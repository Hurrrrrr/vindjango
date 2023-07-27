from django import forms
from .models import UserAnswers

class UserAnswersForm(forms.ModelForm):

    GRAPE_CHOICES = ("Chardonnay", "Chenin Blanc", "Gewurtraminer",
    "Pinot Gris/Grigio", "Riesling", "Sauvignon Blanc", "Cabernet Sauvignon",
    "Merlot,", "Pinot Noir", "Syrah/Shiraz", "Grenache-based blend",
    "Cabernet Sauvignon-based blend", "Merlot-based blend", "Nebbiolo",
    "Corvina-based blend", "Sangiovese", "Tempranillo", "Malbec",
    "Gamay", "Cabernet Franc")

    class Meta:
        model = UserAnswers
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