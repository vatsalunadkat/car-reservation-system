from django.db import models
from user_register.models import User
from vehicle_register.models import Vehicle

# Create your models here.


class Booking(models.Model):
    booking_datetime = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    booking_status = models.CharField(max_length=255)

    REQUIRED_FIELDS = []
