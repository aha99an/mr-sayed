from django.views.generic import UpdateView, ListView, DeleteView
from .models import CustomUser, StudentPayment
from .forms import StudentChangeForm, test, AdminMyProfileData, AdminStudentPayment
from classes.models import Class
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
import random
from home.permissions import AdminPermission
from lectures.models import Lecture, StudentLectureMakeup
from exams.models import Exam, StudentExamMakeup
from django.db.models import Q
import difflib


class AdminStudentListView(AdminPermission, ListView):
    queryset = CustomUser.objects.filter(user_type=CustomUser.STUDENT)
    template_name = "accounts/admin-students-list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = CustomUser.objects.filter(user_type=CustomUser.STUDENT)

        # Search
        search_value = self.request.GET.get('search_value',)
        if search_value:
            admin_student_list1 = Q(
                first_name__contains=search_value, user_type=CustomUser.STUDENT)
            admin_student_list2 = Q(
                username__contains=search_value, user_type=CustomUser.STUDENT)
            admin_student_list3 = Q(
                student_class__name__contains=search_value, user_type=CustomUser.STUDENT)
            queryset = CustomUser.objects.filter(
                admin_student_list1 | admin_student_list2 | admin_student_list3)
        # Filter
        student_is_active = self.request.GET.get('student_is_active')
        # print(difflib.get_close_matches('Hello', ["hello"])

        if student_is_active:
            if student_is_active == "True":
                queryset = queryset.filter(student_is_active=True)
            else:
                queryset = queryset.filter(student_is_active=False)

        return queryset

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["students_count"] = CustomUser.objects.filter(
            user_type=CustomUser.STUDENT).count()
        ctx["students_active"] = CustomUser.objects.filter(
            student_is_active=True, user_type=CustomUser.STUDENT).count()
        return ctx


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

        ctx["exams"] = Exam.objects.all()
        ctx["makeup_exams"] = StudentExamMakeup.objects.filter(
            user=ctx["student_user"])
        return ctx


def reset_password(request, pk):
    user = CustomUser.objects.get(id=pk)
    user.random_password = random.randint(0, 999999)
    user.set_password(user.random_password)
    user.save()
    return HttpResponseRedirect(reverse_lazy("student_update_view", kwargs={"pk": pk}))


def add_makeup_lecture(request, pk):
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


def add_makeup_exam(request, pk):
    if request.method == 'POST':
        StudentExamMakeup.objects.get_or_create(
            user=CustomUser.objects.get(id=pk), exam=Exam.objects.get(id=int(request.POST.get("exam_id"))))

    return HttpResponseRedirect(reverse_lazy("student_update_view", kwargs={"pk": pk}))


class ExamMakeupDeleteView(AdminPermission, DeleteView):
    model = StudentExamMakeup

    def get_object(self):
        return StudentExamMakeup.objects.get(id=self.kwargs.get("makeup_exam_pk"))

    def get_success_url(self):
        return reverse_lazy("student_update_view", kwargs={"pk": self.kwargs.get("student_pk")})


class AdminAccountDeleteView(AdminPermission, DeleteView):
    model = CustomUser

    def get_success_url(self):
        return reverse_lazy("admin_student_list")


class AdminMyProfileDataUpdateView(AdminPermission, UpdateView):
    template_name = 'accounts/admin-my-profile-data.html'
    model = CustomUser
    success_url = reverse_lazy("admin_student_list")
    form_class = AdminMyProfileData


class StudentPaymentUpdateView(AdminPermission, UpdateView):
    model = StudentPayment
    form_class = AdminStudentPayment
    template_name = 'accounts/admin-student-payment.html'

    def get_object(self):
        this_user = CustomUser.objects.get(id=self.kwargs.get("student_pk"))
        student_payment, created = StudentPayment.objects.get_or_create(
            user=this_user)
        return student_payment

    def get_success_url(self):
        return reverse_lazy("student_update_view", kwargs={"pk": self.kwargs.get("student_pk")})
