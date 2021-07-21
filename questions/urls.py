from django.urls import path
from .views import QuestionListView, QuestionCreateView, QuestionDetailView, upload_to_s3, mr_question_image_success_upload, SelectedQuestionListView
from .views_admin import AdminQuestionUpdateView, AdminQuestionListView, upload_to_s3_admin, delete_image_answer, MrQuestionMultipleUpdateView, mr_question_admin_image_success_upload, MrQuestionsUploadedFileDeleteView

urlpatterns = [
    path('student-questions', QuestionListView.as_view(), name='student_questions'),
    path('selected-student-questions', SelectedQuestionListView.as_view(), name='selected_student_questions'),
    path('question-detail/<int:pk>/',
         QuestionDetailView.as_view(), name='question_detail'),
    path('new/', QuestionCreateView.as_view(), name='question_new'),
    path('all-questions', AdminQuestionListView.as_view(), name='all_questions'),
#     path('answer-question/<int:pk>/',
#          AdminQuestionUpdateView.as_view(), name='answer_question'),
    path('answer-question/<int:pk>/',
         MrQuestionMultipleUpdateView.as_view(), name='answer_question'),
    path('generate-s3-signature', upload_to_s3, name="generate_s3_signature"),
    path('generate-s3-signature-admin', upload_to_s3_admin,
         name="generate_s3_signature_admin"),
    path('delete-image-answer/<int:pk>/', delete_image_answer,
         name="delete_image_answer"),
    path('mr-question-image-success-upload', mr_question_image_success_upload,
         name="mr_question_image_success_upload"),

    path('mr-question-admin-image-success-upload', mr_question_admin_image_success_upload,
         name="mr_question_admin_image_success_upload"),
    path('image/delete/<int:mr_question_pk>/<int:file_pk>', MrQuestionsUploadedFileDeleteView.as_view(),
         name="delete_mr_questions_file"),
         
]
