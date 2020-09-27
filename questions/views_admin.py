from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import MrQuestion
from django.urls import reverse_lazy
from home.permissions import AdminPermission


class AdminQuestionListView (AdminPermission, ListView):
    model = MrQuestion
    template_name = "questions/all-questions.html"


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
