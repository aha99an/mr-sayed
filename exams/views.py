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
        all_exams = OrderedDict()
        exams = Exam.objects.filter(is_active=True)
        for i in exams:
            answered = "not answered yet"
            if i.student_exam.all():
                answered = "answered"
            all_exams["exam"] = {"exam": i,
                                 "answered": answered}
        ctx["exams"] = all_exams
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
            return redirect("exam_list")
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        all_questions = get_all_questions(self.kwargs.get("exam_pk"))
        if all_questions[self.kwargs.get("question_pk")]["type"] == "choice_question":
            return StudentChoiceAnswerForm
        else:
            return StudentEssayAnswerForm

    def get_object(self):

        exam = Exam.objects.get(id=self.kwargs.get("exam_pk"))
        all_questions = get_all_questions(exam.id)
        question_content = all_questions[self.kwargs.get("question_pk")]

        # get or create student answer
        answer, created = question_content["answer_model"].objects.get_or_create(
            question=question_content["question"], student_exam=self.student_exam)
        return answer

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        exam = Exam.objects.get(id=self.kwargs.get("exam_pk"))
        all_questions = get_all_questions(exam.id)
        ctx["question_content"] = all_questions[self.kwargs.get("question_pk")]
        ctx["exam"] = exam
        ctx["all_questions"] = all_questions
        ctx["exam_time"] = exam.time_quiz
        ctx["student_exam"] = self.student_exam
        ctx["question_id"] = self.kwargs.get("question_pk")

        return ctx

    # def get_context_data(self, *args, **kwargs):
    #     ctx = super().get_context_data(*args, **kwargs)
    #     ctx["question"] = ChoiceQuestion.objects.get(id=self.kwargs.get(
    #         "question_pk"), exam__id=self.kwargs.get("exam_pk"))
    #     return ctx

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


# class ChoiceQuestionUpdateView(UpdateView):
#     # model = StudentChoiceAnswer
#     template_name = 'exams/essay-question.html'
#     form_class = StudentChoiceAnswerForm

#     def get_object(self):
#         exam = Exam.objects.get(id=self.kwargs.get("exam_pk"))
#         all_questions = get_all_questions(exam.id)
#         question = all_questions[self.kwargs.get("question_pk")]["question"]
#         student_exam, created = StudentExam.objects.get_or_create(
#             user=self.request.user, exam=exam)
#         answer, created = StudentChoiceAnswer.objects.get_or_create(
#             question=question, student_exam=student_exam, )

#         return answer

#     def form_valid(self, form):
#         return super().form_valid(form)

#     def get_context_data(self, *args, **kwargs):
#         ctx = super().get_context_data(*args, **kwargs)
#         exam = Exam.objects.get(id=self.kwargs.get("exam_pk"))
#         all_questions = get_all_questions(exam.id)
#         ctx["question_content"] = all_questions[self.kwargs.get("question_pk")]
#         ctx["exam"] = exam
#         ctx["all_questions"] = all_questions
#         return ctx

#     def get_success_url(self):
#         all_questions = get_all_questions(self.kwargs.get("exam_pk"))
#         question_number = self.kwargs.get("question_pk")
#         question = all_questions[question_number]["question"]

#         if question_number == len(all_questions):
#             question_number = 1
#         else:
#             question_number += 1

#         return reverse_lazy(all_questions[question_number]["type"], kwargs={'question_pk': question_number, "exam_pk": self.kwargs.get("exam_pk")})


# class ExamDetailView(DetailView):
#     model = Exam
#     template_name = "exams/exam.html"

#     def get_context_data(self, **kwargs):
#         exam = self.get_object()
#         context = super().get_context_data(**kwargs)
#         choice_qs = ChoiceQuestion.objects.filter(exam=exam)
#         essay_qs = EssayQuestion.objects.filter(exam=exam)
#         true_false_qs = TrueFalseQuestion.objects.filter(exam=exam)
#         choice_qs_dict = OrderedDict()
#         choice_essay_dict = OrderedDict()
#         true_false_qs_dict = OrderedDict()

#         question_number = 1

#         for q in range(choice_qs.count()):
#             choice_qs_dict[str(question_number)] = choice_qs[q]
#             question_number = question_number + 1
#         for q in range(essay_qs.count()):
#             choice_essay_dict[str(question_number)] = essay_qs[q]
#             question_number = question_number + 1
#         for q in range(true_false_qs.count()):
#             true_false_qs_dict[str(question_number)] = true_false_qs[q]
#             question_number = question_number + 1

#         context["choice_qs"] = choice_qs_dict
#         context["essay_qs"] = choice_essay_dict
#         context["true_false_qs"] = true_false_qs_dict
#         return context
