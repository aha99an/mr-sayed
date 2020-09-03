from django.db import models
from django.db.models.signals import post_save, pre_save
from django.core.exceptions import ValidationError
from django.dispatch import receiver
import math
from django.utils import timezone
from accounts.models import CustomUser


class Exam(models.Model):

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    total_question = models.IntegerField(default=0)
    score = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    time_quiz = models.IntegerField(default=0)
    mandatory = models.BooleanField(default=False)
    max_tries = models.IntegerField(default=1)
    availabe_from = models.DateTimeField(blank=True, null=True)
    availabe_to = models.DateTimeField(blank=True, null=True)
    answer = models.FileField(blank=True, null=True)
    show_answer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StudentExam(models.Model):

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="student_exam")
    score = models.IntegerField(null=True, blank=True, default=0)
    answered_questions = models.IntegerField(null=True, blank=True, default=0)
    # status = models.CharField(
    #     max_length=100, choices=STATUS_CHOICES, blank=True, null=True)
    try_number = models.IntegerField(null=True, blank=True, default=0)
    # is_reset = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(editable=False, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.exam.name + " " + self.user.username


class EssayQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.CharField(max_length=300, null=True, blank=True)
    image_question = models.ImageField(null=True, blank=True)
    grade = models.FloatField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StudentEssayAnswer(models.Model):
    question = models.ForeignKey(EssayQuestion, on_delete=models.CASCADE)
    student_exam = models.ForeignKey(
        StudentExam, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100, null=True, blank=True)
    image_answer = models.ImageField(null=True, blank=True)
    grade = models.FloatField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TrueFalseQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
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
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
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
    question = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE)
    student_exam = models.ForeignKey(
        StudentExam, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100, null=True, blank=True)
    # image_answer = models.ImageField(null=True, blank=True)
    grade = models.FloatField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# class QuizQuestion(models.Model):

#     TRUE_FALSE_Q = 0
#     MCQ_Q = 1
#     ESSAY_Q = 2

#     Question_type = (
#         (TRUE_FALSE_Q, 'True & False'),
#         (MCQ_Q, 'MCQ'),
#         (ESSAY_Q, '')
#     )

#     Question_Answer = (
#         (1, 'Option1'),
#         (2, 'Option2'),
#         (3, 'Option3'),
#         (4, 'Option4'),
#     )
#     exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
#     question = models.CharField(max_length=300)
#     option1 = models.CharField(max_length=300, null=True, blank=True)
#     option2 = models.CharField(max_length=300, null=True, blank=True)
#     option3 = models.CharField(max_length=300, null=True, blank=True)
#     option4 = models.CharField(max_length=300, null=True, blank=True)
#     right_answer_choice = models.IntegerField(choices=Question_Answer)
#     right_answer_essay = models.TextField(blank=True, null=True)
#     right_answer_tr_fa = models.BooleanField(
#         default=False, null=True, blank=True)
#     question_type = models.IntegerField(choices=Question_type)
#     created_date = models.DateTimeField(auto_now_add=True)
#     update_date = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.question


# # update the exam total_question number every time a question is added
# @receiver(post_save, sender=QuizQuestion)
# def question_save(sender, instance, **kwargs):
#     exam = Exam.objects.get(quiz_id=instance.quiz_id.quiz_id)
#     exam.total_question = exam.quizquestion_set.all().filter(status=True).count()
#     exam.score = exam.total_question
#     # exam.pass_score = math.ceil(int(exam.total_question)*.8)
#     exam.save()

# # Change provider exam status, count number of tries
# @receiver(post_save, sender=StudentAnswer)
# def providerquiz_save(sender, instance, **kwargs):
#     exam = Exam.objects.get(quiz_id=instance.provider_quiz.exam.quiz_id)
#     provider_quiz = StudentExam.objects.get(id=instance.provider_quiz.id)
#     if provider_quiz.answered_questions < exam.total_question:
#         provider_quiz.status = "incomplete"
#     else:
#         try:
#             current_try_number = StudentExam.objects.filter(exam=exam).filter(user_id=provider_quiz.user_id).exclude(id=StudentExam.id).last().try_number
#             provider_quiz.try_number = int(current_try_number)+1
#         except:
#             provider_quiz.try_number = 1
#         if provider_quiz.score <  math.ceil(int(exam.total_question)*(int(exam.pass_score)*.01)):

#             provider_quiz.status = "fail"
#         else:
#             provider_quiz.status = "pass"
#     provider_quiz.save()
