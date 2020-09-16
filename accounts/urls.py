from django.urls import path
from .views import SignUpView, ProfileView
from .views_admin import AdminStudentListView
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('students/', AdminStudentListView.as_view(), name='admin_student_list')

]
