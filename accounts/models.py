from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    school = models.CharField(max_length=200)
    parentPhoneNumber = models.IntegerField(default=0)
    phoneNumber = models.IntegerField(default=0)
    profile_pic = models.ImageField(null=True, blank=True)


