import datetime
from django.http import FileResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, ListView, RedirectView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from twowayradio.appm.pdfgen import pdf_printer
from .models import Depot, Catalog, ModelProduct, Reason
from twowayradio.models import TwoWay
from tablet.models import Tablet
from bodycam.models import BodyCam
from appeals.models import Appeal
from django.db.models import Count
# Create your views here.    
class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["warehouse"] = Depot.objects.all().count()
        context["twoway"] = TwoWay.objects.all().count() 
        context["tablet"] = Tablet.objects.all().count() 
        context["bodycam"] = BodyCam.objects.all().count() 

        months_notdone = list()
        months_done = list()
        months_rejects = list()
        year = datetime.datetime.now().year
        for month in range(1, 13):        
            start_date = datetime.datetime(year, month, 1)
            end_date = datetime.datetime(year, month+1, 1) if month != 12 else datetime.datetime(year+1, 1, 1)
            months_done.append(Appeal.objects.filter(open_date__gte=start_date, open_date__lte=end_date, status=True).aggregate(Count('id'))['id__count'])
            months_notdone.append(Appeal.objects.filter(open_date__gte=start_date, open_date__lte=end_date, status=False).aggregate(Count('id'))['id__count'])
            months_rejects.append(Appeal.objects.filter(open_date__gte=start_date, open_date__lte=end_date, status=None).aggregate(Count('id'))['id__count'])
        context['status_notdone'] = str(months_notdone)
        context['status_rejects'] = str(months_rejects)
        context['status_done'] = str(months_done)
        context['list_done'] = Appeal.objects.filter(status=True).order_by('-open_date')[:5]
        context['list_notdone'] = Appeal.objects.filter(status=False).order_by('-open_date')[:5]
        context['list_rejects'] = Appeal.objects.filter(status=None).order_by('-open_date')[:5]
        twoway_labels = list()
        twoway_data = list()
        for twoway in TwoWay.objects.all():
            twoway_labels.append(twoway.region.region_name)
        for twoway in twoway_labels:    
            twoway_data.append(TwoWay.objects.filter(region__region_name__exact=twoway).count())        
        context['twoway_labels'] = str(list(set(twoway_labels)))
        context['twoway_data'] = str(list(set(twoway_data)))
        tablet_labels = list()
        tablet_data = list()
        for tablet in Tablet.objects.all():
            tablet_labels.append(tablet.region.region_name)
        for tablet in tablet_labels:    
            tablet_data.append(Tablet.objects.filter(region__region_name__exact=tablet).count())
        context['tablet_labels'] = str(list(set(tablet_labels)))
        context['tablet_data'] = str(list(set(tablet_data)))
        bodycam_labels = list()
        bodycam_data = list()
        for bodycam in BodyCam.objects.all():
            bodycam_labels.append(bodycam.region.region_name)
        for bodycam in bodycam_labels:    
            bodycam_data.append(BodyCam.objects.filter(region__region_name__exact=bodycam).count())
        context['bodycam_labels'] = str(list(set(bodycam_labels)))
        context['bodycam_data'] = str(list(set(bodycam_data)))
        groups =self.request.user.groups.all()

        if 'murojaatchi' in groups:
            return redirect('appeals_list')
        else:
            return render(request, self.template_name, context= context)

class ListDepot(LoginRequiredMixin, ListView):
    model = Depot
    template_name = 'listdepot.html'
    context_object_name = 'depots'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['depots'] = Depot.objects.all().filter(reason=None)
        return data


class OutDepot(LoginRequiredMixin, TemplateView):
    template_name = 'outdepot.html'
    reasonid = int()

    def get(self, request, *args, **kwargs):
        if 'reason' in request.GET:
            reason, created = Reason.objects.get_or_create(reason=self.request.GET['reason'], opener=self.request.user)
            self.reasonid = reason.pk
            context = self.get_context_data()
            return self.render_to_response(context)
        context = dict()
        context['reasons'] = Reason.objects.all()
        return render(request, 'reasons.html', context=context)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['depots'] = Depot.objects.all().filter(reason=self.reasonid)
        data['reasons'] = Reason.objects.get(pk=self.reasonid)
        return data

    def post(self, request):
        data = request.POST
        reason, created = Reason.objects.get_or_create(reason=self.request.GET['reason'], opener=self.request.user)
        if not reason.closed:
            for i in range(1, int(data['counts']) + 1):
                Depot.objects.filter(qr_code=data['field' + str(i)]).update(reason=reason)
        return redirect(self.request.get_full_path())


class AddDepot(LoginRequiredMixin, TemplateView):
    template_name = 'depot.html'

    def post(self, request):
        data = request.POST
        catalog, created_catalog = Catalog.objects.get_or_create(name=data['katalog'])
        model, created_model = ModelProduct.objects.get_or_create(catalog=catalog, name=data['model'])
        for i in range(1, int(data['counts']) + 1):
            Depot.objects.get_or_create(model=model, qr_code=data["field" + str(i)], came_date=datetime.date.today())
        return redirect('add_depot')


class OutDepotClose(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        reason = Reason.objects.get(pk=self.kwargs['pk'])
        reason.closed = True
        reason.save()
        return redirect(str(reverse('out_depot') + '?reason=' + str(reason.reason)))


class OutDepotPrint(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        data = [['T/r ', 'Katalog', 'Model', 'QR Code']]
        pk = self.kwargs['pk']
        objects = Depot.objects.filter(reason_id=pk)
        count = 1
        for obj in objects:
            data.append([count, obj.model.catalog, obj.model, obj.qr_code])
            count += 1
        directory = pdf_printer(data, id='depot' + str(pk))
        return FileResponse(open(directory, 'rb'), as_attachment=False, filename='IIV_' + str(pk) + '.pdf')

