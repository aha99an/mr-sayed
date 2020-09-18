from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import MrQuestion
class QuestionListView (ListView):
    model = MrQuestion
    template_name = "questions/student-questions.html"

class QuestionDetailView(DetailView):
    model = MrQuestion
    template_name = 'questions/question-detail.html'