from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import (Exam, EssayQuestion, TrueFalseQuestion, ChoiceQuestion,
                     StudentExam, StudentChoiceAnswer, StudentEssayAnswer)
from collections import OrderedDict
from .forms import StudentChoiceAnswerForm, StudentEssayAnswerForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.shortcuts import redirect
from django.utils import timezone
from home.permissions import StudentPermission


def get_all_questions(exam_id, user):
    exam = Exam.objects.get(id=exam_id)
    student_exam = exam.student_exam.filter(user=user).last()

    # get questions
    questions = OrderedDict()
    exam_choice_qs = exam.choice_question.all()
    exam_essay_qs = exam.essay_question.all()
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
                                     "question": question,
                                     "answered": answered,
                                     "answer_model": StudentChoiceAnswer,
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
                                     "question": question,
                                     "answered": answered,
                                     "answer_model": StudentEssayAnswer}
        question_index += 1

    return questions


def set_expiry_date(student_exam):
    exam_time = timedelta(minutes=student_exam.exam.time)
    student_exam.expiry_time = student_exam.created_at + exam_time
    student_exam.save()
    return


class ExamListView(StudentPermission, ListView):
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
        if self.request.user.student_is_active is False:
            return redirect('login')
        self.exam = Exam.objects.get(id=self.kwargs.get("exam_pk"))
        self.student_exam, created = StudentExam.objects.get_or_create(
            user=self.request.user, exam=self.exam)
        if not self.student_exam.expiry_time:
            set_expiry_date(self.student_exam)
        if self.student_exam.expiry_time < timezone.now():
            self.request.session['exam_time_expired'] = True
            return redirect("exam_list")
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        all_questions = get_all_questions(
            self.kwargs.get("exam_pk"), self.request.user)
        if all_questions[self.kwargs.get("question_pk")]["type"] == "choice_question":
            return StudentChoiceAnswerForm
        else:
            return StudentEssayAnswerForm

    def get_object(self):

        all_questions = get_all_questions(self.exam.id, self.request.user)
        question_content = all_questions[self.kwargs.get("question_pk")]

        # get or create student answer
        answer, created = question_content["answer_model"].objects.get_or_create(
            question=question_content["question"], student_exam=self.student_exam)
        return answer

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        all_questions = get_all_questions(self.exam.id, self.request.user)
        ctx["question_content"] = all_questions[self.kwargs.get("question_pk")]
        ctx["exam"] = self.exam
        ctx["all_questions"] = all_questions
        ctx["exam_time"] = self.exam.time
        ctx["student_exam"] = self.student_exam
        ctx["question_id"] = self.kwargs.get("question_pk")
        return ctx

    def get_success_url(self):
        all_questions = get_all_questions(
            self.kwargs.get("exam_pk"), self.request.user)
        question_number = self.kwargs.get("question_pk")
        question = all_questions[question_number]["question"]

        if question_number == len(all_questions):
            question_number = 1
        else:
            question_number += 1

        return reverse_lazy('question', kwargs={'question_pk': question_number,
                                                "exam_pk": self.kwargs.get("exam_pk")})
