from django.views.generic import ListView, UpdateView, DetailView

from .models import Lecture, StudentLecture, StudentLectureQuestion, StudentLectureMakeup, StudentLecture
from exams.models import Exam, StudentExam
from home.permissions import StudentPermission
from accounts.models import CustomUser, StudentPayment
from django.shortcuts import redirect
import datetime
from django.utils import timezone
from home.models import Test
import logging

# logger = logging.getLogger('requests')

# check if student solved the exam first
def check_week_exam(week, user):
    # week = self.object.week
    exam = Exam.objects.filter(week=week).last()
    student_exam = ''
    if exam:
        student_exam = StudentExam.objects.filter(exam=exam, user=user).last()
    if student_exam:
        return True
    return False

def check_lecture_time(user):
    now = datetime.datetime.now()
    student_class = user.student_class
    today = datetime.date.today()
    now_minus_start_minutes = (datetime.datetime.combine(today, now.time())
                               - datetime.datetime.combine(today, student_class.start)).total_seconds() / 60
    return now_minus_start_minutes

def is_makeup_lecture_expired(student_lecture):
    now = datetime.datetime.now()
    today = datetime.date.today()
    student_lecture_time_diff = (datetime.datetime.combine(today, now.time())
                               - datetime.datetime.combine(today, student_lecture.seen_at.time())).total_seconds() / 60
    return False if student_lecture_time_diff < student_lecture.lecture.lecture_allowed_time else True

class LectureListView(StudentPermission, ListView):
    template_name = "lectures/lecture-list.html"

    def get_queryset(self):
        user = self.request.user
        now = datetime.datetime.now()
        student_class = user.student_class
        queryset = Lecture.objects.none()

        # permenant lectures
        queryset |= Lecture.objects.filter(is_permanent=True)

        # Makeup lectures
        mackup_lectures = StudentLectureMakeup.objects.filter(
            user=user)
        if mackup_lectures:
            for lecture in mackup_lectures:
                mackup_student_lecture = StudentLecture.objects.filter(lecture=lecture.lecture, user=user).last()
                if mackup_student_lecture and mackup_student_lecture.seen_at is not None:
                    if not is_makeup_lecture_expired(mackup_student_lecture):
                        queryset |= Lecture.objects.filter(id=lecture.lecture.id)
                else:
                    queryset |= Lecture.objects.filter(id=lecture.lecture.id)
        # lectures
        logger = logging.getLogger('testlogger')
        logger.info('This is a simple log message')
        # logger.debug("user:{}, student_class.start:{}, now.time:{}, check_lecture_time:{}".format(user,
        #                                                                                           student_class.start,
        #                                                                                           now.time(),
        #                                                                                           check_lecture_time(user)
        #                                                                                           ))
        # Test.objects.create(logger="user:{}, student_class.start:{}, now.time:{}, check_lecture_time:{}".format(user,
        #                                                                                           student_class.start,
        #                                                                                           now.time(),
        #                                                                                           check_lecture_time(user)
        #                                                                                           ))
        if student_class.start < now.time():
            # now_minus_start_minutes = check_lecture_time(user)
            lectures_pass_now_date = Lecture.objects.filter(week__start__lte=now.date())
            lectures_ids = []
            for lecture in lectures_pass_now_date:
                if check_week_exam(lecture.week, user):
                    lectures_ids.append(lecture.id)
            queryset |= Lecture.objects.filter(id__in=lectures_ids)

        return queryset

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs) 
        if self.request.session.get('exam_not_answered_4_lecture'):
            ctx["exam_not_answered_4_lecture"] = True
            del self.request.session["exam_not_answered_4_lecture"]
        return ctx


class LectureDetailView(StudentPermission, DetailView):
    model = Lecture
    template_name = "lectures/lecture.html"

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        self.object = Lecture.objects.filter(id=kwargs.get('pk')).last()
        week = self.object.week

        if user.is_authenticated:
            now = datetime.datetime.now()
            student_class = user.student_class

            def handle_student_payment():
                payment = StudentPayment.objects.filter(
                    user=user, remainder_available_lectures__gte=1).first()
                if payment:
                    student_lecture, created = StudentLecture.objects.get_or_create(
                        user=user, lecture=self.object)
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
                    if StudentLecture.objects.filter(user=user, lecture=self.object):
                        return True
                    else:
                        return False
            # Permenant Lecture
            if self.object.is_permanent:
                return super().dispatch(request, *args, **kwargs)
            # Makeup Lecture
            student_makeup_lecture = StudentLectureMakeup.objects.filter(user=user, lecture=self.object).last()
            if student_makeup_lecture:
                mackup_student_lecture = StudentLecture.objects.filter(lecture=self.object, user=user).last()
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
                    if check_week_exam(week, user):
                        student_lecture = StudentLecture.objects.create(
                            user=user, lecture=self.object)
                        # payment = StudentPayment.objects.filter(
                        #     user=user, remainder_available_lectures__gte=0).first()
                        # student_lecture.student_payment = payment
                        student_lecture.seen_at = now
                        student_lecture.save()
                        # first time to enter this mackup lecture
                        # if handle_student_payment():
                        return super().dispatch(request, *args, **kwargs)

            if now.date() >= self.object.week.start:
                # now_minus_start_minutes = check_lecture_time(user)
                # if self.object.lecture_allowed_time > now_minus_start_minutes and :
                if check_week_exam(week, user):
                    # subtract one from the avilable lecture to student
                    # handle_student_payment()
                    return super().dispatch(request, *args, **kwargs)
        if not check_week_exam(week, user):
            self.request.session['exam_not_answered_4_lecture'] = True 
        return redirect("lectures_list")

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        lecture = Lecture.objects.filter(id=self.kwargs["pk"]).last()
        ctx["links"] = lecture.lecture_link.all()
        return ctx
