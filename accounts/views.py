from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm
from django.views import generic
from exams.models import Exam, StudentExam, StudentChoiceAnswer
from django.db.models import Sum
from django.utils import timezone


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
