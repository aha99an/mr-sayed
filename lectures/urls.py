from django.urls import path
from .views import LectureListView, LectureDetailView
from .views_admin import AdminLectureListView, AdminLectureCreateView
urlpatterns = [
    path('', LectureListView.as_view(), name='lectures_list'),
    path('lecture/<int:pk>/', LectureDetailView.as_view(),
         name="lecture"),
    path('admin-lectures/', AdminLectureListView.as_view(),
         name="admin_lectures_list"),
    path('create-lecture/', AdminLectureCreateView.as_view(),
         name="create_lecture"),


]
