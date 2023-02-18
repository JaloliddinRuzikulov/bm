from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from warehouse.models import Catalog, ModelProduct, Depot
import datetime


# Create your views here.
class AddView(LoginRequiredMixin, TemplateView):
    template_name = 'depot.html'

    def post(self, request):
        data = request.POST
        catalog, created_catalog = Catalog.objects.get_or_create(name=data['katalog'])
        model, created_model = ModelProduct.objects.get_or_create(catalog=catalog, name=data['model'])
        for i in range(1, int(data['counts']) + 1):
            Depot.objects.get_or_create(model=model, qr_code=data["field" + str(i)], came_date=datetime.date.today())
        return redirect('add_depot')
