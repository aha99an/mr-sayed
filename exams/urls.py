from django.urls import path
from .views import TrainingListView, ExamDetailView
urlpatterns = [
    path('', TrainingListView.as_view(), name='exam_list'),
    path('exam/<int:pk>/', ExamDetailView.as_view(), name='exam_detail'),

]
app_name = 'exams'
