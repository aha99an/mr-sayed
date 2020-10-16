from django.urls import path
from .views import (SignUpView, ProfileView, ExamQuestionDetailView,
                    HomeworkDetailView, MyProfileDataUpdateView, IsNotActiveTemplateView)
from .views_admin import (AdminStudentListView, AdminStudentUpdateView, reset_password,
                          add_makeup_lecture, LectureMakeupDeleteView, AdminAccountDeleteView, AdminMyProfileData,
                          AdminMyProfileDataUpdateView, ExamMakeupDeleteView, add_makeup_exam, StudentPaymentUpdateView)


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
    path("admin-add-makeup-lecture/<int:pk>", add_makeup_lecture,
         name="admin_add_makeup_lecture"),
    path('admin-delete-makeup-lecture/delete/<int:makeup_lecture_pk>/<int:student_pk>', LectureMakeupDeleteView.as_view(),
         name="delete_makeup_lecture"),
    path("admin-add-makeup-exam/<int:pk>", add_makeup_exam,
         name="admin_add_makeup_exam"),
    path('admin-delete-makeup-exam/delete/<int:makeup_exam_pk>/<int:student_pk>', ExamMakeupDeleteView.as_view(),
         name="delete_makeup_exam"),
    path('delete-account/<int:pk>/', AdminAccountDeleteView.as_view(),
         name="delete_account"),
    path("my-profile-data/<int:pk>", MyProfileDataUpdateView.as_view(),
         name="student_update_data"),
    path("admin-my-profile-data/<int:pk>", AdminMyProfileDataUpdateView.as_view(),
         name="admin_student_update_data"),
    path("account-not-active", IsNotActiveTemplateView.as_view(),
         name="account_not_active"),
    path("student-payment-update-view/<int:student_pk>/", StudentPaymentUpdateView.as_view(),
         name="student_payment_update_view"),

]
