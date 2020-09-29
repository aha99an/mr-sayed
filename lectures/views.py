from django.views.generic import ListView, UpdateView, DetailView
from .models import Lecture, StudentLecture, StudentLectureQuestion
from home.permissions import StudentPermission
from accounts.models import CustomUser
from django.shortcuts import redirect
import datetime

def check_lecture_time(user):
    now = datetime.datetime.now()
    student_class = user.student_class
    today = datetime.date.today()
    now_minus_start_minutes = (datetime.datetime.combine(today, now.time())\
                               - datetime.datetime.combine(today, student_class.start)).total_seconds() / 60
    return now_minus_start_minutes

class LectureListView(StudentPermission, ListView):
    template_name = "lectures/lecture-list.html"

    def get_queryset(self):
        now = datetime.datetime.now()
        student_class = self.request.user.student_class
        if student_class.week_day == now.weekday() and student_class.start < now.time():
            now_minus_start_minutes = check_lecture_time(self.request.user)
            return Lecture.objects.filter(week__start__lte=now.date(),
                                          week__end__gte=now.date(),
                                          lecture_allowed_time__gte=now_minus_start_minutes)
        else:
            return Lecture.objects.none()

class LectureDetailView(StudentPermission, DetailView):
    model = Lecture
    template_name = "lectures/lecture.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.object = Lecture.objects.filter(id=kwargs.get('pk')).last()
            now = datetime.datetime.now()
            student_class = self.request.user.student_class
            
            if student_class.week_day == now.weekday() and student_class.start < now.time():
                now_minus_start_minutes = check_lecture_time(self.request.user)
                if self.object.lecture_allowed_time > now_minus_start_minutes:
                    return super().dispatch(request, *args, **kwargs)

        return redirect("lectures_list")

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        lecture = Lecture.objects.get(id=self.kwargs["pk"])
        ctx["links"] = lecture.lecture_link.all()
        return ctx
