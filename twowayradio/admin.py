from django.contrib import admin
from .models import Event, EventName, TwoWay, Region, Liable
# Register your models here.
admin.site.register(Event)
admin.site.register(EventName)
admin.site.register(TwoWay)
admin.site.register(Region)
admin.site.register(Liable)