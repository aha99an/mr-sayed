from django.contrib import admin
from .models import (Homework, StudentHomework,
                     StudentHomeworkFile)

admin.site.register(Homework)
admin.site.register(StudentHomework)
admin.site.register(StudentHomeworkFile)
