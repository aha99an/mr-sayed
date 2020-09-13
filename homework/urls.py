from django.urls import path
from .views_admin import HomeworkAdminListView, HomeworkAdminUpdateView
from .views import (HomeworkListView,
                    HomeworkMultipleUpdateView,
                    UploadedFileDeleteView
                    )

urlpatterns = [
    path('', HomeworkListView.as_view(), name='homework_list'),
    path('homework/<int:homework_pk>/', HomeworkMultipleUpdateView.as_view(),
         name="homework"),
    path('homework/delete/<int:homework_pk>/<int:file_pk>', UploadedFileDeleteView.as_view(),
         name="delete_file"),
    path('homework-list', HomeworkAdminListView.as_view(),
         name='admin_homework_list'),
    path('check-homework/<int:pk>', HomeworkAdminUpdateView.as_view(),
         name='admin_check_homework'),

]
