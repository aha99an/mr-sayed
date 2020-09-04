from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.EmailField(unique=True)
    school = models.CharField(max_length=200)
    parentPhoneNumber = models.IntegerField(default=0)
    phoneNumber = models.IntegerField(default=0)
    profile_pic = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.email= self.username
        super(CustomUser, self).save(*args, **kwargs)