from django.db import models
from config.choices import *
# from eprms_final.users.models import User
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.dispatch import receiver
import math
from django.utils import timezone


class Quiz(models.Model):

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    total_question = models.IntegerField(default=0)
    score = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    time_quiz = models.IntegerField(default=0)
    mandatory = models.BooleanField(default=False)
    max_tries = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="quiz_created_by")
    updated_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="quiz_updated_by")

    def __str__(self):
        return self.name


class QuizQuestion(models.Model):

    TRUE_FALSE_Q = 0
    MCQ_Q = 1
    ESSAY_Q = 2

    Question_type = (
        (TRUE_FALSE_Q, 'True & False'),
        (MCQ_Q, 'MCQ'),
        (ESSAY_Q, '')
        )
    Question_Answer = (
    (1, 'Option1'),
    (2, 'Option2'),
    (3, 'Option3'),
    (4, 'Option4'),
)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    status = models.BooleanField(default=True)
    option1 = models.CharField(max_length=300, null=True, blank=True)
    option2 = models.CharField(max_length=300, null=True, blank=True)
    option3 = models.CharField(max_length=300, null=True, blank=True)
    option4 = models.CharField(max_length=300, null=True, blank=True)
    right_answer_choice = models.IntegerField(choices=Question_Answer)
    right_answer_essay = models.TextField(blank=True,null=True)
    right_answer_tr_fa =  models.BooleanField(default=False, null=True, blank=True)
    question_type = models.IntegerField(choices=Question_type)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="QuizQuestion_created_by")
    updated_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="QuizQuestion_updated_by")

    def __str__(self):
        return self.question


class StudentQuiz(models.Model):
    STATUS_CHOICES = (
        ('pass','pass'),
        ('fail','fail'),
        ('incomplete','incomplete'),)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="provider_quiz")
    score = models.IntegerField(null=True, blank=True, default=0)
    answered_questions = models.IntegerField(null=True, blank=True, default=0)
    status = models.CharField(max_length=100,choices=STATUS_CHOICES,blank=True,null=True)
    try_number = models.IntegerField(null=True, blank=True, default=0)
    is_reset = models.BooleanField(default=False,null=True, blank=True)
    created_at = models.DateTimeField(editable=False,null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.quiz.name+" "+self.user_id.username

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(ProviderQuiz, self).save(*args, **kwargs)

class ProviderAnswers(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    provider_quiz = models.ForeignKey(ProviderQuiz, on_delete=models.CASCADE,null=True,blank=True)
    answer = models.CharField(max_length=100)



# update the quiz total_question number every time a question is added
@receiver(post_save, sender=QuizQuestion)
def question_save(sender, instance, **kwargs):
    quiz = Quiz.objects.get(quiz_id=instance.quiz_id.quiz_id)
    quiz.total_question = quiz.quizquestion_set.all().filter(status=True).count()
    quiz.score = quiz.total_question
    # quiz.pass_score = math.ceil(int(quiz.total_question)*.8)
    quiz.save()

# Change provider quiz status, count number of tries
@receiver(post_save, sender=ProviderAnswers)
def providerquiz_save(sender, instance, **kwargs):
    quiz = Quiz.objects.get(quiz_id=instance.provider_quiz.quiz.quiz_id)
    provider_quiz = ProviderQuiz.objects.get(id=instance.provider_quiz.id)
    if provider_quiz.answered_questions < quiz.total_question:
        provider_quiz.status = "incomplete"
    else:
        try:
            current_try_number = ProviderQuiz.objects.filter(quiz=quiz).filter(user_id=provider_quiz.user_id).exclude(id=provider_quiz.id).last().try_number
            provider_quiz.try_number = int(current_try_number)+1
        except:
            provider_quiz.try_number = 1
        if provider_quiz.score <  math.ceil(int(quiz.total_question)*(int(quiz.pass_score)*.01)):

            provider_quiz.status = "fail"
        else:
            provider_quiz.status = "pass"
    provider_quiz.save()

