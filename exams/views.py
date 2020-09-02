from django.views.generic import ListView, DetailView
from .models import Exam, EssayQuestion, TrueFalseQuestion, ChoiceQuestion
from collections import OrderedDict

class TrainingListView(ListView):
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
