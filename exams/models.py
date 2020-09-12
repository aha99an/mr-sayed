from django.db import models
from django.core.exceptions import ValidationError
from django.dispatch import receiver
import math
from django.utils import timezone
from accounts.models import CustomUser
from datetime import timedelta


class Exam(models.Model):
    CHOICE_EXAM = 0
    VARIETY_EXAM = 1

    EXAM_TYPE_CHOICES = (
        (CHOICE_EXAM, 'امتحان اختياري'),
        (VARIETY_EXAM, 'امتحان اختياري و مقالي'),
    )
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    total_question = models.IntegerField(default=0)
    grade = models.DecimalField(max_digits=10, default=0, decimal_places=1)
    time = models.IntegerField(default=0, help_text="In minutes")
    exam_type = models.IntegerField(
        choices=EXAM_TYPE_CHOICES, default=0)
    # mandatory = models.BooleanField(default=False)
    # max_tries = models.IntegerField(default=1)
    # availabe_from = models.DateTimeField(blank=True, null=True)
    # availabe_to = models.DateTimeField(blank=True, null=True)
    answer = models.FileField(blank=True, null=True)
    show_answer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StudentExam(models.Model):

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="student_exam")
    grade = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True)
    answered_questions = models.IntegerField(null=True, blank=True, default=0)
    is_graded = models.BooleanField(default=False)
    expiry_time = models.DateTimeField(null=True, blank=True)
    # status = models.CharField(
    #     max_length=100, choices=STATUS_CHOICES, blank=True, null=True)
    # try_number = models.IntegerField(null=True, blank=True, default=0)
    # is_reset = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.exam.name + " " + self.user.username


class EssayQuestion(models.Model):
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="essay_question")
    question = models.CharField(max_length=300, null=True, blank=True)
    image_question = models.ImageField(null=True, blank=True)
    grade = models.FloatField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.exam.exam_type = Exam.VARIETY_EXAM
        self.exam.save()
        super(EssayQuestion, self).save(*args, **kwargs)


class StudentEssayAnswer(models.Model):
    question = models.ForeignKey(
        EssayQuestion, on_delete=models.CASCADE, related_name="student_essay_answer")
    student_exam = models.ForeignKey(
        StudentExam, on_delete=models.CASCADE)
    answer = models.TextField(max_length=100, null=True, blank=True)
    image_answer = models.ImageField(null=True, blank=True)
    grade = models.FloatField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ChoiceQuestion(models.Model):
    OPTION1 = 0
    OPTION2 = 1
    OPTION3 = 2
    OPTION4 = 3

    Question_Answer = (
        (OPTION1, 'option1'),
        (OPTION2, 'option2'),
        (OPTION3, 'option3'),
        (OPTION4, 'option4'),
    )
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="choice_question")
    question = models.CharField(max_length=300, null=True, blank=True)
    image_question = models.ImageField(null=True, blank=True)
    option1 = models.CharField(max_length=300)
    option2 = models.CharField(max_length=300)
    option3 = models.CharField(max_length=300, null=True, blank=True)
    option4 = models.CharField(max_length=300, null=True, blank=True)
    right_answer_choice = models.IntegerField(choices=Question_Answer)
    grade = models.FloatField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class StudentChoiceAnswer(models.Model):
    question = models.ForeignKey(
        ChoiceQuestion, on_delete=models.CASCADE, related_name="student_choice_answer")
    student_exam = models.ForeignKey(
        StudentExam, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100, null=True, blank=True)
    grade = models.FloatField(max_length=100, null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        answers_list = [self.question.option1, self.question.option2,
                        self.question.option3, self.question.option4]

        if self.answer == answers_list[self.question.right_answer_choice]:
            self.grade = self.question.grade
        super(StudentChoiceAnswer, self).save(*args, **kwargs)


class TrueFalseQuestion(models.Model):
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="true_false_question")
    question = models.CharField(max_length=300, null=True, blank=True)
    image_question = models.ImageField(null=True, blank=True)
    grade = models.FloatField(max_length=100)
    right_answer = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StudentTrueFalseAnswer(models.Model):
    question = models.ForeignKey(EssayQuestion, on_delete=models.CASCADE)
    student_exam = models.ForeignKey(
        StudentExam, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.BooleanField()
    # image_answer = models.ImageField(null=True, blank=True)
    grade = models.FloatField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
