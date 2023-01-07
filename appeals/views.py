from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Appeal


# Create your views here.


class AppealsNew(LoginRequiredMixin, CreateView):
    model = Appeal
    template_name = 'appeals/add.html'
    fields = ['theme', 'text', 'user']


class AppealsDone(LoginRequiredMixin, ListView):
    model = Appeal
    template_name = 'appeals/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['appeals'] = Appeal.objects.filter(status=True)
        return data


class AppealsMy(LoginRequiredMixin, ListView):
    model = Appeal
    template_name = 'appeals/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['appeals'] = Appeal.objects.filter(user=self.request.user)
        return data


class AppealsNotDone(LoginRequiredMixin, ListView):
    model = Appeal
    template_name = 'appeals/list.html'
    context_object_name = 'appeals'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['appeals'] = Appeal.objects.filter(status=False)
        return data


class AppealsArchive(LoginRequiredMixin, TemplateView):
    template_name = 'appeals/archive.html'


class AppealsDetail(LoginRequiredMixin, DetailView):
    model = Appeal
    template_name = 'appeals/detail.html'

    def post(self, *args, **kwargs):
        description = self.request.POST['description']
        Appeal.objects.filter(pk=kwargs['pk']).update(status=None, description = description)
        return redirect('appeals_notdone')

class AppealsChangeDone(LoginRequiredMixin, UpdateView):
    model = Appeal

    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        Appeal.objects.filter(pk=pk).update(status=True)
        return redirect('appeals_detail', pk=pk)


class AppealsIgnore(LoginRequiredMixin, ListView):
    model = Appeal
    template_name = 'appeals/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['appeals'] = Appeal.objects.filter(status=None)
        return data
