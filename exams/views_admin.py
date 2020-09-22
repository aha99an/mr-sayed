from django.shortcuts import (
    get_object_or_404,
    render,
    HttpResponseRedirect)
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, FormView
from .models import (Exam, EssayQuestion, TrueFalseQuestion, ChoiceQuestion,
                     StudentExam, StudentChoiceAnswer, StudentEssayAnswer)
from classes.models import Class
from .forms import StudentEssayGradingForm
from django.urls import reverse_lazy
from collections import OrderedDict


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
        answer = ""
        student_choice_answer = question.student_choice_answer.filter(
            student_exam=student_exam).last()
        if student_choice_answer:
            if student_choice_answer.answer:
                answer = student_choice_answer.answer

        questions[question_index] = {"url": "choice_question",
                                     "type": "choice_question",
                                     "question": question,
                                     "answered": answer,
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
                                     "student_answer": student_essay_answer,
                                     "answered": answered,
                                     "answer_model": StudentEssayAnswer}
        question_index += 1

    return questions


class ExamAdminListView(ListView):
    template_name = "exams/admin-exam-list.html"

    def get_queryset(self):
        queryset = StudentExam.objects.all()
        class_filter = self.request.GET.get('class_filter')
        is_checked_filter = self.request.GET.get('is_checked_filter')
        if class_filter:
            queryset = queryset.filter(
                user__student_class__name=class_filter)
        if is_checked_filter:
            if is_checked_filter == "True":
                queryset = queryset.filter(is_graded=True)
            else:
                queryset = queryset.filter(is_graded=False)

        return queryset

    def get_context_data(self, **kwargs):
        ctx = super(ExamAdminListView, self).get_context_data(**kwargs)
        ctx["classes"] = Class.objects.all()
        ctx["class_filter"] = self.request.GET.get('class_filter')
        ctx["is_checked_filter"] = self.request.GET.get('is_checked_filter')

        return ctx


class AdminChoiceQuestion(DetailView):
    template_name = 'exams/admin-question.html'

    def get_object(self):
        self.student_exam_pk = self.kwargs.get("student_exam_pk")
        student_exam = StudentExam.objects.get(id=self.student_exam_pk)
        student_exam.is_graded = True
        student_exam.save()
        self.question_pk = self.kwargs.get("question_pk")
        self.all_questions = get_all_questions(
            student_exam.exam.id, student_exam.user)
        if self.question_pk:
            question_content = self.all_questions[self.question_pk]

        else:
            question_content = list(self.all_questions.values())[0]

        return question_content

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["all_questions"] = self.all_questions
        ctx["student_exam_pk"] = self.student_exam_pk
        ctx["form"] = StudentEssayGradingForm
        if self.question_pk:
            ctx["question_pk"] = self.question_pk
        else:
            ctx["question_pk"] = 1
        return ctx


def update_view(request, student_essay_answer_pk, question_pk):

    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(StudentEssayAnswer, id=student_essay_answer_pk)
    question_id = obj.question.id
    # pass the object as instance in form
    form = StudentEssayGradingForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse_lazy('admin_choice_question', kwargs={"student_exam_pk": obj.student_exam.id,
                                                                                  'question_pk': question_pk,
                                                                                  }))

    else:
        return HttpResponseRedirect("/"+student_essay_answer_pk)

class AdminAddExamListView(ListView):
    template_name = "exams/admin-add-exam-list.html"
    model = Exam