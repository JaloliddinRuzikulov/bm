import datetime
from django.db import models
from django.urls import reverse
from django.conf import settings
from accounts.models import Region


class EventNamet(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Eventt(models.Model):
    name = models.ForeignKey(EventNamet, on_delete=models.CASCADE, null=True, blank=True, default=None)
    opener = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.name.name

    def get_absolute_url(self):
        return reverse('events', args=[str(self.id)])

    def get_count(self):
        return Tablet.objects.filter(event__id=self.id).count()

class Liable(models.Model):
    full_name = models.CharField(max_length=250)
    description = models.CharField(max_length=250, blank=True)
    phone_number = models.CharField(max_length=60, blank=True)
    document_number = models.CharField(max_length=250, blank=True)
    created_date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name

    def get_qrcode(self):
        return (Tablet.objects.all().filter(liable__id=self.id)).first()

class Tablet(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    sr_code = models.CharField(max_length=255)
    number_code = models.CharField(max_length=250, blank=True, null=True)
    came_date = models.DateTimeField(auto_now_add=True)
    warehouse = models.BooleanField(default=True)
    liable = models.ManyToManyField(Liable, blank=True)
    event = models.ManyToManyField(Eventt, blank=True)

    class Meta:
        ordering = ['sr_code']

    def __str__(self):
        return self.sr_code
