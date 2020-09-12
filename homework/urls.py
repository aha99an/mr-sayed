from django.urls import path
from .views import (HomeworkListView,
                    HomeworkMultipleUpdateView,
                    UploadedFileDeleteView
                    )
from .views_admin import HomeworkClassesListView
urlpatterns = [
    path('', HomeworkListView.as_view(), name='homework_list'),
    path('homework/<int:homework_pk>/', HomeworkMultipleUpdateView.as_view(),
         name="homework"),
    path('homework/delete/<int:homework_pk>/<int:file_pk>', UploadedFileDeleteView.as_view(),
         name="delete_file"),
    path('homework-list', HomeworkClassesListView.as_view(),
         name='admin_homework_list'),

]
