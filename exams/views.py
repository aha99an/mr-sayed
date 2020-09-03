from django.views.generic import ListView, DetailView, CreateView
from .models import Exam, EssayQuestion, TrueFalseQuestion, ChoiceQuestion, StudentExam
from collections import OrderedDict
from .forms import StudentChoiceAnswerForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


class ExamListView(ListView):
    model = Exam
    template_name = "exams/exam-list.html"

    def get_queryset(self):
        return Exam.objects.filter(is_active=True)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["something"] = "something"
    #     return context


class ExamDetailView(DetailView):
    model = Exam
    template_name = "exams/exam.html"

    def get_context_data(self, **kwargs):
        exam = self.get_object()
        context = super().get_context_data(**kwargs)
        choice_qs = ChoiceQuestion.objects.filter(exam=exam)
        essay_qs = EssayQuestion.objects.filter(exam=exam)
        true_false_qs = TrueFalseQuestion.objects.filter(exam=exam)
        choice_qs_dict = OrderedDict()
        choice_essay_dict = OrderedDict()
        true_false_qs_dict = OrderedDict()

        question_number = 1

        for q in range(choice_qs.count()):
            choice_qs_dict[str(question_number)] = choice_qs[q]
            question_number = question_number + 1
        for q in range(essay_qs.count()):
            choice_essay_dict[str(question_number)] = essay_qs[q]
            question_number = question_number + 1
        for q in range(true_false_qs.count()):
            true_false_qs_dict[str(question_number)] = true_false_qs[q]
            question_number = question_number + 1

        context["choice_qs"] = choice_qs_dict
        context["essay_qs"] = choice_essay_dict
        context["true_false_qs"] = true_false_qs_dict
        return context


class ChoiceQuestionCreateView(CreateView):
    template_name = 'exams/choice-question.html'
    form_class = StudentChoiceAnswerForm

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["question"] = ChoiceQuestion.objects.get(id=self.kwargs.get(
            "question_pk"), exam__id=self.kwargs.get("exam_pk"))
        return ctx

    def get_success_url(self):
        # if self.request.method =="POST":
        #         print ("hereeeeeeeeeeeeeeeeeeeeeeeeee")
        #         formo = self.ExampleFormSet(self.request.POST)
        #         instances = formo.save(commit=False)
        #         for instance in instances:
        #                 instance.save()
        return reverse_lazy('home:home')

    def form_valid(self, form):
        print("HEIILOLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
        self.object = form.save(commit=False)
        print(self.object)
        self.object.question = ChoiceQuestion.objects.get(id=self.kwargs.get(
            "question_pk"), exam__id=self.kwargs.get("exam_pk"))
        self.object.student_exam = StudentExam.objects.get(
            user=self.request.user, exam__id=self.kwargs.get("exam_pk"))
        self.object.save()

        # do something with self.object
        # remember the import: from django.http import HttpResponseRedirect
        return HttpResponseRedirect(self.get_success_url())
