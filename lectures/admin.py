from django.contrib import admin
from .models import Lecture, StudentLecture, StudentLectureQuestion, LectureLink, StudentLectureMakeup


@admin.register(StudentLecture)
class StudentLectureAdmin(admin.ModelAdmin):
    fields = ["user", "lecture", "is_seen", "student_payment", "seen_at"]
    readonly_fields = ("updated_at", "created_at")

admin.site.register(Lecture)
admin.site.register(LectureLink)
# admin.site.register(StudentLecture)
admin.site.register(StudentLectureQuestion)
admin.site.register(StudentLectureMakeup)
