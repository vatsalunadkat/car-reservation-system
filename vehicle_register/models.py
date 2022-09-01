from django.db import models

# Create your models here.


class Vehicle(models.Model):
    name = models.CharField(max_length=255)
    vehicle_model = models.CharField(max_length=255)
    licence_number = models.CharField(max_length=50, unique=True)
    available = models.BooleanField(default=True)

    REQUIRED_FIELDS = []
