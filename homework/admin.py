from django.contrib import admin
from .models import (Homework, HomeworkFile, HomeworkAnswerFile, StudentHomework,
                     StudentHomeworkFile, HomeworkNotebook)

admin.site.register(Homework)
admin.site.register(HomeworkFile)
admin.site.register(HomeworkAnswerFile)
admin.site.register(StudentHomework)
admin.site.register(StudentHomeworkFile)
admin.site.register(HomeworkNotebook)
