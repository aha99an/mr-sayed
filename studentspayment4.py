
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mr-syed.settings')
application = get_wsgi_application()

from accounts.models import CustomUser, StudentPayment
from datetime import datetime


users = CustomUser.objects.filter(student_is_active=True)
now = datetime.now()
for user in users:
    StudentPayment.objects.create(user=user, number_available_lectures=4, paid_at=now.date(), notes="")
    payment = StudentPayment.objects.filter(
        user=user).last()
