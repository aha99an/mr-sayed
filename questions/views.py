from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import MrQuestion
from django.urls import reverse_lazy
from home.permissions import StudentPermission
import os
import json
import boto3
# import urllib2


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
        print("HELLO")
        S3_BUCKET = 'mr-sayedabdelhamed2'

        # context['data'] = presigned_post
        # context['url'] = 'https://%s.s3.amazonaws.com/%s' % (
        # S3_BUCKET, file_name)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        print("HELLO")
        context = super().get_context_data(**kwargs)
        # ctx["is_checked_filter"] = self.request.GET.get('is_checked_filter')
        S3_BUCKET = 'mr-sayedabdelhamed2'
        file_name = self.request.GET.get('file_name')
        file_type = self.request.GET.get('file_type')
        if file_name:
            s3 = boto3.client('s3')
            presigned_post = s3.generate_presigned_post(
                Bucket=S3_BUCKET,
                Key=file_name,
                Fields={"acl": "public-read", "Content-Type": file_type},
                Conditions=[
                    {"acl": "public-read"},
                    {"Content-Type": file_type}
                ],
                ExpiresIn=3600
            )
            context['data'] = presigned_post
            context['url'] = 'https://%s.s3.amazonaws.com/%s' % (
                S3_BUCKET, file_name)
            print(context['data'])
            print(context['url'])
            # return json.dumps({
            #     'data': presigned_post,
            #     'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
            # })
        return context


def index2(request):
    S3_BUCKET = 'mr-sayedabdelhamed2'
    file_name = request.GET.get('file_name')
    file_type = request.GET.get('file_type')
    if file_name:
        s3 = boto3.client('s3')
        presigned_post = s3.generate_presigned_post(
            Bucket=S3_BUCKET,
            Key=file_name,
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
        print(data["data"])
        return HttpResponse(json.dumps(data), content_type="application/json")

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
