from .models import Class, Week
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from .forms import ClassForm, WeekForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponseRedirect


class ClassListView(ListView):
    model = Class
    template_name = "classes/class-list.html"

class ClassCreateView(CreateView):
    template_name = "classes/create-class.html"
    form_class = ClassForm
    success_url = reverse_lazy('create_class')

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     print(form.instance.end)
    #     # form.instance.user = self.request.user
    #     self.object.save()
    #     return HttpResponseRedirect(self.get_success_url())

    # def form_invalid(self, form):
    #     return self.render_to_response(self.get_context_data(form=form))


class ClassUpdateView(UpdateView):
    model = Class
    template_name = "classes/update-class.html"
    form_class = ClassForm
    success_url = reverse_lazy('class_list')

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["object_id"] = self.object.id
        return ctx

class ClassDeleteView(DeleteView):
    model = Class
    success_url = reverse_lazy('class_list')




class WeekCreateView(CreateView):
    model = Week
    template_name = 'classes/week-new.html'
    fields = ['name', 'start', 'end']
    success_url = reverse_lazy('week_list')

class WeekListView(ListView):
    model = Week
    template_name = "classes/week-list.html"

class WeekUpdateView(UpdateView):
    model = Week
    template_name = "classes/week-update.html"
    form_class = WeekForm
    success_url = reverse_lazy('week_list')

class WeekDeleteView(DeleteView):
    model = Week
    success_url = reverse_lazy('week_list')