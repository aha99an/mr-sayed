from django.urls import path
from .views import SignUpView, ProfileView, ExamQuestionDetailView
from .views_admin import AdminStudentListView
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('students/', AdminStudentListView.as_view(), name='admin_student_list'),
    path('profile-exam/<int:student_exam_pk>/',
         ExamQuestionDetailView.as_view(), name="profile_exam_first_question"),
    path('profile-exam/<int:student_exam_pk>/<int:question_pk>/',
         ExamQuestionDetailView.as_view(), name="profile_exam_question"),
]
