from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_id = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=225)
    mobile = models.CharField(max_length = 13)
    # username is required by AbstractUser, but we can override it.
    username = None

    USERNAME_FIELD = 'email_id'
    REQUIRED_FIELDS = []