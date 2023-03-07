from django.db import models

# Create your models here.
class Region(models.Model):
    region = models.CharField(max_length=250)

    def __str__(self):
        return self.region


class   