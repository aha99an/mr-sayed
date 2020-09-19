from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import MrQuestion
from django.urls import reverse_lazy



class QuestionListView (ListView):
    template_name = "questions/student-questions.html"
    def get_queryset(self):
        return MrQuestion.objects.filter(user=self.request.user)

class QuestionDetailView(DetailView):
    model = MrQuestion
    template_name = 'questions/question-detail.html'


class QuestionCreateView(CreateView):
    model = MrQuestion
    template_name = 'questions/question-new.html'
    fields = ('question', 'image_question',)
    success_url = reverse_lazy('questions_list')

    def form_valid(self, form): # new
        form.instance.user = self.request.user
        return super().form_valid(form)


class QuestionallListView (ListView):
    model = MrQuestion
    template_name = "questions/student-questions.html"
   