
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mr-syed.settings')
application = get_wsgi_application()
from accounts.models import CustomUser, StudentPayment
from datetime import datetime




users = CustomUser.objects.filter(student_is_active=True)
now = datetime.now()
for user in users:
    payment = StudentPayment.objects.filter(
        user=user).last()
    if payment:
        if payment.last_lecture_attended:
            if (now.date() - payment.last_lecture_attended).days >= 0:
                user.student_is_active = False
        if payment.remainder_available_lectures <= 0:
            user.student_is_active = False
    else:
        user.student_is_active = False
    user.save()
    MrQuestion.objects.create(user=CustomUser.objects.last(),
                              question=user.id
                              )
