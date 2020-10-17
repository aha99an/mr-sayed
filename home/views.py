from django.views.generic import TemplateView, CreateView
from accounts.models import StudentPayment, CustomUser
from datetime import datetime
from questions.models import MrQuestion


class HomePageView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = datetime.now()
        if self.request.user.is_authenticated:
            payment = StudentPayment.objects.filter(
                user=self.request.user).last()
            if payment:
                if payment.last_lecture_attended:
                    if (now.date() - payment.last_lecture_attended).days >= 0:
                        CustomUser.objects.filter(id=self.request.user.id).update(
                            student_is_active=False)
                if payment.remainder_available_lectures <= 0:
                    CustomUser.objects.filter(id=self.request.user.id).update(
                        student_is_active=False)
            else:
                CustomUser.objects.filter(id=self.request.user.id).update(
                    student_is_active=False)
        return context


class TestView(CreateView):
    template_name = "test/elements.html"
