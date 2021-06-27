from django.urls import path
from home.views import HomePageView, TestPageView
from home.views import ahmedHassan

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('.well-known/acme-challenge/V9PvGlFDugxa4JrhHqf4Jrmk6ZJ1KOPwfl7VMuZNNUk/', TestPageView.as_view(), name="test"),
    path('ahmed-hassan', ahmedHassan.as_view(), name='ahmed_hassan'),

]
