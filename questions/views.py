from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import MrQuestion
from django.urls import reverse_lazy
from home.permissions import StudentPermission


class QuestionListView (StudentPermission, ListView):
    template_name = "questions/student-questions.html"

    def get_queryset(self):
        return MrQuestion.objects.filter(user=self.request.user)


class QuestionDetailView(StudentPermission, DetailView):
    model = MrQuestion
    template_name = 'questions/question-detail.html'


class QuestionCreateView(StudentPermission, CreateView):
    model = MrQuestion
    template_name = 'questions/question-new.html'
    fields = ('question', 'image_question',)
    success_url = reverse_lazy('student_questions')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
