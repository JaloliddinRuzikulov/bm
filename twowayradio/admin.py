from django.contrib import admin
from .models import Event, EventName, TwoWay, Liable
# Register your models here.
admin.site.register(Event)
admin.site.register(EventName)
admin.site.register(TwoWay)
admin.site.register(Liable)