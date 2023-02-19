from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import WalkTalKie, Liable, Regions
import datetime


# Create your views here.
class AddView(LoginRequiredMixin, TemplateView):
    template_name = 'walktalkio_add.html'

    def post(self, request):
        data = request.POST
        tuman, created_catalog = Regions.objects.get_or_create(region_name=data['tuman'])
        for i in range(1, int(data['counts']) + 1):
            WalkTalKie.objects.get_or_create(model=data['model'], region=tuman, sr_code=data["field" + str(i)],
                                             came_date=datetime.date.today())
        return redirect('add_walktalkio')


class WalkTalkIOView(LoginRequiredMixin, TemplateView):
    template_name = 'walktalkio.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['searched'] = False;
        if self.request.GET:
            sr_code = self.request.GET['search']
            try:
                obj = WalkTalKie.objects.get(sr_code=sr_code)
                context['searched'] = sr_code
                context['liables'] = obj.Liable.all()
            except:
                context['searched'] = None;

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        data = self.request.POST
        obj = WalkTalKie.objects.get(sr_code=data['sr_code'])
        obj.Liable.create(full_name=data['fish'], work=data['ishi'], created_date=datetime.datetime.now())
        context = self.get_context_data(**kwargs)
        return redirect(self.request.get_full_path())
