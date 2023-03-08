from django.db import models
from django.urls import reverse

from django.contrib.auth.models import AbstractUser
from twowayradio.models import Region
# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=60)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
