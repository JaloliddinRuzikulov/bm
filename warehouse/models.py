from django.db import models
from django.urls import reverse
from accounts.models import CustomUser


# Create your models here.
class Catalog(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class ModelProduct(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


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


class WalTalKie(models.Model):
    event = models.ManyToManyField(Event, blank=True)
    model_product = models.ForeignKey(ModelProduct, on_delete=models.CASCADE)
    number_code = models.SmallIntegerField(default=0)
    qr_code = models.CharField(max_length=200)
    warehouse = models.BooleanField(default=True)

    def __str__(self):
        return self.qr_code


class Reason(models.Model):
    reason = models.CharField(max_length=100)
    opener = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rea_date = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.reason

    def get_absolute_url(self):
        return reverse('reason', args=[str(self.id)])


class Depot(models.Model):
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE, null=True, blank=True)
    model = models.ForeignKey(ModelProduct, on_delete=models.CASCADE, blank=False)
    qr_code = models.CharField(max_length=250)
    came_date = models.DateTimeField(auto_created=True)
    came_out_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.qr_code

    def get_absolute_url(self):
        return reverse('depot', args=[str(self.pk)])
