from django.db import models
from classes.models import Week
from accounts.models import CustomUser
import os


class Homework(models.Model):
    name = models.CharField(max_length=200, verbose_name="اسم الواجب")
    week = models.ForeignKey(Week, on_delete=models.SET_NULL,
                             related_name="homework", null=True, blank=True, verbose_name="الأسبوع")
    homework_file = models.FileField(
        null=True, blank=True, verbose_name="ملف الواجب")
    homework_text = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="الواجب")
    homework_answer_file = models.FileField(
        null=True, blank=True, verbose_name="ملف حل الواجب")
    show_answer = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class StudentHomework(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    homework = models.ForeignKey(
        Homework, on_delete=models.CASCADE, related_name="student_homework")
    notes = models.TextField(null=True, blank=True)
    is_checked = models.BooleanField(default=False)
    notes_file = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.homework.name + "__" + self.user.username

    def save(self, *args, **kwargs):
        if self.notes:
            self.is_checked = True
        else:
            self.is_checked = False
        super(StudentHomework, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created_at',)


class StudentHomeworkFile(models.Model):
    student_homework = models.ForeignKey(
        StudentHomework, on_delete=models.CASCADE, related_name="student_homework_file")
    student_homework_file = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def snippet_file_name(self):
        if len(self.student_homework_file.name) > 20:
            return "..."+self.student_homework_file.name.rsplit(
                '/', 1)[1][:20]
        else:
            return self.student_homework_file.name

    class Meta:
        ordering = ('created_at',)


class StudentHomeworkMakeup(models.Model):
    exam = models.ForeignKey(
        Homework, on_delete=models.CASCADE, related_name="student_homework_makeup")
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="student_homework_makeup")
