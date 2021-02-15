from django.urls import path
from home.views import HomePageView, TestPageView
from home.views import ahmedHassan

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('test/', TestPageView.as_view(), name="test"),
    path('ahmed-hassan', ahmedHassan.as_view(), name='ahmed_hassan'),

]
