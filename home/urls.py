from django.urls import path
from home.views import HomePageView, TestPageView
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('test/', TestPageView.as_view(), name="test")
]
