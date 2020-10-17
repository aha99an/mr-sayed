

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mr-syed.settings')
application = get_wsgi_application()
from accounts.models import CustomUser
from classes.models import Class
from exams.models import StudentExamMakeup, Exam
# id =16

users = CustomUser.objects.filter(student_is_active=True)
exam = Exam.objects.get(id=16)
for user in users:
    StudentExamMakeup.objects.create(user=user, exam=exam)
