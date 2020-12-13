from django.views.generic import ListView, UpdateView, DetailView

from .models import Lecture, StudentLecture, StudentLectureQuestion, StudentLectureMakeup, StudentLecture

from home.permissions import StudentPermission
from accounts.models import CustomUser, StudentPayment
from django.shortcuts import redirect
import datetime
from django.utils import timezone
import logging

logger = logging.getLogger('requests')


now = datetime.datetime.now()
def check_lecture_time(user):
    # now = datetime.datetime.now()
    student_class = user.student_class
    today = datetime.date.today()
    now_minus_start_minutes = (datetime.datetime.combine(today, now.time())
                               - datetime.datetime.combine(today, student_class.start)).total_seconds() / 60
    return now_minus_start_minutes

def is_makeup_lecture_expired(student_lecture):
    # now = datetime.datetime.now()
    today = datetime.date.today()
    student_lecture_time_diff = (datetime.datetime.combine(today, now.time())
                               - datetime.datetime.combine(today, student_lecture.seen_at.time())).total_seconds() / 60
    return False if student_lecture_time_diff < student_lecture.lecture.lecture_allowed_time else True

class LectureListView(StudentPermission, ListView):
    template_name = "lectures/lecture-list.html"

    def get_queryset(self):
        # now = datetime.datetime.now()
        student_class = self.request.user.student_class
        queryset = Lecture.objects.none()

        # permenant lectures
        queryset |= Lecture.objects.filter(is_permanent=True)

        # Makeup lectures
        mackup_lectures = StudentLectureMakeup.objects.filter(
            user=self.request.user)
        if mackup_lectures:
            for lecture in mackup_lectures:
                mackup_student_lecture = StudentLecture.objects.filter(lecture=lecture.lecture, user=self.request.user).last()
                if mackup_student_lecture and mackup_student_lecture.seen_at is not None:
                    if not is_makeup_lecture_expired(mackup_student_lecture):
                        queryset |= Lecture.objects.filter(id=lecture.lecture.id)
                else:
                    queryset |= Lecture.objects.filter(id=lecture.lecture.id)
        # lectures
        logger.debug("user:{}, student_class.start:{}, now.time:{}, check_lecture_time:{}".format(self.request.user,
                                                                                                  student_class.start,
                                                                                                  now.time(),
                                                                                                  check_lecture_time(self.request.user)
                                                                                                  ))
        if student_class.week_day == now.weekday() and student_class.start < now.time():
            now_minus_start_minutes = check_lecture_time(self.request.user)
            queryset |= Lecture.objects.filter(week__start__lte=now.date(),
                                               week__end__gte=now.date(),
                                               lecture_allowed_time__gte=now_minus_start_minutes)

        return queryset


class LectureDetailView(StudentPermission, DetailView):
    model = Lecture
    template_name = "lectures/lecture.html"

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            self.object = Lecture.objects.filter(id=kwargs.get('pk')).last()
            # now = datetime.datetime.now()
            student_class = self.request.user.student_class

            def handle_student_payment():
                payment = StudentPayment.objects.filter(
                    user=self.request.user, remainder_available_lectures__gte=1).first()
                if payment:
                    student_lecture, created = StudentLecture.objects.get_or_create(
                        user=request.user, lecture=self.object)
                    if created:
                        # subtract from remainder_available_lectures and get date if last lecture
                        payment.remainder_available_lectures -= 1
                        if payment.remainder_available_lectures == 0:
                            payment.last_lecture_attended = now.date()
                        payment.save()
                        # save student payment in lecture class
                        student_lecture.student_payment = payment
                        student_lecture.seen_at = now
                        student_lecture.save()
                    else:
                        if student_lecture.seen_at is None:
                            student_lecture.seen_at = now
                            student_lecture.save()
                    return True
                else:
                    if StudentLecture.objects.filter(user=request.user, lecture=self.object):
                        return True
                    else:
                        return False
            # Permenant Lecture
            if self.object.is_permanent:
                return super().dispatch(request, *args, **kwargs)

            # Makeup Lecture
            student_makeup_lecture = StudentLectureMakeup.objects.filter(user=self.request.user, lecture=self.object).last()
            if student_makeup_lecture:
                mackup_student_lecture = StudentLecture.objects.filter(lecture=self.object, user=self.request.user).last()
                # subtract one from the avilable lecture to student
                if mackup_student_lecture:
                    # check seen_at time if not exist then it is the first time student watches the lecture
                    if mackup_student_lecture.seen_at is not None:
                        if not is_makeup_lecture_expired(mackup_student_lecture):
                            return super().dispatch(request, *args, **kwargs)
                    else:
                        mackup_student_lecture.seen_at = now
                        mackup_student_lecture.save()
                        return super().dispatch(request, *args, **kwargs)
                else:
                    if handle_student_payment():
                        return super().dispatch(request, *args, **kwargs)

            if student_class.week_day == now.weekday() and student_class.start <= now.time():
                now_minus_start_minutes = check_lecture_time(self.request.user)
                if self.object.lecture_allowed_time > now_minus_start_minutes and now.date() <= self.object.week.end:
                    # subtract one from the avilable lecture to student
                    handle_student_payment()
                    return super().dispatch(request, *args, **kwargs)

        return redirect("lectures_list")

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        lecture = Lecture.objects.get(id=self.kwargs["pk"])
        ctx["links"] = lecture.lecture_link.all()
        return ctx
