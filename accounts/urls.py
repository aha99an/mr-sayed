from django.urls import path
from .views import (SignUpView, ProfileView, ExamQuestionDetailView,
                    HomeworkDetailView, MyProfileDataUpdateView, IsNotActiveTemplateView)
from .views_admin import (AdminStudentListView, AdminStudentUpdateView, reset_password,AdminProfileView,
                          add_makeup_lecture, LectureMakeupDeleteView, AdminAccountDeleteView, AdminMyProfileData,
                          AdminMyProfileDataUpdateView, ExamMakeupDeleteView, add_makeup_exam, StudentPaymentUpdateView,
                          AdminStudentPaymentListView, StudentPaymentCreateView, AdminStudentPaymentDeleteView,
                          add_makeup_homework, HomeworkMakeupDeleteView, AdminHomeworkDetailView)


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('admin-profile/<int:pk>', AdminProfileView.as_view(), name='admin_profile'),
    path('students/', AdminStudentListView.as_view(), name='admin_student_list'),
    path('profile-exam/<int:student_exam_pk>/<int:question_pk>/',
         ExamQuestionDetailView.as_view(), name="profile_exam_question"),
    path('profile-homework/<int:pk>/',
         HomeworkDetailView.as_view(), name="profile_homework"),
    path('admin-profile-homework/<int:pk>/',
         AdminHomeworkDetailView.as_view(), name="admin_profile_homework"),
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
    path("admin-add-makeup-homework/<int:pk>", add_makeup_homework,
         name="admin_add_makeup_homework"),
    path('admin-delete-makeup-homework/delete/<int:makeup_homework_pk>/<int:student_pk>', HomeworkMakeupDeleteView.as_view(),
         name="admin_delete_makeup_homework"),
    path('delete-account/<int:pk>/', AdminAccountDeleteView.as_view(),
         name="delete_account"),
    path("my-profile-data/<int:pk>", MyProfileDataUpdateView.as_view(),
         name="student_update_data"),
    path("admin-my-profile-data/<int:pk>", AdminMyProfileDataUpdateView.as_view(),
         name="admin_student_update_data"),
    path("account-not-active", IsNotActiveTemplateView.as_view(),
         name="account_not_active"),
    path("admin-student-payment-update-view/<int:pk>/<int:student_pk>/", StudentPaymentUpdateView.as_view(),
         name="student_payment_update_view"),
    path("admin-student-payment-list-view/<int:student_pk>/", AdminStudentPaymentListView.as_view(),
         name="admin_student_payment_list_view"),
    path("admin-student-payment-create-view/<int:student_pk>/", StudentPaymentCreateView.as_view(),
         name="admin_student_payment_create_view"),
    path("admin-student-payment-delete-view/<int:pk>/<int:student_pk>/", AdminStudentPaymentDeleteView.as_view(),
         name="admin_student_payment_delete_view"),
]
