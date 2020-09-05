from django.urls import path
from .views import (HomeworkListView,
                    HomeworkUpdateView,
                    HomeworkMultipleUpdateView,
                    UploadedFileDeleteView
                    )
urlpatterns = [
    path('', HomeworkListView.as_view(), name='homework_list'),
    path('homework/<int:homework_pk>/', HomeworkMultipleUpdateView.as_view(),
         name="homework"),
    path('homework/delete/<int:home_work_answer_file_pk>', UploadedFileDeleteView.as_view(),
         name="delete_file"),

]
