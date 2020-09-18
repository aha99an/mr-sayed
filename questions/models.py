from django.db import models
from accounts.models import CustomUser


class MrQuestion(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True , related_name="user_mr_question")
    question = models.CharField(max_length=1000, null=True, blank=True)
    image_question = models.ImageField(null=True, blank=True)
    answer = models.CharField(max_length=1000, null=True, blank=True)
    image_answer = models.ImageField(null=True, blank=True)
    is_answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
