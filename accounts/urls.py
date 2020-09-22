from django.urls import path
from .views import SignUpView, ProfileView, ExamQuestionDetailView, HomeworkDetailView
from .views_admin import AdminStudentListView, AdminStudentUpdateView, reset_password


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('students/', AdminStudentListView.as_view(), name='admin_student_list'),
    path('profile-exam/<int:student_exam_pk>/<int:question_pk>/',
         ExamQuestionDetailView.as_view(), name="profile_exam_question"),
    path('profile-homework/<int:pk>/',
         HomeworkDetailView.as_view(), name="profile_homework"),
    path("student/<int:pk>", AdminStudentUpdateView.as_view(),
         name="student_update_view"),
    path("admin-reset-password/<int:pk>", reset_password,
         name="student_reset_password"),
]
