from django.views.generic import ListView, UpdateView, CreateView
from django.views.generic.edit import DeleteView
from .models import (Homework, StudentHomework,
                     StudentHomeworkFile, )
from classes.models import Class
from .forms import AdminHomeworkForm
from django.urls import reverse_lazy
from home.permissions import AdminPermission


class AdminCheckHomeworkListView(AdminPermission, ListView):
    model = StudentHomework
    template_name = "homework/admin-homework-list.html"
    # queryset = StudentHomework.objects.all()

    def get_queryset(self):
        queryset = StudentHomework.objects.all()
        class_filter = self.request.GET.get('class_filter')
        is_checked_filter = self.request.GET.get('is_checked_filter')
        if class_filter:
            queryset = queryset.filter(
                user__student_class__name=class_filter)
        if is_checked_filter:
            if is_checked_filter == "True":
                queryset = queryset.filter(is_checked=True)
            else:
                queryset = queryset.filter(is_checked=False)

        return queryset

    def get_context_data(self, **kwargs):
        ctx = super(AdminCheckHomeworkListView,
                    self).get_context_data(**kwargs)
        ctx["classes"] = Class.objects.all()
        ctx["class_filter"] = self.request.GET.get('class_filter')
        ctx["is_checked_filter"] = self.request.GET.get('is_checked_filter')

        return ctx


class AdminCheckHomeworkUpdateView(AdminPermission, UpdateView):
    model = StudentHomework
    template_name = 'homework/admin-check-homework.html'
    form_class = AdminHomeworkForm
    success_url = reverse_lazy('admin_homework_list')

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        student_homework = StudentHomework.objects.get(
            id=self.kwargs.get("pk"))
        ctx["student_homework"] = student_homework.homework
        ctx["student_homework_files"] = student_homework.student_homework_file.all()

        ctx["homework_questions"] = student_homework.homework.homework_file.all()
        return ctx


class AdminCreateHomeworkView(AdminPermission, CreateView):
    model = Homework
    template_name = 'homework/admin-create-homework.html'
    fields = ['name', 'week', 'homework_file',
              'homework_text', 'homework_answer_file']
    success_url = reverse_lazy('admin_add_homework_list')


class AdminUpdateHomeworkView(AdminPermission, UpdateView):
    model = Homework
    template_name = 'homework/admin-update-homework.html'
    fields = ['name', 'week', 'homework_file',
              'homework_text', 'homework_answer_file']
    success_url = reverse_lazy('admin_add_homework_list')


class AdminAddHomeworkListView (AdminPermission, ListView):
    model = Homework
    template_name = "homework/admin-add-homework-list.html"


class AdminDeleteHomework(AdminPermission, DeleteView):
    model = Homework
    success_url = reverse_lazy('admin_add_homework_list')
