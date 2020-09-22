from django.contrib.auth.models import AbstractUser
from django.db import models
from classes.models import Class


class CustomUser(AbstractUser):
    STUDENT = 0
    ADMIN = 1

    USER_TYPE_CHOICES = (
        (STUDENT, 'student'),
        (ADMIN, 'admin'),
    )

    username = models.EmailField(unique=True)
    school = models.CharField(max_length=200)
    parentPhoneNumber = models.IntegerField(default=0)
    phoneNumber = models.IntegerField(default=0)
    profile_pic = models.ImageField(null=True, blank=True)
    student_class = models.ForeignKey(Class, null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name="student_class", verbose_name="المجموعة")
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=0)
    student_is_active = models.BooleanField(default=False)
    random_password = models.CharField(max_length=10, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.email = self.username
        super(CustomUser, self).save(*args, **kwargs)

    def is_student(self):
        if not self.user_type:
            return True

    def is_admin(self):
        if self.user_type:
            return True
