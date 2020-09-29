from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from .models import Lecture, StudentLecture, StudentLectureQuestion, LectureLink
from .forms import LectureCreateForm
from django.urls import reverse_lazy
from home.permissions import AdminPermission


class AdminLectureListView(AdminPermission, ListView):
    model = Lecture
    template_name = "lectures/admin-lecture-list.html"


class AdminLectureCreateView(AdminPermission, CreateView):
    template_name = "lectures/admin-lecture-create.html"
    form_class = LectureCreateForm
    success_url = reverse_lazy("admin_lectures_list")

    def get_success_url(self):
        lecture_links = self.request.POST.getlist("lecture_links")
        if lecture_links:
            for link in lecture_links:
                if link != "":
                    LectureLink.objects.create(link=link, lecture=self.object)
        return self.success_url


class AdminLectureUpdateView(AdminPermission, UpdateView):
    template_name = "lectures/admin-lecture-update.html"
    form_class = LectureCreateForm
    success_url = reverse_lazy("admin_lectures_list")
    model = Lecture

    def form_valid(self, form):
        lecture_links = self.request.POST.getlist("lecture_links")
        if lecture_links:
            for link in lecture_links:
                if link != "":
                    LectureLink.objects.create(link=link, lecture=self.object)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["links"] = LectureLink.objects.filter(lecture=self.object)
        return context


class AdminLectureDeleteView(AdminPermission, DeleteView):
    model = Lecture

    def get_success_url(self):
        return reverse_lazy("admin_lectures_list")


class AdminLectureLinkDeleteView(AdminPermission, DeleteView):
    model = LectureLink

    def get_success_url(self):
        return reverse_lazy("update_lecture",
                            kwargs={"pk": Lecture.objects.filter(lecture_link=self.object).last().id})
