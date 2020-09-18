from django.views.generic import CreateView, ListView
from .models import CustomUser


class AdminStudentListView(ListView):
    model = CustomUser
    template_name = "accounts/admin-students-list.html"
