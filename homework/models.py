from django.db import models
from classes.models import Week
from accounts.models import CustomUser
import os


class Homework(models.Model):
    name = models.CharField(max_length=200)
    week = models.ForeignKey(
        Week, on_delete=models.CASCADE, related_name="homework")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class HomeworkFile(models.Model):
    homework = models.ForeignKey(
        Homework, on_delete=models.CASCADE, related_name="homework_file")
    homework_file = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def extension(self):
        name, extension = os.path.splitext(self.homework_file.name)
        return extension


class HomeworkNotebook(models.Model):
    homework = models.ForeignKey(
        Homework, on_delete=models.CASCADE, related_name="homework_notebook")
    homework_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class HomeworkAnswerFile(models.Model):
    homework = models.ForeignKey(
        Homework, on_delete=models.CASCADE, related_name="homework_answer_file")
    homework_answer_file = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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


class StudentHomeworkFile(models.Model):
    student_homework = models.ForeignKey(
        StudentHomework, on_delete=models.CASCADE, related_name="student_homework_file")
    student_homework_file = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def snippet_file_name(self):
        if len(self.student_homework_file.name) > 20:
            return self.student_homework_file.name[:20] + "..."
        else:
            return self.student_homework_file.name
