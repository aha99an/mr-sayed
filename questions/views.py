from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import MrQuestion
from django.urls import reverse_lazy
from home.permissions import StudentPermission
from django.shortcuts import redirect
import os
import json
import boto3
import random
import uuid


class QuestionListView (StudentPermission, ListView):
    template_name = "questions/student-questions.html"

    def get_queryset(self):
        return MrQuestion.objects.filter(user=self.request.user)


class QuestionDetailView(StudentPermission, DetailView):
    model = MrQuestion
    template_name = 'questions/question-detail.html'


class QuestionCreateView(StudentPermission, CreateView):
    model = MrQuestion
    template_name = 'questions/question-new.html'
    fields = ('question', 'image_question',)
    success_url = reverse_lazy('student_questions')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # # ctx["is_checked_filter"] = self.request.GET.get('is_checked_filter')
        # S3_BUCKET = 'mr-sayedabdelhamed2'
        # file_name = self.request.GET.get('file_name')
        # file_type = self.request.GET.get('file_type')
        # if file_name:
        #     s3 = boto3.client('s3')
        #     presigned_post = s3.generate_presigned_post(
        #         Bucket=S3_BUCKET,
        #         Key=file_name,
        #         Fields={"acl": "public-read", "Content-Type": file_type},
        #         Conditions=[
        #             {"acl": "public-read"},
        #             {"Content-Type": file_type}
        #         ],
        #         ExpiresIn=3600
        #     )
        #     context['data'] = presigned_post
        #     context['url'] = 'https://%s.s3.amazonaws.com/%s' % (
        #         S3_BUCKET, file_name)
        #     # return json.dumps({
        #     #     'data': presigned_post,
        #     #     'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
        #     # })
        return context


def index2(request):
    lowercase_str = uuid.uuid4().hex
    S3_BUCKET = 'mr-sayedabdelhamed2'
    file_name = request.GET.get('file_name')
    file_type = request.GET.get('file_type')
    question = request.GET.get('question')
    if not question:
        question = "سؤال بصورة"
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
        MrQuestion.objects.create(
            question=question, user=request.user, image_question=image_name)
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        MrQuestion.objects.create(
            question=question, user=request.user)
        return redirect('student_questions')

    # if request.method == 'GET':
        # form = InvoiceForm(request.POST)
        # if form.is_valid():
        #     instance = form.save(commit=False)
        #     instance.save()
        #     return redirect('home2')

    # else:
    #     form = InvoiceForm()

    # return render(request, 'home2.html', {'form': form,
    #                                       'invoices': Invoice.objects.all()})
