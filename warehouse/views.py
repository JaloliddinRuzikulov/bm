import datetime
from django.http import FileResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, ListView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from twowayradio.appm.pdfgen import pdf_printer
from .models import Depot, Catalog, ModelProduct, Reason


# Create your views here.


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        groups =self.request.user.groups.all()
        if 'murojaatchi' in groups:
            return redirect('appeals_list')
        else:
            return render(request, self.template_name)

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

