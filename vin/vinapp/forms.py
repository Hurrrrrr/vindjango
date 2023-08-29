from django import forms
from django.forms import TextInput
from .models import UserAnswers
import json

class UserAnswersForm(forms.ModelForm):

    # replace these with dynamically generated lists
    GRAPE_CHOICES = ("Chardonnay", "Chenin Blanc", "Gewurtraminer",
    "Pinot Gris/Grigio", "Riesling", "Sauvignon Blanc", "Cabernet Sauvignon",
    "Merlot,", "Pinot Noir", "Syrah/Shiraz", "Grenache-based blend",
    "Cabernet Sauvignon-based blend", "Merlot-based blend", "Nebbiolo",
    "Corvina-based blend", "Sangiovese", "Tempranillo", "Malbec",
    "Gamay", "Cabernet Franc", "Viognier", "Mourverde")

    COUNTRY_CHOICES = ("France", "Italy", "USA", "Germany",
    "Spain", "Argentina", "Australia", "New Zealand")

    REGION_CHOICES = ("Burgundy", "California", "Loire", "Alsace", "Mosel",
    "South Island", "Bordeaux", "Northern Rhone", "Southern Rhone", "Piedmont",
    "Veneto", "Tuscany", "La Rioja", "Cuyo", "South Australia")

    APPELLATION_CHOICES = ("Chablis 1er Cru", "Chassagne-Montratcher 1er Cru",
    "Napa Valley", "Vouvray", "Alsace Grand Cru", "Pinot Grigio Delle Venezie",
    "Mosel", "Sancerre", "Marlborough", "St-Julien", "Saint-Emilion",
    "Bourgogne 1er Cru", "Cote-Rotie", "Chateauneuf-Du-Pape", "Barolo",
    "Amarone Della Valpolicella", "Brunello Di Montalcino Riserva",
    "Rioja Gran Reserva", "Russian River Valley", "Mendoza", "Barossa Valley",
    "Central Otago", "Bourgogne", "Chianti Classico Riserva")

    class Meta:
        model = UserAnswers
        fields = ['grape', 'country', 'region', 'appellation', 'vintage']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grape'].widget.attrs.update({
            'class': 'autocomplete',
            'data-choices': json.dumps(self.GRAPE_CHOICES),
            'placeholder': "Grape: (ie. Chardonnay)"
            })
        self.fields['country'].widget.attrs.update({
            'class': 'autocomplete',
            'data-choices': json.dumps(self.COUNTRY_CHOICES),
            'placeholder': "Country: (ie. France)"
            })
        self.fields['region'].widget.attrs.update({
            'class': 'autocomplete',
            'data-choices': json.dumps(self.REGION_CHOICES),
            'placeholder': "Region: (ie. Burgundy)"
            })
        self.fields['appellation'].widget.attrs.update({
            'class': 'autocomplete',
            'data-choices': json.dumps(self.APPELLATION_CHOICES),
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