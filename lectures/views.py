from django.views.generic import ListView, UpdateView, DetailView
from .models import Lecture, StudentLecture, StudentLectureQuestion


class LectureListView(ListView):
    model = Lecture
    template_name = "lectures/lecture-list.html"

    # def get_queryset(self):
    #     return Homework.objects.all()

    # def get_context_data(self, *args, **kwargs):
    #     ctx = super().get_context_data(*args, **kwargs)
    #     all_homeworks = []
    #     # homeworks = self.get_queryset()
    #     # for i in homeworks:
    #     #     answered = "not answered yet"
    #     #     if i.student_homework.get(user=self.request.user).student_homework_file.all():
    #     #         answered = "answered"
    #     #     all_homeworks.append({"homework": i,
    #     #                           "answered": answered})
    #     ctx["lecture"] = Lecture.objects.last()
    #     return ctx


class LectureDetailView(DetailView):
    model = Lecture
    template_name = "lectures/lecture.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        lecture = Lecture.objects.get(id=self.kwargs["pk"])
        ctx["links"] = lecture.lecture_link.all()
        return ctx
