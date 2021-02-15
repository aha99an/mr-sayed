from django.views.generic import TemplateView, CreateView
from datetime import datetime

class HomePageView(TemplateView):
    template_name = 'home/home.html'


class TestPageView(TemplateView):
    template_name = 'home/test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = datetime.now().time()
        return context

class ahmedHassan(TemplateView):
    template_name = 'home/ahmed-hassan.html'
