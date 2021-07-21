from django.db import models
from accounts.models import CustomUser


class MrQuestion(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="user_mr_question")
    question = models.CharField(
        max_length=1000, null=True, blank=True, verbose_name="السؤال:")
    image_question = models.ImageField(
        upload_to="images/questions", null=True, blank=True, verbose_name="اسأل بصوره:")
    answer = models.CharField(max_length=1000, null=True, blank=True)
    image_answer = models.ImageField(
        upload_to="images/questions", null=True, blank=True)
    is_answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.answer or self.image_answer:
            self.is_answered = True
        super(MrQuestion, self).save(*args, **kwargs)

    def __str__(self):
        if self.user:
            return self.user.username + "_" + str(self.id)
        return str(self.id)

class MrQuestionFile(models.Model):
    mr_question = models.ForeignKey(
        MrQuestion, on_delete=models.CASCADE, related_name="mr_question_file")
    mr_question_file = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def snippet_file_name(self):
        if len(self.mr_question_file.name) > 20:
            return "..."+self.mr_question_file.name.rsplit(
                '/', 1)[1][:20]
        else:
            return self.mr_question_file.name

    class Meta:
        ordering = ('created_at',)
