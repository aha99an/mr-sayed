from django.urls import path
from .views import QuestionListView
from .views import QuestionDetailView
from .views import QuestionCreateView
from .views_admin import AdminQuestionUpdateView, AdminQuestionListView

urlpatterns = [
    path('student-questions', QuestionListView.as_view(), name='student_questions'),
    path('question-detail/<int:pk>/',
         QuestionDetailView.as_view(), name='question_detail'),
    path('new/', QuestionCreateView.as_view(), name='question_new'),
    path('all-questions', AdminQuestionListView.as_view(), name='all_questions'),
    path('answer-question/<int:pk>/',
         AdminQuestionUpdateView.as_view(), name='answer_question'),
]
