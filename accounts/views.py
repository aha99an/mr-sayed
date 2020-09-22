from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView
from .forms import CustomUserCreationForm
from django.views import generic
from exams.models import Exam, StudentExam, StudentChoiceAnswer, StudentEssayAnswer
from django.db.models import Sum
from django.utils import timezone
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
                answer = student_choice_answer

        questions[question_index] = {"url": "choice_question",
                                     "type": "choice_question",
                                     "question": question,
                                     "answer": answer,
                                     "answer_model": StudentChoiceAnswer,
                                     }
        question_index += 1

    for question in exam_essay_qs:
        # question status
        answer = ""
        student_essay_answer = question.student_essay_answer.last()
        print(question)
        print(student_essay_answer)
        if student_essay_answer:
            if student_essay_answer.answer or student_essay_answer.image_answer:
                answer = student_essay_answer

        questions[question_index] = {"url": "essay_question",
                                     "type": "essay_question",
                                     "question": question,
                                     "answer": answer,
                                     "answer_model": StudentEssayAnswer}
        question_index += 1

    return questions


def grade_choice_exam(student_exam_id):
    student_exam = StudentExam.objects.get(id=student_exam_id)
    student_exam.grade = StudentChoiceAnswer.objects.filter(
        student_exam=student_exam).aggregate(
            Sum('grade'))["grade__sum"]
    student_exam.is_graded = True
    student_exam.save()
    return


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        # Exams
        student_exams = StudentExam.objects.filter(user=self.request.user)
        for student_exam in student_exams:
            if student_exam.expiry_time < timezone.now():
                if not student_exam.is_graded:
                    if student_exam.exam.exam_type == Exam.CHOICE_EXAM:
                        grade_choice_exam(student_exam.id)
                        student_exams = StudentExam.objects.filter(
                            user=self.request.user)

        ctx["student_exams"] = student_exams
        return ctx


class ExamQuestionDetailView(DetailView):
    template_name = 'accounts/profile-exam.html'

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
        print(question_content)
        return question_content

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["all_questions"] = self.all_questions
        ctx["student_exam_pk"] = self.student_exam_pk
        if self.question_pk:
            ctx["question_pk"] = self.question_pk
        else:
            ctx["question_pk"] = 1
        return ctx
