from django.urls import path
from .views import (ExamListView, QuestionUpdateView)
urlpatterns = [
    path('', ExamListView.as_view(), name='exam_list'),
    # path('exam/<int:pk>/', ExamDetailView.as_view(), name='exam_detail'),
    # path('choice/<int:exam_pk>/<int:question_pk>/', ChoiceQuestionCreateView.as_view(),
    #      name="choice_question"),
    # path('choice/<int:exam_pk>/<int:question_pk>/', ChoiceQuestionUpdateView.as_view(),
    #      name="choice_question"),
    path('question/<int:exam_pk>/<int:question_pk>/', QuestionUpdateView.as_view(),
         name="question"),

]
