from django import forms
from .models import UserAnswers
import json

class UserAnswersForm(forms.ModelForm):

    # replace these with dynamically generated lists
    GRAPE_CHOICES = ("Chardonnay", "Chenin Blanc", "Gewurtraminer",
    "Pinot Gris/Grigio", "Riesling", "Sauvignon Blanc", "Cabernet Sauvignon",
    "Merlot,", "Pinot Noir", "Syrah/Shiraz", "Grenache-based blend",
    "Cabernet Sauvignon-based blend", "Merlot-based blend", "Nebbiolo",
    "Corvina-based blend", "Sangiovese", "Tempranillo", "Malbec",
    "Gamay", "Cabernet Franc")

    COUNTRY_CHOICES = ("France", "Italy", "USA", "Germany",
    "Spain", "Argentina", "Australia", "New Zealand")

    REGION_CHOICES = ("Burgundy", "California", "Loire", "Alsace", "Mosel",
    "South Island", "Bordeaux", "Northern Rhone", "Southern Rhone", "Piedmont",
    "Veneto", "Tuscany", "La Rioja", "Cuyo", "South Australia")

    APPELLATION_CHOICES = ("Chablis 1er Cru", "Chassagne-Montratcher 1er Cru",
    "Napa Valley", "Vouvray", "Alsace Grand Cru", "Pinot Grigio Delle Venezie",
    "Mosel", "Sancerre", "Marlborough", "St-Julien", "Saint-Emilion",
    "Borgogne 1er Cru", "Cote-Rotie", "Chateauneuf-Du-Pape", "Barolo",
    "Amarone Della Valpolicella", "Brunello Di Montalcino Riserva",
    "Rioja Gran Reserva", "Russian River Valley", "Mendoza", "Barossa Valley",
    "Central Otago", "Borgogne")

    class Meta:
        model = UserAnswers
        fields = ['grape', 'country', 'region', 'appellation', 'vintage']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grape'].widget.attrs.update({'class': 'autocomplete',
        'data-choices': json.dumps(self.GRAPE_CHOICES)})
        self.fields['country'].widget.attrs.update({'class': 'autocomplete',
        'data-choices': json.dumps(self.COUNTRY_CHOICES)})
        self.fields['region'].widget.attrs.update({'class': 'autocomplete',
        'data-choices': json.dumps(self.REGION_CHOICES)})
        self.fields['appellation'].widget.attrs.update({'class': 'autocomplete',
        'data-choices': json.dumps(self.APPELLATION_CHOICES)})

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