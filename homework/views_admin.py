from django.views.generic import ListView, UpdateView
from django.views.generic.edit import FormView, DeleteView
from .models import (Homework, HomeworkFile, HomeworkAnswerFile, StudentHomework,
                     StudentHomeworkFile, HomeworkNotebook)
from classes.models import Class


class HomeworkClassesListView(ListView):
    model = StudentHomework
    template_name = "homework/admin-homework-list.html"
    queryset = StudentHomework.objects.all()

    def get_queryset(self):
        class_filter = self.request.GET.get('class_filter')
        print(class_filter, "HHHHHHHHHH")
        if class_filter:
            self.queryset = StudentHomework.objects.filter(
                user__student_class__name=class_filter)

        # order = self.request.GET.get('orderby', 'give-default-value')
        # if filter_val:
        #     new_context = StudentHomework.objects.filter(
        #         state=filter_val,
        return self.queryset

    def get_context_data(self, **kwargs):
        ctx = super(HomeworkClassesListView, self).get_context_data(**kwargs)
        ctx["classes"] = Class.objects.all()
        ctx["class_filter"] = self.request.GET.get('class_filter')
        return ctx
