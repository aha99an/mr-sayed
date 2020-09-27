from django.views.generic import ListView, UpdateView, DetailView
from .models import Lecture, StudentLecture, StudentLectureQuestion
from home.permissions import StudentPermission


class LectureListView(StudentPermission, ListView):
    model = Lecture
    template_name = "lectures/lecture-list.html"


class LectureDetailView(StudentPermission, DetailView):
    model = Lecture
    template_name = "lectures/lecture.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        lecture = Lecture.objects.get(id=self.kwargs["pk"])
        ctx["links"] = lecture.lecture_link.all()
        return ctx
