import datetime
from django.db import models
from accounts.models import CustomUser
from django.urls import reverse


class EventName(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.ForeignKey(EventName, on_delete=models.CASCADE, null=True, blank=True, default=None)
    opener = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.name.name

    def get_absolute_url(self):
        return reverse('events', args=[str(self.id)])


class Region(models.Model):
    region_name = models.CharField(max_length=255)

    def __str__(self):
        return self.region_name


class Liable(models.Model):
    full_name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class TwoWay(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    sr_code = models.CharField(max_length=255)
    came_date = models.DateTimeField(auto_created=True)
    warehouse = models.BooleanField(default=True)
    liable = models.ManyToManyField(Liable, blank=True)
    event = models.ManyToManyField(Event, blank=True)

    class Meta:
        ordering = ['sr_code']

    def __str__(self):
        return self.sr_code
