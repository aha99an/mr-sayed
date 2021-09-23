from django.urls import path
from home.views import HomePageView, TestPageView
from home.views import ahmedHassan

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('.well-known/acme-challenge/0iDuM9BMYqxmU4d0k7ZaDBc_lQJxClXZFlGO-HrZxVM', TestPageView.as_view(), name="test"),
    path('ahmed-hassan', ahmedHassan.as_view(), name='ahmed_hassan'),

]
