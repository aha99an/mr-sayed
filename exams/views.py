from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import (Exam, EssayQuestion, TrueFalseQuestion, ChoiceQuestion,
                     StudentExam, StudentChoiceAnswer, StudentEssayAnswer)
from collections import OrderedDict
from .forms import StudentChoiceAnswerForm, StudentEssayAnswerForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from datetime import timedelta, datetime
from django.shortcuts import redirect
from django.utils import timezone
from home.permissions import StudentPermission
import json
import collections
from django.forms.models import model_to_dict


def get_all_questions(exam_id, user):
    exam = Exam.objects.get(id=exam_id)
    student_exam = exam.student_exam.filter(user=user).last()

    # get questions
    questions = OrderedDict()
    exam_choice_qs = exam.choice_question.all().order_by("?")
    exam_essay_qs = exam.essay_question.all().order_by("?")
    question_index = 1

    # Choice questions
    for question in exam_choice_qs:
        # question status
        answered = "not answered"
        student_choice_answer = question.student_choice_answer.filter(
            student_exam=student_exam).last()
        if student_choice_answer:
            if student_choice_answer.answer:
                answered = "answered"

        questions[question_index] = {"url": "choice_question",
                                     "type": "choice_question",
                                     "question": question.id,
                                     "answered": answered,
                                     "grade": question.grade
                                     #  "answer_model": StudentChoiceAnswer,
                                     }
        question_index += 1

    for question in exam_essay_qs:
        # question status
        answered = "not answered"
        student_essay_answer = question.student_essay_answer.filter(
            student_exam=student_exam).last()
        if student_essay_answer:
            if student_essay_answer.answer or student_essay_answer.image_answer:
                answered = "answered"

        questions[question_index] = {"url": "essay_question",
                                     "type": "essay_question",
                                     "question": question.id,
                                     "answered": answered,
                                     "grade": question.grade,
                                     #  "answer_model": StudentEssayAnswer
                                     }
        question_index += 1
    return questions


def set_expiry_date(student_exam):
    exam_time = timedelta(minutes=student_exam.exam.time)
    student_exam.expiry_time = student_exam.created_at + exam_time
    student_exam.save()
    return


now = datetime.now()


class ExamListView(StudentPermission, ListView):
    template_name = "exams/exam-list.html"

    def get_queryset(self):
        if self.request.user.student_class.week_day == now.weekday():
            return Exam.objects.filter(week__start__lte=now.date(), week__end__gte=now.date(), is_active=True)
        else:
            return Exam.objects.none()

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        all_exams = []
        exams = self.get_queryset()
        for i in exams:
            answered = "not answered yet"
            if i.student_exam.filter(user=self.request.user):
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
        if self.request.user.is_authenticated is False:
            return redirect('login')
        if self.request.user.student_is_active is False:
            return redirect('home')
        self.exam = Exam.objects.filter(id=self.kwargs.get("exam_pk"),
                                        week__start__lte=now.date(),
                                        week__end__gte=now.date(), is_active=True).last()
        if not self.exam:
            return redirect('exam_list')
        self.student_exam, created = StudentExam.objects.get_or_create(
            user=self.request.user, exam=self.exam)
        if not self.student_exam.expiry_time:
            set_expiry_date(self.student_exam)
        if self.student_exam.expiry_time < timezone.now():
            self.request.session['exam_time_expired'] = True
            return redirect("exam_list")

        # save RANDOM order of questions in student_exam model
        if not self.student_exam.questions:
            self.student_exam.questions = self.all_questions = get_all_questions(
                self.kwargs.get("exam_pk"), self.request.user)
            self.student_exam.save()
            self.student_exam.refresh_from_db()
        self.all_questions = eval(self.student_exam.questions)

        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        # all_questions = get_all_questions(
        #     self.kwargs.get("exam_pk"), self.request.user)
        if self.all_questions[self.kwargs.get("question_pk")]["type"] == "choice_question":
            return StudentChoiceAnswerForm
        else:
            return StudentEssayAnswerForm

    def get_object(self):
        question_content = self.all_questions[self.kwargs.get("question_pk")]

        if question_content["type"] == "choice_question":
            question = ChoiceQuestion.objects.get(
                id=question_content["question"])
            answer, created = StudentChoiceAnswer.objects.get_or_create(
                question=question, student_exam=self.student_exam)
        else:
            question = EssayQuestion.objects.get(
                id=question_content["question"])
            answer, created = StudentEssayAnswer.objects.get_or_create(
                question=question, student_exam=self.student_exam)
        return answer

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        # all_questions = get_all_questions(self.exam.id, self.request.user)
        ctx["question_content"] = self.all_questions[self.kwargs.get(
            "question_pk")]
        ctx["all_questions"] = self.all_questions
        ctx["student_exam"] = self.student_exam
        ctx["question_id"] = self.kwargs.get("question_pk")
        return ctx

    def get_success_url(self):
        question_number = self.kwargs.get("question_pk")
        question = self.all_questions[question_number]["question"]

        if question_number == len(self.all_questions):
            question_number = 1
        else:
            question_number += 1

        return reverse_lazy('question', kwargs={'question_pk': question_number,
                                                "exam_pk": self.kwargs.get("exam_pk")})
