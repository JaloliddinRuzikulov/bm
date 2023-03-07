from django.contrib import admin
from .models import Catalog, ModelProduct, Reason, Depot
# Register your models here.
admin.site.register(Catalog)
admin.site.register(ModelProduct)
admin.site.register(Reason)
admin.site.register(Depot)
