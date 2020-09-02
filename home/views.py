from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'home/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["zeby"] = "a7la so7ab "
        context["zebk"] = "so7aby men so5ery"
        print(context)
        return context