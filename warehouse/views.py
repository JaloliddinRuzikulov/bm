import datetime
from django.http import FileResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, ListView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from .appm.pdfgen import pdf_printer
from .models import Depot, Catalog, ModelProduct, WalTalKie, Reason, Event, EventName


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


class ListWalTalKie(LoginRequiredMixin, ListView):
    model = WalTalKie
    template_name = 'listwaltalkie.html'
    context_object_name = 'waltalkies'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        cost_in = WalTalKie.objects.filter(warehouse=True).count()
        cost_out = WalTalKie.objects.filter(warehouse=False).count()
        data['bazada'] = cost_in
        data['tadbirda'] = cost_out
        return data


class WalTalKieView(LoginRequiredMixin, TemplateView):
    template_name = 'waltalkie.html'
    eventid = int()

    def get(self, request, *args, **kwargs):
        if 'event' in request.GET:
            name = EventName.objects.get(name__icontains=self.request.GET['event'])
            event = Event.objects.create(name=name, opener=self.request.user)
            self.eventid = event.pk
            context = self.get_context_data()
            return redirect('/waltalkie/out/?eviews=' + str(self.eventid))

        if 'eviews' in request.GET:
            # name = EventName.objects.get(name__icontains=self.request.GET['eviews'])
            event = Event.objects.get(pk=self.request.GET['eviews'])
            self.eventid = event.pk
            context = self.get_context_data()
            return self.render_to_response(context)

        context = dict()
        context['events'] =Event.objects.all()
        context['ename'] = EventName.objects.all()
        return render(request, 'event.html', context=context)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['waltalkies'] = WalTalKie.objects.all().filter(event__id=self.eventid)
        data['events'] = Event.objects.get(pk=self.eventid)
        return data

    def post(self, request):
        data = request.POST
        event = Event.objects.get(pk=self.request.GET['eviews'])
        if not event.closed:
            for i in range(1, int(data['counts']) + 1):
                try:
                    obj = WalTalKie.objects.get(qr_code=data['field' + str(i)])
                    obj.event.add(event)
                    obj.warehouse = False
                    obj.save()
                except:
                    continue
        return redirect(self.request.get_full_path())


class AddWalTalKie(LoginRequiredMixin, TemplateView):
    template_name = 'addwaltalkie.html'

    def post(self, request):
        data = request.POST
        catalog, created_catalog = Catalog.objects.get_or_create(name='Ratsiya')
        model, created_model = ModelProduct.objects.get_or_create(catalog=catalog, name=data['model'])
        for i in range(1, int(data['counts']) + 1):
            WalTalKie.objects.get_or_create(model_product=model, qr_code=data["field" + str(i)],
                                            number_code=data["number_code" + str(i)], )
        return redirect('add_waltalkie')


class InWalTalKie(LoginRequiredMixin, TemplateView):
    template_name = 'inwaltalkie.html'

    def post(self, request):
        data = request.POST
        for i in range(1, int(data['counts']) + 1):
            try:
                obj = WalTalKie.objects.get(qr_code__contains=data["field" + str(i)])
                obj.warehouse = True
                obj.save()
            except:
                continue
        return redirect('in_waltalkie')


class WalTalKieClose(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        event = Event.objects.get(pk=self.kwargs['pk'])
        event.closed = True
        event.save()
        return redirect(str(reverse('out_waltalkie') + '?eviews=' + str(event.id)))


class WalTalKiePrint(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        data = [['T/r ', 'N_', 'Seriya nomer', 'Ism Familiya', 'Soxa xizmat', 'Tel nomer', 'Imzo', 'Qaytarildi']]
        pk = self.kwargs['pk']
        event = Event.objects.get(pk=pk)
        objects = WalTalKie.objects.filter(event=event)
        count = 1
        for obj in objects:
            data.append([count, obj.number_code, obj.qr_code])
            count += 1
        directory = pdf_printer(data, id='waltalkie' + str(pk))
        return FileResponse(open(directory, 'rb'), as_attachment=False, filename='IIV_' + str(pk) + '.pdf')


class OutWalTalKie(LoginRequiredMixin, TemplateView):
    template_name = 'addwaltalkie.html'

    def post(self, request):
        data = request.POST
        catalog, created_catalog = Catalog.objects.get_or_create(name=data['katalog'])
        model, created_model = ModelProduct.objects.get_or_create(catalog=catalog, name=data['model'])
        for i in range(1, int(data['counts']) + 1):
            WalTalKie.objects.get_or_create(model_product=model, qr_code=data["field" + str(i)],
                                            number_code=data["number_code" + str(i)], )
        return redirect('add_waltalkie')
