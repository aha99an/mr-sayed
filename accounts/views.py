from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView
from .forms import CustomUserCreationForm ,MyProfileData
from django.views import generic
from exams.models import Exam, StudentExam, StudentChoiceAnswer, StudentEssayAnswer
from django.db.models import Sum
from django.utils import timezone
from collections import OrderedDict
from homework.models import StudentHomework
from home.permissions import StudentPermission
from datetime import datetime
from .models import CustomUser
from django.shortcuts import redirect

now = datetime.now()


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


class ProfileView(StudentPermission, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        student_exams = StudentExam.objects.filter(user=self.request.user)
        # Check exams, first make sure student exam time is done, then if not graded try grading it
        for student_exam in student_exams:
            if student_exam.expiry_time < timezone.now():
                if not student_exam.is_graded:
                    if student_exam.exam.exam_type == Exam.CHOICE_EXAM:
                        grade_choice_exam(student_exam.id)
                        student_exams = StudentExam.objects.filter(
                            user=self.request.user)
        # Variety Exam
        for student_exam in student_exams:
            if now.date() > student_exam.exam.week.end:
                if not student_exam.is_graded:
                    if student_exam.exam.exam_type == Exam.VARIETY_EXAM:
                        for question in student_exam.student_essay_answer.all():
                            if not question.is_graded:
                                break
                            essay_answers_grade = StudentEssayAnswer.objects.filter(
                                student_exam=student_exam).aggregate(
                                Sum('grade'))["grade__sum"]
                            if student_exam.student_choice_answer.all():
                                choice_answers_grade = StudentChoiceAnswer.objects.filter(
                                    student_exam=student_exam).aggregate(
                                    Sum('grade'))["grade__sum"]
                            else:
                                choice_answers_grade = 0
                            student_exam.grade = essay_answers_grade + choice_answers_grade
                            student_exam.is_graded = True
                            student_exam.save()
        # Exams
        # we will check for l field and make it true in case of we exceeded el end time bta3 el week (7esa)
        for student_exam in student_exams:
            if not student_exam.exam.show_answer:
                if now.date() > student_exam.exam.week.end:
                    student_exam.exam.show_answer = True
                    student_exam.exam.save()

        # we will check for show_answer field and make it true in case of we exceeded el end time bta3 el week (7esa)
        student_homeworks = StudentHomework.objects.filter(
            user=self.request.user)
        for student_homework in student_homeworks:
            if not student_homework.homework.show_answer:
                if now.date() > student_homework.homework.week.end:
                    student_homework.homework.show_answer = True
                    student_homework.homework.save()
        ctx["student_exams"] = student_exams
        ctx["student_homeworks"] = student_homeworks
        return ctx


class ExamQuestionDetailView(StudentPermission, DetailView):
    template_name = 'accounts/profile-exam.html'
    def dispatch(self, request, *args, **kwargs):
        self.student_exam_pk = self.kwargs.get("student_exam_pk")
        student_exam = StudentExam.objects.get(id=self.student_exam_pk)
        if not student_exam.is_graded:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        student_exam = StudentExam.objects.get(id=self.student_exam_pk)
        student_exam.is_graded = True
        student_exam.save()
        self.question_pk = self.kwargs.get("question_pk")
        self.all_questions = get_all_questions(
            student_exam.exam.id, student_exam.user)
        question_content = self.all_questions[self.question_pk]

        return question_content

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["all_questions"] = self.all_questions
        ctx["student_exam_pk"] = self.student_exam_pk
        if self.question_pk:
            ctx["question_pk"] = self.question_pk
        else:
            ctx["question_pk"] = 1
        ctx["student_exam"] = StudentExam.objects.get(id=self.student_exam_pk)
        return ctx


class HomeworkDetailView(StudentPermission, DetailView):
    template_name = 'accounts/profile-homework.html'
    model = StudentHomework

class MyProfileDataUpdateView(StudentPermission, UpdateView):
    template_name = 'accounts/my-profile-data.html'
    model = CustomUser
    success_url = reverse_lazy("profile")
    form_class = MyProfileData

class IsNotActiveTemplateView(TemplateView):
    template_name = 'accounts/is_not_active_students.html'
