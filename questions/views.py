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
    success_url = reverse_lazy('student_questions')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class QuestionallListView (ListView):
    model = MrQuestion
    template_name = "questions/all-questions.html"

class QuestionUpdateView(UpdateView): 
    model = MrQuestion
    template_name = 'questions/answer-question.html'
    fields = ('answer', 'image_answer')
    success_url = reverse_lazy('all_questions')

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        question_model = self.get_object()
        ctx['question'] = question_model

        return ctx