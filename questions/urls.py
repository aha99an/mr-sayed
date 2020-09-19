from django.urls import path
from .views import QuestionListView
from .views import QuestionDetailView
from .views import QuestionCreateView
from .views import QuestionallListView


urlpatterns = [
    path('questions-list', QuestionListView.as_view(), name='questions_list'),
    path('question-detail/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'), 
    path('new/', QuestionCreateView.as_view(), name='question_new'), 
    path('all_questions', QuestionallListView.as_view(), name='all_questions'), 
]
