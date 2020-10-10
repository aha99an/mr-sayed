from django.db import models
from django.core.exceptions import ValidationError
import math
import collections
from django.utils import timezone
from accounts.models import CustomUser
from datetime import timedelta
from classes.models import Week
from django.contrib.postgres.fields import JSONField


class Exam(models.Model):
    CHOICE_EXAM = 0
    VARIETY_EXAM = 1

    EXAM_TYPE_CHOICES = (
        (CHOICE_EXAM, 'امتحان اختياري'),
        (VARIETY_EXAM, 'امتحان اختياري و مقالي'),
    )
    week = models.ForeignKey(
        Week, on_delete=models.SET_NULL, verbose_name="الأسبوع", null=True, blank=True)
    name = models.CharField(max_length=200)
    total_question = models.IntegerField(default=0)
    grade = models.DecimalField(
        max_digits=10, default=0, decimal_places=1, verbose_name="الدرجة")
    time = models.IntegerField(default=0, verbose_name="الوقت بالدقايق")
    exam_type = models.IntegerField(
        choices=EXAM_TYPE_CHOICES, default=0)
    answer = models.FileField(blank=True, null=True)
    show_answer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    been_a_week = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_past_week(self):
        if self.been_a_week:
            return True
        if timezone.now().date() > self.week.end:
            self.been_a_week = True
            self.save()
            return True
        return False

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created_at',)


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
    questions = models.TextField(null=True, blank=True)
    questions_json = JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.exam.name + " " + self.user.username

    class Meta:
        ordering = ('created_at',)


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

    def delete(self, *args, **kwargs):
        # This means that it is the only essay question in this exam
        if not self.exam.essay_question.count == 1:
            self.exam.exam_type = Exam.CHOICE_EXAM
            self.exam.save()
        super(EssayQuestion, self).delete(*args, **kwargs)

    def __str__(self):
        return self.question + "--" + self.exam.name

    class Meta:
        ordering = ('created_at',)


class StudentEssayAnswer(models.Model):
    question = models.ForeignKey(
        EssayQuestion, on_delete=models.CASCADE, related_name="student_essay_answer")
    student_exam = models.ForeignKey(
        StudentExam, on_delete=models.CASCADE, related_name="student_essay_answer")
    answer = models.TextField(max_length=100, null=True, blank=True)
    image_answer = models.ImageField(null=True, blank=True)

    grade = models.FloatField(max_length=100, null=True, blank=True)
    is_graded = models.BooleanField(default=False)
    is_answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.answer or self.image_answer:
            self.is_answered = True
        else:
            self.is_answered = False
        print(self.grade)
        if self.grade:
            print("HELLO THERE")
        super(StudentEssayAnswer, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created_at',)


class ChoiceQuestion(models.Model):
    OPTION1 = 1
    OPTION2 = 2
    OPTION3 = 3
    OPTION4 = 4

    QUESTION_ANSWER_CHOICES = (
        (OPTION1, "الاختيار الاول"),
        (OPTION2, "الاختيار الثاني"),
        (OPTION3, "الاختيار الثالث"),
        (OPTION4, "الاختيار الرابع"),
    )
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="choice_question")
    question = models.CharField(max_length=300, null=True, blank=True)
    image_question = models.ImageField(null=True, blank=True)
    option1 = models.CharField(max_length=300)
    option2 = models.CharField(max_length=300)
    option3 = models.CharField(max_length=300)
    option4 = models.CharField(max_length=300)
    right_answer_choice = models.IntegerField(choices=QUESTION_ANSWER_CHOICES)
    grade = models.FloatField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question or " "

    class Meta:
        ordering = ('created_at',)


class StudentChoiceAnswer(models.Model):
    question = models.ForeignKey(
        ChoiceQuestion, on_delete=models.CASCADE, related_name="student_choice_answer")
    student_exam = models.ForeignKey(
        StudentExam, on_delete=models.CASCADE, related_name="student_choice_answer")
    answer = models.CharField(max_length=100, null=True, blank=True)
    grade = models.FloatField(max_length=100, null=True, blank=True, default=0)
    is_answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        answers_list = [self.question.option1, self.question.option2,
                        self.question.option3, self.question.option4]

        if self.answer == answers_list[self.question.right_answer_choice - 1]:
            self.grade = self.question.grade
        else:
            self.grade = 0
        if self.answer:
            self.is_answered = True
        else:
            self.is_answered = False
        super(StudentChoiceAnswer, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created_at',)


class TrueFalseQuestion(models.Model):
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="true_false_question")
    question = models.CharField(max_length=300, null=True, blank=True)
    image_question = models.ImageField(null=True, blank=True)
    grade = models.FloatField(max_length=100)
    right_answer = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)


class StudentTrueFalseAnswer(models.Model):
    question = models.ForeignKey(EssayQuestion, on_delete=models.CASCADE)
    student_exam = models.ForeignKey(
        StudentExam, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.BooleanField()
    # image_answer = models.ImageField(null=True, blank=True)
    grade = models.FloatField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)


class StudentExamMakeup(models.Model):
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="student_exam_makeup")
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="student_exam_makeup")
