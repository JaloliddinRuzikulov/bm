from django.shortcuts import render, redirect, reverse
from django.http import FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, RedirectView
from .models import BodyCam, EventNameb, Eventb
from accounts.models import CustomUser, Region
from twowayradio.appm.pdfgen import pdf_printer
import datetime


# Create your views here.
class AddView(LoginRequiredMixin, TemplateView):
    template_name = 'twoway_add.html'

    def post(self, request):
        data = request.POST
        tuman, created_catalog = Region.objects.get_or_create(region_name=data['tuman'])
        for i in range(1, int(data['counts']) + 1):
            BodyCam.objects.get_or_create(model=data['model'], region=tuman, sr_code=data["field" + str(i)],
                                         came_date=datetime.date.today())
        return redirect('add_bodycam')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['regions'] = Region.objects.all()
        context['special'] = True
        return context


class ReturnView(LoginRequiredMixin, TemplateView):
    template_name = 'twoway_return.html'

    def post(self, request):
        data = request.POST
        for i in range(1, int(data['counts']) + 1):
            try:
                obj = BodyCam.objects.get(sr_code=data["field" + str(i)])
                obj.warehouse = True
                obj.save()
            except:
                continue
        return redirect('return_bodycam')


class ManageView(LoginRequiredMixin, TemplateView):
    template_name = 'twoway_manage.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['searched'] = False;
        context['section'] = 'body camera'
        if self.request.GET:
            sr_code = self.request.GET['search']
            try:
                obj = BodyCam.objects.get(sr_code=sr_code)
                context['searched'] = sr_code
                context['liables'] = obj.liable.order_by('created_date')
                context['twoway'] = obj
            except:
                context['searched'] = None;
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        data = self.request.POST
        obj = BodyCam.objects.get(sr_code=data['sr_code'])
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
            name = EventNameb.objects.get(name__icontains=self.request.GET['event'])
            event = Eventb.objects.create(name=name, opener=self.request.user)
            self.eventid = event.pk
            context = self.get_context_data()
            return redirect('/bodycam/lavent/?eviews=' + str(self.eventid))

        if 'eviews' in request.GET:
            # name = EventNameb.objects.get(name__icontains=self.request.GET['eviews'])
            event = Eventb.objects.get(pk=self.request.GET['eviews'])
            self.eventid = event.pk
            context = self.get_context_data()
            return self.render_to_response(context)

        context = dict()
        context['events'] = Eventb.objects.all()
        context['ename'] = EventNameb.objects.all()
        return render(request, 'event.html', context=context)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['twoways'] = BodyCam.objects.all().filter(event__id=self.eventid)
        data['events'] = Eventb.objects.get(pk=self.eventid)
        data['section'] = 'body camera'
        return data

    def post(self, request):
        data = request.POST
        event = Eventb.objects.get(pk=self.request.GET['eviews'])
        if not event.closed:
            for i in range(1, int(data['counts']) + 1):
                try:
                    obj = BodyCam.objects.get(sr_code=data['field' + str(i)])
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
        event = Eventb.objects.get(pk=pk)
        objects = BodyCam.objects.filter(event=event)
        count = 1
        for obj in objects:
            data.append([count, obj.number_code, obj.qr_code])
            count += 1
        directory = pdf_printer(data, id='waltalkie' + str(pk))
        return FileResponse(open(directory, 'rb'), as_attachment=False, filename='IIV_' + str(pk) + '.pdf')


class LaventCloseView(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        event = Eventb.objects.get(pk=self.kwargs['pk'])
        event.closed = True
        event.save()
        return redirect(str(reverse('lavent_bodycam') + '?eviews=' + str(event.id)))


class DataView(LoginRequiredMixin, ListView):
    model = BodyCam
    template_name = 'twoway_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        user = self.request.user
        other = CustomUser.objects.get(pk = user.pk).region.region_name
        data['section'] = 'body camera'
        if user.is_superuser:
            data['twoways'] = BodyCam.objects.all()
            data['options'] = Region.objects.all()
            data['boolrole'] = CustomUser.objects.get(pk=user.pk).region.region_name

        else:
            region = Region.objects.get(region_name=other)
            data['twoways'] = BodyCam.objects.all().filter(region=region)
            data['options'] = Region.objects.all().filter(region_name=other)
        return data
