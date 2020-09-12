from django.contrib import admin
from .models import Lecture, StudentLecture, StudentLectureQuestion, LectureLink

admin.site.register(Lecture)
admin.site.register(LectureLink)
admin.site.register(StudentLecture)
admin.site.register(StudentLectureQuestion)
