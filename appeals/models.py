from django.db import models
from django.shortcuts import reverse
from accounts.models import CustomUser


# Create your models here.
class Appeal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    theme = models.CharField(max_length=250)
    text = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, null=True, blank=True)
    open_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.theme + " " + self.user.last_name

    def get_absolute_url(self):
        return reverse('appeals_list')
