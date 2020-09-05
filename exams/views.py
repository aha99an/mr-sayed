from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import (Exam, EssayQuestion, TrueFalseQuestion, ChoiceQuestion,
                     StudentExam, StudentChoiceAnswer, StudentEssayAnswer)
from collections import OrderedDict
from .forms import StudentChoiceAnswerForm, StudentEssayAnswerForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.utils import timezone


def get_all_questions(exam_id):
    exam = Exam.objects.get(id=exam_id)
    # get questions
    questions = OrderedDict()
    exam_choice_qs = exam.choice_question.all()
    exam_essay_qs = exam.essay_question.all()
    question_index = 1

    # Choice questions
    for question in exam_choice_qs:
        # question status
        answered = "not answered"
        if question.student_choice_answer.all():
            if question.student_choice_answer.all() and question.student_choice_answer.first().answer:
                answered = "answered"

        questions[question_index] = {"url": "choice_question",
                                     "type": "choice_question",
                                     "question": question,
                                     "answered": answered,
                                     "answer_model": StudentChoiceAnswer}
        question_index += 1

    for question in exam_essay_qs:
        # question status
        answered = "not answered"
        if question.student_essay_answer.all():
            if question.student_essay_answer.first().answer or question.student_essay_answer.first().image_answer:
                answered = "answered"

        questions[question_index] = {"url": "essay_question",
                                     "type": "essay_question",
                                     "question": question,
                                     "answered": answered,
                                     "answer_model": StudentEssayAnswer}
        question_index += 1

    return questions


class ExamListView(ListView):
    model = Exam
    template_name = "exams/exam-list.html"

    def get_queryset(self):
        return Exam.objects.filter(is_active=True)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        all_exams = []
        exams = self.get_queryset()
        for i in exams:
            answered = "not answered yet"
            if i.student_exam.all():
                answered = "answered"
            all_exams.append({"exam": i,
                              "answered": answered})
        ctx["exams"] = all_exams
        if self.request.session.get('exam_time_expired'):
            ctx["exam_time_expired"] = True
            del self.request.session["exam_time_expired"]
        return ctx


class QuestionUpdateView(UpdateView):
    model = StudentEssayAnswer
    template_name = 'exams/question.html'
    # form_class = StudentEssayAnswerForm

    def dispatch(self, request, *args, **kwargs):
        self.exam = Exam.objects.get(id=self.kwargs.get("exam_pk"))
        self.student_exam, created = StudentExam.objects.get_or_create(
            user=self.request.user, exam=self.exam)
        addtime = timedelta(minutes=self.exam.time_quiz)
        finish_time = self.student_exam.created_at + addtime
        if finish_time < timezone.now():
            self.request.session['exam_time_expired'] = True
            return redirect("exam_list")
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        all_questions = get_all_questions(self.kwargs.get("exam_pk"))
        if all_questions[self.kwargs.get("question_pk")]["type"] == "choice_question":
            return StudentChoiceAnswerForm
        else:
            return StudentEssayAnswerForm

    def get_object(self):

        all_questions = get_all_questions(self.exam.id)
        question_content = all_questions[self.kwargs.get("question_pk")]

        # get or create student answer
        answer, created = question_content["answer_model"].objects.get_or_create(
            question=question_content["question"], student_exam=self.student_exam)
        return answer

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        all_questions = get_all_questions(self.exam.id)
        ctx["question_content"] = all_questions[self.kwargs.get("question_pk")]
        ctx["exam"] = self.exam
        ctx["all_questions"] = all_questions
        ctx["exam_time"] = self.exam.time_quiz
        ctx["student_exam"] = self.student_exam
        ctx["question_id"] = self.kwargs.get("question_pk")
        return ctx

    def get_success_url(self):
        all_questions = get_all_questions(self.kwargs.get("exam_pk"))
        question_number = self.kwargs.get("question_pk")
        question = all_questions[question_number]["question"]

        if question_number == len(all_questions):
            question_number = 1
        else:
            question_number += 1

        return reverse_lazy('question', kwargs={'question_pk': question_number,
                                                "exam_pk": self.kwargs.get("exam_pk")})
