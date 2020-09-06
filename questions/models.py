from django.db import models
from accounts.models import CustomUser

# Create your models here.

class MrQuestion(models.Model):
    ءuser = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True , related_name="user_mr_question")
    question = models.CharField(max_length=1000, null=True, blank=True)
    answer = models.CharField(max_length=1000, null=True, blank=True)




    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
