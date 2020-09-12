from django.urls import path
from .views import LectureListView, LectureDetailView

urlpatterns = [
    path('', LectureListView.as_view(), name='lectures_list'),
    path('lecture/<int:pk>/', LectureDetailView.as_view(),
         name="lecture"),
    # path('homework/delete/<int:homework_pk>/<int:file_pk>', UploadedFileDeleteView.as_view(),
    #      name="delete_file"),

]
