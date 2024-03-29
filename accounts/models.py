from django.contrib.auth.models import AbstractUser
from django.db import models
from classes.models import Class
import random


class CustomUser(AbstractUser):
    STUDENT = 0
    ADMIN = 1

    USER_TYPE_CHOICES = (
        (STUDENT, 'student'),
        (ADMIN, 'admin'),
    )

    username = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    parentPhoneNumber = models.CharField(max_length=200, default="0")
    phoneNumber = models.CharField(max_length=200, default="0")
    email = models.EmailField(max_length=255, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)
    student_class = models.ForeignKey(Class, null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name="student_class", verbose_name="المجموعة")
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=0)
    student_is_active = models.BooleanField(default=False)
    random_password = models.CharField(max_length=10, null=True, blank=True)
    homeWorkAnswerd = models.BooleanField(default=False)
    examStudentGrade = models.FloatField(default=None, null=True, blank=True)
    examGrade = models.FloatField(default=None, null=True, blank=True)
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.email = self.username

        if self.is_active is False:
            self.is_active = True
        super(CustomUser, self).save(*args, **kwargs)

    def is_student(self):
        if not self.user_type:
            return True

    def is_admin(self):
        if self.user_type:
            return True

    def reset_password(self):
        self.random_password = random.randint(0, 999999)
        self.set_password(self.random_password)
        self.save()

    class Meta:
        ordering = ('date_joined',)


class StudentPayment(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    number_available_lectures = models.IntegerField(
        default=0, null=True, blank=True)
    remainder_available_lectures = models.IntegerField(
        default=0, null=True, blank=True)
    paid_at = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    last_lecture_attended = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.remainder_available_lectures = self.number_available_lectures
        if self.number_available_lectures:
            CustomUser.objects.filter(id=self.user_id).update(
                student_is_active=True)
        super(StudentPayment, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name
