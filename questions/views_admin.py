from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import MrQuestion
from django.urls import reverse_lazy
from home.permissions import AdminPermission


class AdminQuestionListView (AdminPermission, ListView):
    model = MrQuestion
    template_name = "questions/all-questions.html"
    paginate_by = 10

    # def get_queryset(self):
    #     try:
    #         a = self.request.GET.get('exam',)
    #     except KeyError:
    #         a = None
    #     q = MrQuestion.objects.all()

    #     class_filter = self.request.GET.get('class_filter')
    #     is_answered = self.request.GET.get('is_answered')
    #     if class_filter:
    #         q = q.filter(
    #             user__student_class__name=class_filter)
    #     if is_answered:
    #         if is_answered == "True":
    #             q = q.filter(is_graded=True)
    #         else:
    #             q = q.filter(is_graded=False)

    #     return q






    def get_queryset(self):
        queryset = MrQuestion.objects.all()
        class_filter = self.request.GET.get('class_filter')
        is_answered = self.request.GET.get('is_answered')
        if class_filter:
            queryset = queryset.filter(
                user__is_answered=class_filter)
        if is_answered:
            if is_answered == "True":
                queryset = queryset.filter(is_answered=True)
            else:
                queryset = queryset.filter(is_answered=False)
        return queryset





class AdminQuestionUpdateView(AdminPermission, UpdateView):
    model = MrQuestion
    template_name = 'questions/answer-question.html'
    fields = ('answer', 'image_answer')
    success_url = reverse_lazy('all_questions')

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        question_model = self.get_object()
        ctx['question'] = question_model

        return ctx
