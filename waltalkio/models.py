import datetime

from django.db import models


class Regions(models.Model):
    region_name = models.CharField(max_length=255)

    def __str__(self):
        return self.region_name


class Liable(models.Model):
    full_name = models.CharField(max_length=250)
    work = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class WalkTalKie(models.Model):
    region = models.ForeignKey(Regions, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    sr_code = models.CharField(max_length=255)
    came_date = models.DateTimeField(auto_created=True)
    Liable = models.ManyToManyField(Liable, blank=True)

    class Meta:
        ordering = ['sr_code']

    def __str__(self):
        return self.sr_code
