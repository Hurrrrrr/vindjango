from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

class StandardIntField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(MinValueValidator(0))
        self.validators.append(MaxValueValidator(255))

class Wine(models.Model):
    scope = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)]
    )
    style = models.CharField(max_length=50)
    label_color = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    appellation = models.CharField(max_length=50)
    grapes = models.CharField(max_length=100)
    vintage = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)]
    )
    producer = models.CharField(max_length=50, null=True, blank=True)
    bottling = models.CharField(max_length=50, null=True, blank=True)
    clarity = models.CharField(max_length=50)
    appearance_red = StandardIntField()
    appearance_green = StandardIntField()
    appearance_blue = StandardIntField()
    appearance_other = models.CharField(max_length=50, null=True, blank=True)
    condition = models.CharField(max_length=50)
    nose_intensity = StandardIntField()
    development = StandardIntField()
    petillance = StandardIntField()
    sweetness = StandardIntField()
    acidity = StandardIntField()
    alcohol = StandardIntField()
    body = StandardIntField()
    tannin_or_bitterness = StandardIntField()
    finish = StandardIntField()
    fruit_color = StandardIntField()
    fruit_family = StandardIntField()
    fruit_ripeness = StandardIntField()
    fruit_subcondition = StandardIntField()
    floral = StandardIntField()
    herbaceous = StandardIntField()
    herbal = StandardIntField()
    earth_organic = StandardIntField()
    earth_inorganic = StandardIntField()
    grape_spice = StandardIntField()
    oak_aroma = StandardIntField()
    oak_intensity = StandardIntField()
    aroma_other = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        class_name = type(self).__name__
        return f"Wine({', '.join(f'{k}={v}' for k, v in vars(self).items())})"
    
    def get_label_color(self):
        return self.label_color
    
    def get_clarity(self):
        return self.clarity
    
    # finish appearance once this program has a graphical display
    def get_appearance(self):
        return f"{self.appearance_red},{self.appearance_green},{self.appearance_blue}"

    def get_appearance_other(self):
        return self.appearance_other
    
    def get_condition(self):
        return self.condition
    
    def get_nose_intensity(self):
        return self.nose_intensity
    
    def get_development(self):
        return self.nose_intensity

    def get_petillance(self):
        return self.petillance

    def get_sweetness(self):
        return self.sweetness

    def get_acidity(self):
        return self.acidity

    def get_alcohol(self):
        return self.alcohol

    def get_body(self):
        return self.body

    def get_tannin_or_bitterness(self):
        return self.tannin_or_bitterness

    def get_finish(self):
        return self.finish
    
    def get_fruit_color(self):
        return self.fruit_color

    def get_fruit_family(self):
        return self.fruit_family

    def get_fruit_ripeness(self):
        return self.fruit_ripeness

    def get_fruit_subcondition(self):
        return self.fruit_subcondition

    def get_floral(self):
        return self.floral

    def get_herbaceous(self):
        return self.herbaceous

    def get_herbal(self):
        return self.herbal

    def get_earth_organic(self):
        return self.earth_organic

    def get_earth_inorganic(self):
        return self.earth_inorganic

    def get_grape_spice(self):
        return self.grape_spice

    def get_oak_aroma(self):
        return self.oak_aroma
    
    def get_oak_intensity(self):
        return self.oak_intensity
    
    def get_aroma_other(self):
        return self.aroma_other
    
    # repeating myself for encapsulation
    def get_primary_country(self):
        return self.country.split(",")[0]

    def get_primary_grape(self):
        return self.grapes.split(",")[0]

    def get_primary_region(self):
        return self.region.split(",")[0]
    
    def get_primary_appellation(self):
        return self.appellation.split(",")[0]
    
    def get_secondary_grapes(self):
        split_grapes = self.grapes.split(",")
        if len(split_grapes) <= 1:
            return False
        else:
            return split_grapes[1:]

class Answers(models.Model):
    grape = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    appellation = models.CharField(max_length=100)
    vintage = models.IntegerField()