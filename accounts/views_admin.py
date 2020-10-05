from django.views.generic import UpdateView, ListView, DeleteView
from .models import CustomUser
from .forms import StudentChangeForm, test
from classes.models import Class
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
import random
from home.permissions import AdminPermission
from lectures.models import Lecture, StudentLectureMakeup
from django.db.models import Q


class AdminStudentListView(AdminPermission, ListView):
    queryset = CustomUser.objects.filter(user_type=CustomUser.STUDENT)
    template_name = "accounts/admin-students-list.html"
    paginate_by = 10

    def get_queryset(self):
        try:
            a = self.request.GET.get('account',)
        except KeyError:
            a = None

        if a:

            admin_student_list1 = Q(
                first_name__contains=a, user_type=CustomUser.STUDENT)
            admin_student_list2 = Q(
                username__contains=a, user_type=CustomUser.STUDENT)
            admin_student_list3 = Q(
                student_class__name__contains=a, user_type=CustomUser.STUDENT)
            q = CustomUser.objects.filter(
                admin_student_list1 | admin_student_list2 | admin_student_list3)

        else:
            q = CustomUser.objects.filter(user_type=CustomUser.STUDENT)
        return q


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
        ctx["lectures"] = Lecture.objects.all()
        ctx["makeup_lectures"] = StudentLectureMakeup.objects.filter(
            user=ctx["student_user"])
        ctx["formo"] = test
        return ctx


def reset_password(request, pk):
    user = CustomUser.objects.get(id=pk)
    user.random_password = random.randint(0, 999999)
    user.set_password(user.random_password)
    user.save()
    return HttpResponseRedirect(reverse_lazy("student_update_view", kwargs={"pk": pk}))


def index2(request, pk):
    if request.method == 'POST':
        StudentLectureMakeup.objects.get_or_create(
            user=CustomUser.objects.get(id=pk), lecture=Lecture.objects.get(id=int(request.POST.get("lecture_id"))))

    return HttpResponseRedirect(reverse_lazy("student_update_view", kwargs={"pk": pk}))


class LectureMakeupDeleteView(AdminPermission, DeleteView):
    model = StudentLectureMakeup

    def get_object(self):
        return StudentLectureMakeup.objects.get(id=self.kwargs.get("makeup_lecture_pk"))

    def get_success_url(self):
        return reverse_lazy("student_update_view", kwargs={"pk": self.kwargs.get("student_pk")})
