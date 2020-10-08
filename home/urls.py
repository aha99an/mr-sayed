from django.urls import path
from home.views import HomePageView, TestView
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('test', TestView.as_view(), name="test")
]
