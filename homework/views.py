from home.permissions import StudentPermission
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import FormView, DeleteView
from .models import (Homework, StudentHomework,
                     StudentHomeworkFile)
from collections import OrderedDict
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from django.shortcuts import redirect
from django.utils import timezone
from .forms import StudentHomeworkFileForm, StudentHomeworkMultipleFileForm
image_extensions = ('.djvu', '.art', '.cpt', '.tif', '.jpe', '.rgb', '.svgz', '.nef', '.xbm', '.jpeg', '.jpm', '.erf', '.cdt', '.bmp', '.pgm', '.ico', '.xpm', '.jpx', '.pcx', '.ief',
                    '.svg', '.jp2', '.pbm', '.djv', '.cr2', '.png', '.xwd', '.ppm', '.jng', '.jpg2', '.orf', '.cdr', '.gif', '.psd', '.ras', '.pnm', '.crw', '.wbmp', '.pat', '.tiff', '.jpf', '.jpg')


class HomeworkListView(StudentPermission, ListView):
    model = Homework
    template_name = "homework/homework-list.html"

    def get_queryset(self):
        return Homework.objects.all()

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        all_homeworks = []
        homeworks = self.get_queryset()
        for i in homeworks:
            answered = "not answered yet"
            if i.student_homework.filter(user=self.request.user):
                if i.student_homework.filter(user=self.request.user).last().student_homework_file.all():
                    answered = "answered"
            all_homeworks.append({"homework": i,
                                  "answered": answered})
        ctx["homeworks"] = all_homeworks
        return ctx


class HomeworkMultipleUpdateView(FormView):
    template_name = 'homework/homework.html'
    form_class = StudentHomeworkMultipleFileForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.student_is_active is False:
            return redirect('login')
        self.homwork = Homework.objects.get(id=self.kwargs.get("homework_pk"))
        self.student_homework, created = StudentHomework.objects.get_or_create(
            homework=self.homwork, user=self.request.user)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('student_homework_file')

        if form.is_valid():
            for f in files:
                StudentHomeworkFile.objects.create(
                    student_homework=self.student_homework, student_homework_file=f)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        homework = Homework.objects.get(id=self.kwargs.get("homework_pk"))
        homework_questions = homework.homework_file.all()

        student_homework = StudentHomework.objects.filter(
            homework__id=self.kwargs.get("homework_pk"), user=self.request.user).last()

        ctx["homework_questions"] = homework_questions
        ctx["homework"] = homework
        ctx["image_extensions"] = image_extensions
        if student_homework:
            ctx["uploaded_files"] = student_homework.student_homework_file.all()

        return ctx

    def get_success_url(self):
        return reverse_lazy("homework", kwargs={"homework_pk": self.kwargs.get("homework_pk")})


class UploadedFileDeleteView(StudentPermission, DeleteView):
    model = StudentHomeworkFile

    def get_object(self):
        return StudentHomeworkFile.objects.get(id=self.kwargs.get("file_pk"))

    def get_success_url(self):
        return reverse_lazy("homework", kwargs={"homework_pk": self.kwargs.get("homework_pk")})
