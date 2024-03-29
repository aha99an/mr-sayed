from django.views.generic import UpdateView, ListView, DeleteView, CreateView, TemplateView, DetailView
from .models import CustomUser, StudentPayment
from .forms import StudentChangeForm, test, AdminMyProfileData, AdminStudentPayment, AdminStudentPaymentUpdateForm
from classes.models import Class
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
import random
from home.permissions import AdminPermission
from lectures.models import Lecture, StudentLectureMakeup, StudentLecture
from exams.models import Exam, StudentExamMakeup, StudentExam
from django.db.models import Q
from homework.models import Homework, StudentHomeworkMakeup, StudentHomework
from django.utils import timezone
from datetime import datetime
now = datetime.now()

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
        ctx["lectures"] = Lecture.objects.filter(is_permanent=False)
        ctx["makeup_lectures"] = StudentLectureMakeup.objects.filter(
            user=ctx["student_user"])

        ctx["exams"] = Exam.objects.all()
        ctx["makeup_exams"] = StudentExamMakeup.objects.filter(
            user=ctx["student_user"])

        ctx["homeworks"] = Homework.objects.all()
        ctx["makeup_homeworks"] = StudentHomeworkMakeup.objects.filter(
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
        lecture_id = int(request.POST.get("lecture_id"))
        user = CustomUser.objects.get(id=pk)
        
        StudentLectureMakeup.objects.get_or_create(
            user=user, lecture=Lecture.objects.get(id=lecture_id))

        student_lecture = StudentLecture.objects.filter(lecture=lecture_id, user=user).last()
        if student_lecture:
            student_lecture.seen_at = None
            student_lecture.save()

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


def add_makeup_homework(request, pk):
    if request.method == 'POST':
        StudentHomeworkMakeup.objects.get_or_create(
            user=CustomUser.objects.get(id=pk), homework=Homework.objects.get(id=int(request.POST.get("homework_id"))))

    return HttpResponseRedirect(reverse_lazy("student_update_view", kwargs={"pk": pk}))


class HomeworkMakeupDeleteView(AdminPermission, DeleteView):
    model = StudentHomeworkMakeup

    def get_object(self):
        return StudentHomeworkMakeup.objects.get(id=self.kwargs.get("makeup_homework_pk"))

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
    form_class = AdminStudentPaymentUpdateForm
    template_name = 'accounts/admin-student-payment.html'

    def get_success_url(self):
        return reverse_lazy("admin_student_payment_list_view", kwargs={"student_pk": self.kwargs.get("student_pk")})


class StudentPaymentCreateView(AdminPermission, CreateView):
    model = StudentPayment
    form_class = AdminStudentPayment
    template_name = 'accounts/admin-student-payment.html'

    def form_valid(self, form):
        form.instance.user = CustomUser.objects.get(
            id=self.kwargs.get("student_pk"))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("admin_student_payment_list_view", kwargs={"student_pk": self.kwargs.get("student_pk")})


class AdminStudentPaymentListView(AdminPermission, ListView):
    template_name = "accounts/admin-student-payment-list.html"

    def get_queryset(self):
        queryset = StudentPayment.objects.filter(
            user__id=self.kwargs.get("student_pk"))
        return queryset

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["student_pk"] = self.kwargs.get("student_pk")
        return ctx


class AdminStudentPaymentDeleteView(AdminPermission, DeleteView):
    model = StudentPayment

    def get_success_url(self):
        return reverse_lazy("admin_student_payment_list_view", kwargs={"student_pk": self.kwargs.get("student_pk")})


class AdminProfileView(AdminPermission, TemplateView):
    template_name = 'accounts/admin-profile.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["student_user"] = CustomUser.objects.get(id=self.kwargs["pk"])

        # we will check for show_answer field and make it true in case of we exceeded el end time bta3 el week (7esa)
        homeworks = []
        exams = []
        
        #add homeworks 
        all_homeworks = Homework.objects.all()
        for homework in all_homeworks:
            answered = False
            student_homework = StudentHomework.objects.filter(
                user=self.kwargs.get("pk"), homework=homework).last()
            if student_homework and student_homework.student_homework_file.all():
                answered = True
            homeworks.append({"homework": homework, "answered": answered})

        # add exams
        all_exams = Exam.objects.all()
        for exam in all_exams:
            exam_answered = False
            student_exam = StudentExam.objects.filter(
                user=self.kwargs.get("pk"), exam=exam).last()
            exam_grade = exam.grade
            exam_answered = False
            if student_exam:
                exam_answered = True
            exams.append({"exam": exam, "student_exam": student_exam})

        ctx["homeworks"] = homeworks
        ctx["exams"] = exams
        return ctx
