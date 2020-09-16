from django.urls import path
from .views import (ExamListView, QuestionUpdateView)
from .views_admin import ExamAdminListView, AdminChoiceQuestion, update_view
urlpatterns = [
    path('', ExamListView.as_view(), name='exam_list'),
    path('question/<int:exam_pk>/<int:question_pk>/', QuestionUpdateView.as_view(),
         name="question"),
    # Admin urls
    path('exam-list/', ExamAdminListView.as_view(), name='admin_exam_list'),
    path('choice-question/<int:student_exam_pk>/<int:question_pk>/',
         AdminChoiceQuestion.as_view(), name='admin_choice_question'),

    path('choice-question/<int:student_exam_pk>/',
         AdminChoiceQuestion.as_view(), name='admin_first_choice_question'),

    path('update_grade/<int:student_essay_answer_pk>/<int:question_pk>/',
         update_view, name='update_grade'),
]
