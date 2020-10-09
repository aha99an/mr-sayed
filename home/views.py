from django.views.generic import TemplateView, CreateView


class HomePageView(TemplateView):
    template_name = 'home/home.html'

class TestView(CreateView):
    template_name = "test/elements.html"
