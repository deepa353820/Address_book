from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Address(models.Model):
    label = models.CharField(max_length=200)
    latitude = models.FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)]
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)]
    )

    def __str__(self):
        return self.label
    