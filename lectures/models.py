from django.db import models
from classes.models import Week
from accounts.models import CustomUser


class Lecture(models.Model):
    name = models.CharField(max_length=255)
    week = models.ForeignKey(
        Week, on_delete=models.SET_NULL, related_name="lecture", null=True, blank=True)
    lecture_allowed_time = models.IntegerField(default=0)
    lecture_manual_allow = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class LectureLink(models.Model):
    link = models.TextField()
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, related_name="lecture_link")

    def link_number(self):
        try:
            return self.link.split(".com/")[1]
        except:
            return "Invalid Link"


class StudentLecture(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE)
    special_access = models.BooleanField(default=False)
    attendance = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StudentLectureQuestion(models.Model):
    student_lecture = models.ForeignKey(
        StudentLecture, on_delete=models.CASCADE)
    question = models.TextField()
    time = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
