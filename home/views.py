from django.views.generic import TemplateView, CreateView


class HomePageView(TemplateView):
    template_name = 'home/home.html'


class TestPageView(TemplateView):
    template_name = 'home/test.html'


class ahmedHassan(TemplateView):
     template_name = 'home/ahmed-hassan.html'