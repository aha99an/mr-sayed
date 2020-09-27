from .models import Class, Week
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from .forms import ClassForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from home.permissions import StudentPermission


class ClassListView(StudentPermission, ListView):
    model = Class
    template_name = "classes/class-list.html"


class WeekListView(StudentPermission, ListView):
    model = Week
    template_name = "classes/class-list.html"


class ClassCreateView(StudentPermission, CreateView):
    template_name = "classes/create-class.html"
    form_class = ClassForm
    success_url = reverse_lazy('create_class')


class ClassUpdateView(StudentPermission, UpdateView):
    model = Class
    template_name = "classes/update-class.html"
    form_class = ClassForm
    success_url = reverse_lazy('class_list')

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["object_id"] = self.object.id
        return ctx


class ClassDeleteView(StudentPermission, DeleteView):
    model = Class
    success_url = reverse_lazy('class_list')
