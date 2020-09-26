from django.views.generic import ListView, UpdateView, CreateView
from .models import Lecture, StudentLecture, StudentLectureQuestion
from .forms import LectureCreateForm
from django.urls import reverse_lazy


class AdminLectureListView(ListView):
    model = Lecture
    template_name = "lectures/admin-lecture-list.html"


class AdminLectureCreateView(CreateView):
    template_name = "lectures/admin-lecture-create.html"
    form_class = LectureCreateForm
    success_url = reverse_lazy("admin_lectures_list")

    def form_valid(self, form):
        print(self.request.POST)
        print(self.request.POST.getlist("lecture_links"))
        # print(form.instance)
        # # form.instance.exam = Exam.objects.filter(
        # #     id=self.kwargs.get("pk")).last()
        # print(form.name)
        return super().form_valid(form)
