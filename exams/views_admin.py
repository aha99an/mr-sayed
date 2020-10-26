from django.shortcuts import (
    get_object_or_404,
    render,
    HttpResponseRedirect)
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, CreateView
from .models import (Exam, EssayQuestion, TrueFalseQuestion, ChoiceQuestion,
                     StudentExam, StudentChoiceAnswer, StudentEssayAnswer)
from classes.models import Class
from .forms import StudentEssayGradingForm, ExamCreateForm, ChoiceQuestionCreateForm, EssayQuestionCreateForm
from django.urls import reverse_lazy
from collections import OrderedDict
from home.permissions import AdminPermission
from django.db.models import Q


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
        else:
            StudentChoiceAnswer.objects.create(
                question=question, student_exam=student_exam)

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
        else:
            StudentEssayAnswer.objects.create(
                question=question, student_exam=student_exam)

        questions[question_index] = {"url": "essay_question",
                                     "type": "essay_question",
                                     "question": question,
                                     "student_answer": student_essay_answer,
                                     "answered": answered,
                                     "answer_model": StudentEssayAnswer}
        question_index += 1

    return questions


class ExamAdminListView(AdminPermission, ListView):
    template_name = "exams/admin-exam-list.html"
    paginate_by = 10

    def get_queryset(self):
        try:
            a = self.request.GET.get('search_value',)
        except KeyError:
            a = None
        q = StudentExam.objects.all()
        if a:

            admin_student_list1 = Q(user__first_name__contains=a)
            admin_student_list2 = Q(user__username__contains=a)
            admin_student_list3 = Q(exam__name__contains=a)
            admin_student_list4 = Q(user__student_class__name__contains=a)
            q = q.filter(admin_student_list1 |
                         admin_student_list2 | admin_student_list3 | admin_student_list4)

        class_filter = self.request.GET.get('class_filter')
        is_checked_filter = self.request.GET.get('is_checked_filter')
        if class_filter:
            q = q.filter(
                user__student_class__name=class_filter)
        if is_checked_filter:
            if is_checked_filter == "True":
                q = q.filter(is_graded=True)
            else:
                q = q.filter(is_graded=False)

        return q

    def get_context_data(self, **kwargs):
        ctx = super(ExamAdminListView, self).get_context_data(**kwargs)
        ctx["classes"] = Class.objects.all()
        ctx["class_filter"] = self.request.GET.get('class_filter')
        ctx["is_checked_filter"] = self.request.GET.get('is_checked_filter')
        ctx["search_value"] = self.request.GET.get('search_value')
        return ctx


class AdminChoiceQuestion(AdminPermission, DetailView):
    template_name = 'exams/admin-question.html'

    def get_object(self):
        self.student_exam_pk = self.kwargs.get("student_exam_pk")
        student_exam = StudentExam.objects.get(id=self.student_exam_pk)
        self.question_pk = self.kwargs.get("question_pk")
        self.all_questions = get_all_questions(
            student_exam.exam.id, student_exam.user)
        if self.question_pk:
            question_content = self.all_questions[self.question_pk]
        else:
            question_content = list(self.all_questions.values())[0]
        print(question_content, "AAAAAAAAAAAAA")
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
        form.instance.is_graded = True
        form.save()
        return HttpResponseRedirect(reverse_lazy('admin_choice_question', kwargs={"student_exam_pk": obj.student_exam.id,
                                                                                  'question_pk': question_pk,
                                                                                  }))

    else:
        return HttpResponseRedirect("/"+student_essay_answer_pk)


class AdminAddExamListView(AdminPermission, ListView):
    template_name = "exams/admin-add-exam-list.html"
    model = Exam


class AdminExamCreateView(AdminPermission, CreateView):
    form_class = ExamCreateForm
    success_url = reverse_lazy('admin_add_exam_list')
    template_name = 'exams/admin-create-exam.html'

    def get_success_url(self):
        question_type = self.request.POST.get("question_type")
        if question_type == "choice":
            return reverse_lazy("admin_create_choice_question", kwargs={"pk": self.object.id})
        elif question_type == "essay":
            return reverse_lazy("admin_create_essay_question", kwargs={"pk": self.object.id})

        return self.success_url


class AdminExamUpdateView(AdminPermission, UpdateView):
    model = Exam
    form_class = ExamCreateForm
    template_name = 'exams/admin-create-exam.html'

    def get_success_url(self):

        question_type = self.request.POST.get("question_type")
        if question_type == "choice":
            return reverse_lazy("admin_create_choice_question", kwargs={"pk": self.object.id})
        elif question_type == "essay":
            return reverse_lazy("admin_create_essay_question", kwargs={"pk": self.object.id})
        else:
            return reverse_lazy('admin_add_exam_list')

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        # essay_question = EssayQuestion.objects
        # ctx
        return ctx


class AdminExamDeleteView(AdminPermission, DeleteView):
    model = Exam
    success_url = reverse_lazy('admin_add_exam_list')


class AdminChoiceQuestionCreateView(AdminPermission, CreateView):
    form_class = ChoiceQuestionCreateForm
    template_name = 'exams/admin-add-question.html'

    def form_valid(self, form):
        form.instance.exam = Exam.objects.filter(
            id=self.kwargs.get("pk")).last()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("admin_update_exam", kwargs={"pk": self.kwargs.get("pk")})


class AdminEssayQuestionCreateView(AdminPermission, CreateView):
    form_class = EssayQuestionCreateForm
    template_name = 'exams/admin-add-question.html'

    def form_valid(self, form):
        form.instance.exam = Exam.objects.filter(
            id=self.kwargs.get("pk")).last()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("admin_update_exam", kwargs={"pk": self.kwargs.get("pk")})


class AdminChoiceQuestionUpdateView(AdminPermission, UpdateView):
    model = ChoiceQuestion
    form_class = ChoiceQuestionCreateForm
    template_name = 'exams/admin-add-question.html'

    def get_success_url(self):
        exam = ChoiceQuestion.objects.get(id=self.kwargs.get("pk")).exam
        return reverse_lazy("admin_update_exam", kwargs={"pk": exam.id})


class AdminEssayQuestionUpdateView(AdminPermission, UpdateView):
    model = EssayQuestion
    form_class = EssayQuestionCreateForm
    template_name = 'exams/admin-add-question.html'

    def get_success_url(self):
        exam = EssayQuestion.objects.get(id=self.kwargs.get("pk")).exam
        return reverse_lazy("admin_update_exam", kwargs={"pk": exam.id})


class AdminChoiceQuestionDeleteView(AdminPermission, DeleteView):
    model = ChoiceQuestion

    def get_success_url(self):
        exam = ChoiceQuestion.objects.get(id=self.kwargs.get("pk")).exam
        return reverse_lazy("admin_update_exam", kwargs={"pk": exam.id})


class AdminEssayQuestionDeleteView(AdminPermission, DeleteView):
    model = EssayQuestion

    def get_success_url(self):
        exam = EssayQuestion.objects.get(id=self.kwargs.get("pk")).exam
        return reverse_lazy("admin_update_exam", kwargs={"pk": exam.id})

class AdminExamForStudentDeleteView(AdminPermission, DeleteView):
    model = StudentExam
    success_url = reverse_lazy('admin_exam_list')