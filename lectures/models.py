from django.db import models
from classes.models import Week
from accounts.models import CustomUser, StudentPayment


class Lecture(models.Model):
    name = models.CharField(max_length=255)
    week = models.ForeignKey(
        Week, on_delete=models.SET_NULL, related_name="lecture", null=True, blank=True)
    lecture_allowed_time = models.IntegerField(default=0, null=True, blank=True)
    homeworkAnswerFile = models.FileField(
        null=True, blank=True, verbose_name=" ملف الواجب في المحاضرة")
    examAnswerFile = models.FileField(
        null=True, blank=True, verbose_name=" ملف الامتحان في المحاضرة")
    is_permanent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)


class LectureLink(models.Model):
    link = models.TextField()
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, related_name="lecture_link")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def link_number(self):
        try:
            return self.link.split(".com/")[1]
        except:
            return "Invalid Link"

    class Meta:
        ordering = ('id',)


class StudentLecture(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)
    student_payment = models.ForeignKey(
        StudentPayment, on_delete=models.SET_NULL, related_name="student_lecture", null=True, blank=True)
    seen_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.user.first_name + "-" + self.lecture.name


class StudentLectureQuestion(models.Model):
    student_lecture = models.ForeignKey(
        StudentLecture, on_delete=models.CASCADE)
    question = models.TextField()
    time = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)


class StudentSeenLink(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    link = models.ForeignKey(LectureLink, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)


class StudentLectureMakeup(models.Model):
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, related_name="student_lecture_makeup")
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="student_lecture_makeup")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)
