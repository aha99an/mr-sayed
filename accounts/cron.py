# python manage.py crontab add
from questions.models import MrQuestion
from accounts.models import CustomUser, StudentPayment
from datetime import datetime


def deactivate_users():
    users = CustomUser.objects.filter(student_is_active=True)
    now = datetime.now()
    for user in users:
        payment = StudentPayment.objects.filter(
            user=user).last()
        if payment:
            if payment.last_lecture_attended:
                if (now.date() - payment.last_lecture_attended).days >= 0 and payment.remainder_available_lectures <= 0:
                    user.student_is_active = False
            if payment.remainder_available_lectures <= 0:
                user.student_is_active = False
        else:
            user.student_is_active = False
        user.save()
