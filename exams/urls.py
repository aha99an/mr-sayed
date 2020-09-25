from django.urls import path
from .views import (ExamListView, QuestionUpdateView)
from .views_admin import (ExamAdminListView, AdminChoiceQuestion, update_view, AdminAddExamListView,
                          AdminExamCreateView, AdminExamUpdateView, AdminExamDeleteView,
                          AdminChoiceQuestionCreateView, AdminEssayQuestionCreateView, AdminEssayQuestionUpdateView, AdminChoiceQuestionUpdateView,
                          AdminChoiceQuestionDeleteView, AdminEssayQuestionDeleteView)


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

    path('exam-list-add/', AdminAddExamListView.as_view(),
         name='admin_add_exam_list'),
    path('exam-create/', AdminExamCreateView.as_view(), name='admin_create_exam'),
    path('exam-update/<int:pk>/', AdminExamUpdateView.as_view(),
         name='admin_update_exam'),
    path('exam-delete/<int:pk>/', AdminExamDeleteView.as_view(),
         name='admin_delete_exam'),
    path('exam-create-choice-question/<int:pk>/',
         AdminChoiceQuestionCreateView.as_view(), name='admin_create_choice_question'),
    path('exam-create-essay-question/<int:pk>/',
         AdminEssayQuestionCreateView.as_view(), name='admin_create_essay_question'),
    path('exam-update-essay-question/<int:pk>/',
         AdminEssayQuestionUpdateView.as_view(), name='admin_update_essay_question'),
    path('exam-update-choice-question/<int:pk>/',
         AdminChoiceQuestionUpdateView.as_view(), name='admin_update_choice_question'),
    path('exam-delete-choice-question/<int:pk>/',
         AdminChoiceQuestionDeleteView.as_view(), name='admin_delete_choice_question'),
    path('exam-delete-essay-question/<int:pk>/',
         AdminEssayQuestionDeleteView.as_view(), name='admin_delete_essay_question'),
]
