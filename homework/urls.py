from django.urls import path
from .views_admin import AdminCheckHomeworkListView, AdminCheckHomeworkUpdateView, AdminCreateHomeworkView ,AdminUpdateHomeworkView ,AdminAddHomeworkListView,AdminDeleteHomework
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
     path('homework-list', AdminCheckHomeworkListView.as_view(),
         name='admin_homework_list'),
     path('check-homework/<int:pk>', AdminCheckHomeworkUpdateView.as_view(),
         name='admin_check_homework'),
     path('admin-create-homework', AdminCreateHomeworkView.as_view(),
         name="admin_create_homework"),
    path('admin-update-homework/<int:pk>/', AdminUpdateHomeworkView.as_view(),
         name="admin_update_homework"),
    path('admin-add-homework-list', AdminAddHomeworkListView.as_view(),
         name="admin_add_homework_list"),

         path('admin-delet-homework/<int:pk>/', AdminDeleteHomework.as_view(),
         name="admin_delete_homework"),
]
