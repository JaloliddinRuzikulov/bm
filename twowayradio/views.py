from django.shortcuts import render, redirect, reverse
from django.http import FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, RedirectView
from .models import TwoWay, Region, Liable, EventName, Event
from twowayradio.appm.pdfgen import pdf_printer
import datetime


# Create your views here.
class AddView(LoginRequiredMixin, TemplateView):
    template_name = 'twoway_add.html'

    def post(self, request):
        data = request.POST
        tuman, created_catalog = Region.objects.get_or_create(region_name=data['tuman'])
        for i in range(1, int(data['counts']) + 1):
            TwoWay.objects.get_or_create(model=data['model'], region=tuman, sr_code=data["field" + str(i)],
                                         came_date=datetime.date.today())
        return redirect('add_twoway')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['regions'] = Region.objects.all()
        return context


class ReturnView(LoginRequiredMixin, TemplateView):
    template_name = 'twoway_return.html'

    def post(self, request):
        data = request.POST
        for i in range(1, int(data['counts']) + 1):
            try:
                obj = TwoWay.objects.get(sr_code=data["field" + str(i)])
                obj.warehouse = True
                obj.save()
            except:
                continue
        return redirect('return_twoway')


class ManageView(LoginRequiredMixin, TemplateView):
    template_name = 'twoway_manage.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['searched'] = False;
        if self.request.GET:
            sr_code = self.request.GET['search']
            try:
                obj = TwoWay.objects.get(sr_code=sr_code)
                context['searched'] = sr_code
                context['liables'] = obj.liable.order_by('created_date')
                context['twoway'] = obj
            except:
                context['searched'] = None;
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        data = self.request.POST
        obj = TwoWay.objects.get(sr_code=data['sr_code'])
        obj.liable.create(full_name=data['fish'], description=data['ishi'],
                          phone_number=data['phone_number'],
                          document_number=data['document_number'],
                          created_date=datetime.datetime.now())
        return redirect(self.request.get_full_path())


class LaventView(LoginRequiredMixin, TemplateView):
    template_name = 'twoway_lavent.html'
    eventid = int()

    def get(self, request, *args, **kwargs):
        if 'event' in request.GET:
            name = EventName.objects.get(name__icontains=self.request.GET['event'])
            event = Event.objects.create(name=name, opener=self.request.user)
            self.eventid = event.pk
            context = self.get_context_data()
            return redirect('/twoway/lavent/?eviews=' + str(self.eventid))

        if 'eviews' in request.GET:
            # name = EventName.objects.get(name__icontains=self.request.GET['eviews'])
            event = Event.objects.get(pk=self.request.GET['eviews'])
            self.eventid = event.pk
            context = self.get_context_data()
            return self.render_to_response(context)

        context = dict()
        context['events'] = Event.objects.all()
        context['ename'] = EventName.objects.all()
        return render(request, 'event.html', context=context)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['twoways'] = TwoWay.objects.all().filter(event__id=self.eventid)
        data['events'] = Event.objects.get(pk=self.eventid)
        return data

    def post(self, request):
        data = request.POST
        event = Event.objects.get(pk=self.request.GET['eviews'])
        if not event.closed:
            for i in range(1, int(data['counts']) + 1):
                try:
                    obj = TwoWay.objects.get(sr_code=data['field' + str(i)])
                    obj.event.add(event)
                    obj.warehouse = False
                    obj.save()
                except:
                    continue
        return redirect(self.request.get_full_path())


class LaventPrintView(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        data = [['T/r ', 'N_', 'Seriya nomer', 'Ism Familiya', 'Soxa xizmat', 'Tel nomer', 'Imzo', 'Qaytarildi']]
        pk = self.kwargs['pk']
        event = Event.objects.get(pk=pk)
        objects = TwoWay.objects.filter(event=event)
        count = 1
        for obj in objects:
            data.append([count, obj.number_code, obj.qr_code])
            count += 1
        directory = pdf_printer(data, id='waltalkie' + str(pk))
        return FileResponse(open(directory, 'rb'), as_attachment=False, filename='IIV_' + str(pk) + '.pdf')


class LaventCloseView(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        event = Event.objects.get(pk=self.kwargs['pk'])
        event.closed = True
        event.save()
        return redirect(str(reverse('lavent_twoway') + '?eviews=' + str(event.id)))


class DataView(LoginRequiredMixin, ListView):
    model = TwoWay
    template_name = 'twoway_list.html'
    context_object_name = 'twoways'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        cost_in = TwoWay.objects.filter(warehouse=True).count()
        cost_out = TwoWay.objects.filter(warehouse=False).count()
        data['cost_in'] = cost_in
        data['cost_out'] = cost_out
        return data
