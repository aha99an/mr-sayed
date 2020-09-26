from django.urls import path
from .views import LectureListView, LectureDetailView
from .views_admin import AdminLectureListView, AdminLectureCreateView,\
    AdminLectureUpdateView, AdminLectureLinkDeleteView, AdminLectureDeleteView
urlpatterns = [
    path('', LectureListView.as_view(), name='lectures_list'),
    path('lecture/<int:pk>/', LectureDetailView.as_view(),
         name="lecture"),
    path('admin-lectures/', AdminLectureListView.as_view(),
         name="admin_lectures_list"),
    path('create-lecture/', AdminLectureCreateView.as_view(),
         name="create_lecture"),
    path('update-lecture/<int:pk>/', AdminLectureUpdateView.as_view(),
         name="update_lecture"),
    path('delete-lecture-link/<int:pk>/', AdminLectureLinkDeleteView.as_view(),
         name="delete_lecture_link"),
    path('delete-lecture/<int:pk>/', AdminLectureDeleteView.as_view(),
         name="delete_lecture"),


]
