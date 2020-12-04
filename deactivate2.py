
import os
from django.core.wsgi import get_wsgi_application
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mr-syed.settings')
application = get_wsgi_application()
from questions.models import MrQuestion
from accounts.models import CustomUser, StudentPayment
from exams.models import Exam, StudentExam, StudentChoiceAnswer
from homework.models import Homework, StudentHomework
from datetime import datetime, timedelta
from django.db.models import Sum
users = CustomUser.objects.filter(student_is_active=True)
now = datetime.now()
one_week_ago = datetime.today() - timedelta(days=7)

for user in users:
    payment = StudentPayment.objects.filter(
        user=user).last()
    if payment:
        if payment.last_lecture_attended:
            if (now.date() - payment.last_lecture_attended).days >= 6 and payment.remainder_available_lectures <= 0:
                user.student_is_active = False
                user.save()
        elif payment.remainder_available_lectures <= 0:
            user.student_is_active = False
            user.save()
    else:
        user.student_is_active = False
        user.save()


@transaction.atomic
def check_all_exams_not_graded():
    student_exams = StudentExam.objects.filter(is_graded=False)
    for student_exam in student_exams:
        student_exam.grade = StudentChoiceAnswer.objects.filter(
            student_exam=student_exam).aggregate(
                Sum('grade'))["grade__sum"]
        student_exam.is_graded = True
        student_exam.save()
check_all_exams_not_graded()


@transaction.atomic
def assign_students_grades_and_homework():
    students = CustomUser.objects.filter(user_type=0)
    exam = Exam.objects.filter(week__start__lte=one_week_ago, week__end__gte=one_week_ago).last()
    if exam:
        for student in students:
            student.examGrade = exam.grade
            studentExam = StudentExam.objects.filter(
                exam=exam, user=student).last()
            if studentExam:
                student.examStudentGrade = studentExam.grade
            else:
                student.examStudentGrade = None
            student.save()

    homework = Homework.objects.filter(week__start__lte=one_week_ago, week__end__gte=one_week_ago).last()
    if homework:
        for student in students:
            studentHomework = StudentHomework.objects.filter(homework=homework, user=student).last()
            # not only viewed the homework but also uploaded files as answers
            if studentHomework and studentHomework.student_homework_file.all():
                student.homeWorkAnswerd = True
            else:
                student.homeWorkAnswerd = False
            student.save()

assign_students_grades_and_homework()
