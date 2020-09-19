from django.urls import path
from .views import QuestionListView
from .views import QuestionDetailView
from .views import QuestionCreateView
from .views import QuestionallListView
from .views import QuestionUpdateView


urlpatterns = [
    path('student-questions', QuestionListView.as_view(), name='student_questions'),
    path('question-detail/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'), 
    path('new/', QuestionCreateView.as_view(), name='question_new'), 
    path('all-questions', QuestionallListView.as_view(), name='all_questions'), 
    path('answer-question/<int:pk>/', QuestionUpdateView.as_view(), name='answer_question'), 
]
