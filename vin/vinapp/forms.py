from django import forms
from django.forms import TextInput
from .models import UserAnswers, Wine
import json

class UserAnswersForm(forms.ModelForm):

    class Meta:
        model = UserAnswers
        fields = ['grape', 'country', 'region', 'appellation', 'vintage']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def get_unique_values(field_name):
            all_values = Wine.objects.values_list(field_name, flat=True)
            unique_values = set()
            for value in all_values:
                if value:
                    split_values = [v.strip() for v in value.split(',')]
                    unique_values.update(split_values)
            return list(unique_values)

        self.fields['grape'].widget.attrs.update({
            'class': 'autocomplete',
            'data-choices': json.dumps(get_unique_values('grapes')),
            'placeholder': "Grape: (ie. Chardonnay)"
            })
        self.fields['country'].widget.attrs.update({
            'class': 'autocomplete',
            'data-choices': json.dumps(get_unique_values('country')),
            'placeholder': "Country: (ie. France)"
            })
        self.fields['region'].widget.attrs.update({
            'class': 'autocomplete',
            'data-choices': json.dumps(get_unique_values('region')),
            'placeholder': "Region: (ie. Burgundy)"
            })
        self.fields['appellation'].widget.attrs.update({
            'class': 'autocomplete',
            'data-choices': json.dumps(get_unique_values('appellation')),
            'placeholder': "Appellation (ie. Macon)"
            })
        self.fields['vintage'].widget.attrs.update({
            'placeholder': "Vintage (ie. 2020)"
            })

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

    scope = forms.ChoiceField(
        choices=SCOPE_CHOICES,
        widget=forms.Select(attrs={'title':
        f"A narrow scope means only the most world's most well-known styles "
        f"of wines can appear. A wide scope means anything can appear, "
        f"including rare and obscure wines."}))
    accuracy = forms.ChoiceField(
        choices=ACCURACY_CHOICES,
        widget=forms.Select(attrs={'title':
        f"Lowering accuracy allows you to simulate human imperfection. "
        f"The lower the accuracy, the more likely a tasting note will "
        f"contain errors, and these errors are more likely to be greater in "
        f"magnitude."}))