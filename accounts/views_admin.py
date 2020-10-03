from django.views.generic import UpdateView, ListView
from .models import CustomUser
from .forms import StudentChangeForm
from classes.models import Class
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
import random
from home.permissions import AdminPermission



class AdminStudentListView(AdminPermission, ListView):
    queryset = CustomUser.objects.filter(user_type=CustomUser.STUDENT)
    template_name = "accounts/admin-students-list.html"
    paginate_by = 20
    def get_queryset(self):
        try:
            a = self.request.GET.get('account',)
        except KeyError:
            a = None
        if a:
            admin_student_list = CustomUser.objects.filter(first_name=a,user_type=CustomUser.STUDENT)
            admin_student_list = CustomUser.objects.filter(username=a,user_type=CustomUser.STUDENT)
            admin_student_list = CustomUser.objects.filter(student_class__name=a,user_type=CustomUser.STUDENT)

        else:
            admin_student_list = CustomUser.objects.filter(user_type=CustomUser.STUDENT)
        return admin_student_list

class AdminStudentUpdateView(AdminPermission, UpdateView):
    model = CustomUser
    form_class = StudentChangeForm
    template_name = "accounts/admin-student-update.html"
    success_url = reverse_lazy("admin_student_list")

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["classes"] = Class.objects.all()
        ctx["student_user"] = CustomUser.objects.get(id=self.kwargs["pk"])
        ctx["reseted_password"] = ctx["student_user"].check_password(
            ctx["student_user"].random_password)
        return ctx


def reset_password(request, pk):
    user = CustomUser.objects.get(id=pk)
    user.random_password = random.randint(0, 999999)
    user.set_password(user.random_password)
    user.save()
    return HttpResponseRedirect(reverse_lazy("student_update_view", kwargs={"pk": pk}))
