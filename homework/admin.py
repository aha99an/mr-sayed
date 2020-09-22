from django.contrib import admin
from .models import (Homework, HomeworkFile, StudentHomework,
                     StudentHomeworkFile)

admin.site.register(Homework)
admin.site.register(HomeworkFile)
admin.site.register(StudentHomework)
admin.site.register(StudentHomeworkFile)
