from django.contrib import admin
from .models import Catalog, ModelProduct, Event, WalTalKie, Reason, Depot, EventName
# Register your models here.
admin.site.register(Catalog)
admin.site.register(ModelProduct)
admin.site.register(Event)
admin.site.register(WalTalKie)
admin.site.register(Reason)
admin.site.register(Depot)
admin.site.register(EventName)