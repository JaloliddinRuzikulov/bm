from django.db import models
from django.urls import reverse

from django.contrib.auth.models import AbstractUser


# Create your models here.
class Region(models.Model):
    region_name = models.CharField(max_length=255)

    def __str__(self):
        return self.region_name


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=60)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True, default=None)
