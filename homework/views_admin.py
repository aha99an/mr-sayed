from django.views.generic import ListView, UpdateView
from django.views.generic.edit import DeleteView
from .models import (Homework, HomeworkFile, StudentHomework,
                     StudentHomeworkFile)
from classes.models import Class
from .forms import AdminHomeworkForm
from django.urls import reverse_lazy


class HomeworkAdminListView(ListView):
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
        ctx = super(HomeworkAdminListView, self).get_context_data(**kwargs)
        ctx["classes"] = Class.objects.all()
        ctx["class_filter"] = self.request.GET.get('class_filter')
        ctx["is_checked_filter"] = self.request.GET.get('is_checked_filter')

        return ctx


class HomeworkAdminUpdateView(UpdateView):
    model = StudentHomework
    template_name = 'homework/admin-check-homework.html'
    form_class = AdminHomeworkForm
    success_url = reverse_lazy('admin_homework_list')

    # def get_object(self):

    #     all_questions = get_all_questions(self.exam.id, self.request.user)
    #     question_content = all_questions[self.kwargs.get("question_pk")]

    #     # get or create student answer
    #     answer, created = question_content["answer_model"].objects.get_or_create(
    #         question=question_content["question"], student_exam=self.student_exam)
    #     return answer

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        student_homework = StudentHomework.objects.get(
            id=self.kwargs.get("pk"))
        ctx["student_homework"] = student_homework.homework
        ctx["student_homework_files"] = student_homework.student_homework_file.all()

        ctx["homework_questions"] = student_homework.homework.homework_file.all()
        return ctx
