from django.urls import path
from .views import (ClassListView, ClassCreateView, ClassUpdateView, ClassDeleteView, WeekListView
                    )
urlpatterns = [
    path('classes/', ClassListView.as_view(), name='class_list'),
    path('create-class/', ClassCreateView.as_view(), name='create_class'),
    path('update-class/<int:pk>', ClassUpdateView.as_view(), name='update_class'),
    path('delete-class/<int:pk>', ClassDeleteView.as_view(), name='delete_class'),

    path('weeks/', WeekListView.as_view(), name='week_list'),

    # path('homework/<int:homework_pk>/', HomeworkMultipleUpdateView.as_view(),
    #      name="homework"),
    # path('homework/delete/<int:homework_pk>/<int:file_pk>', UploadedFileDeleteView.as_view(),
    #      name="delete_file"),

]