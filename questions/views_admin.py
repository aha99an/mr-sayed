from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import MrQuestion
from django.urls import reverse_lazy
from home.permissions import AdminPermission
import os
import json
import boto3
import random
import uuid
from django.shortcuts import redirect
from django.http import HttpResponse


class AdminQuestionListView (AdminPermission, ListView):
    model = MrQuestion
    template_name = "questions/all-questions.html"
    paginate_by = 10

    # def get_queryset(self):
    #     try:
    #         a = self.request.GET.get('exam',)
    #     except KeyError:
    #         a = None
    #     q = MrQuestion.objects.all()

    #     class_filter = self.request.GET.get('class_filter')
    #     is_answered = self.request.GET.get('is_answered')
    #     if class_filter:
    #         q = q.filter(
    #             user__student_class__name=class_filter)
    #     if is_answered:
    #         if is_answered == "True":
    #             q = q.filter(is_graded=True)
    #         else:
    #             q = q.filter(is_graded=False)

    #     return q

    def get_queryset(self):
        queryset = MrQuestion.objects.all()
        # class_filter = self.request.GET.get('class_filter')
        is_answered = self.request.GET.get('is_answered')
        # if class_filter:
        #     queryset = queryset.filter(
        #         user__is_answered=class_filter)
        if is_answered:
            if is_answered == "True":
                queryset = queryset.filter(is_answered=True)
            else:
                queryset = queryset.filter(is_answered=False)
        return queryset


class AdminQuestionUpdateView(AdminPermission, UpdateView):
    model = MrQuestion
    template_name = 'questions/answer-question.html'
    fields = ('answer', 'image_answer')
    success_url = reverse_lazy('all_questions')

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        question_model = self.get_object()
        ctx['question'] = question_model

        return ctx


def upload_to_s3_admin(request):
    lowercase_str = uuid.uuid4().hex
    S3_BUCKET = 'mr-sayedabdelhamed2'
    file_name = request.GET.get('file_name')
    file_type = request.GET.get('file_type')
    answer_question = request.GET.get('answer_question')
    question_id = request.GET.get("question_id")
    mrquestion = MrQuestion.objects.get(id=int(question_id))

    file_only_name, file_extension = os.path.splitext(file_name)
    image_name = "images/questions/" + file_only_name + \
        request.user.username + "-" + lowercase_str[:6] + str(file_extension)

    if file_name:
        s3 = boto3.client('s3')
        presigned_post = s3.generate_presigned_post(
            Bucket=S3_BUCKET,
            Key="static/" + image_name,
            Fields={"acl": "public-read", "Content-Type": file_type},
            Conditions=[
                {"acl": "public-read"},
                {"Content-Type": file_type}
            ],
            ExpiresIn=3600
        )
        data = {
            'data': presigned_post,
            'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
        }
        mrquestion.answer = answer_question
        mrquestion.image_answer = image_name
        mrquestion.save()
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        mrquestion.answer = answer_question
        mrquestion.save()
        return redirect('all_questions')


def delete_image_answer(request, pk):
    mrquestion = MrQuestion.objects.get(id=pk)
    mrquestion.image_answer = None
    mrquestion.save()
    return redirect(reverse_lazy("answer_question", kwargs={"pk": pk}))
