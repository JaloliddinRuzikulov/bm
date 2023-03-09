from django.db import models
from django.shortcuts import reverse
from django.conf import settings

# Create your models here.
class Appeal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    theme = models.CharField(max_length=250)
    text = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, null=True, blank=True)
    open_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.theme + " " + self.user.last_name

    def get_absolute_url(self):
        return reverse('appeals_list')
