from django.urls import path
from .views import QuestionListView
from .views import QuestionDetailView


urlpatterns = [
    path('questions-list', QuestionListView.as_view(), name='questions_list'),
    path('question-detail/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'), # new
]
