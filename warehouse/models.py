from django.db import models
from django.urls import reverse
from django.conf import settings

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


class Reason(models.Model):
    reason = models.CharField(max_length=100)
    opener = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
