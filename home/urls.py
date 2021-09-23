from django.urls import path
from home.views import HomePageView, TestPageView
from home.views import ahmedHassan

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('.well-known/acme-challenge/pA_0B3Uj9jTNr_Z3fu4_9103qob8fUF--OZSamNeWB4/', TestPageView.as_view(), name="test"),
    path('ahmed-hassan', ahmedHassan.as_view(), name='ahmed_hassan'),

]
