from .models import Class, Week
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from .forms import ClassForm, WeekForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from home.permissions import AdminPermission


class ClassListView(AdminPermission, ListView):
    model = Class
    template_name = "classes/class-list.html"


class ClassCreateView(AdminPermission, CreateView):
    template_name = "classes/create-class.html"
    form_class = ClassForm
    success_url = reverse_lazy('class_list')


class ClassUpdateView(AdminPermission, UpdateView):
    model = Class
    template_name = "classes/update-class.html"
    form_class = ClassForm
    success_url = reverse_lazy('class_list')

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["object_id"] = self.object.id
        return ctx


class ClassDeleteView(AdminPermission, DeleteView):
    model = Class
    success_url = reverse_lazy('class_list')


class WeekCreateView(AdminPermission, CreateView):
    model = Week
    template_name = 'classes/week-new.html'
    fields = ['name', 'start', 'end']
    success_url = reverse_lazy('week_list')


class WeekListView(AdminPermission, ListView):
    model = Week
    template_name = "classes/week-list.html"


class WeekUpdateView(AdminPermission, UpdateView):
    model = Week
    template_name = "classes/week-update.html"
    fields = ['name', 'start', 'end']
    success_url = reverse_lazy('week_list')


class WeekDeleteView(AdminPermission, DeleteView):
    model = Week
    success_url = reverse_lazy('week_list')
