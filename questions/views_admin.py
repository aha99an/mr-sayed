from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from .models import MrQuestion, MrQuestionFile
from .forms import MrQuestionMultipleFileForm
from django.urls import reverse_lazy
from home.permissions import AdminPermission
import os
import json
import boto3
import random
import uuid
from django.shortcuts import redirect
from django.http import HttpResponse
from datetime import datetime

image_extensions = ('.djvu', '.art', '.cpt', '.tif', '.jpe', '.rgb', '.svgz', '.nef', '.xbm', '.jpeg', '.jpm', '.erf', '.cdt', '.bmp', '.pgm', '.ico', '.xpm', '.jpx', '.pcx', '.ief',
                    '.svg', '.jp2', '.pbm', '.djv', '.cr2', '.png', '.xwd', '.ppm', '.jng', '.jpg2', '.orf', '.cdr', '.gif', '.psd', '.ras', '.pnm', '.crw', '.wbmp', '.pat', '.tiff', '.jpf', '.jpg')


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
    question_id = request.GET.get("mr_question_id")
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
        # mrquestion.answer = answer_question
        # mrquestion.image_answer = image_name
        # mrquestion.save()
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        mrquestion.answer = answer_question
        mrquestion.save()
        return redirect('all_questions')

def mr_question_image_success_upload(request):
    image_name = request.GET.get('image_name')[7:]
    question_id = request.GET.get('question_id')

    mr_question = MrQuestion.objects.get(id=int(question_id))
    # student_homework, created = StudentHomework.objects.get_or_create(
    #     homework=homework, user=request.user)
    MrQuestionFile.objects.create(
        mr_question=mr_question, mr_question_file=image_name)

    return HttpResponse(status=201)


class MrQuestionMultipleUpdateView(AdminPermission, FormView):
    template_name = 'questions/answer-question.html'
    form_class = MrQuestionMultipleFileForm
    success_url = reverse_lazy('all_questions')

    def form_invalid(self, form, error_message):
        ctx = self.get_context_data()
        ctx["error_message"] = error_message
        return self.render_to_response(ctx)

    def dispatch(self, request, *args, **kwargs):
        now = datetime.now()
        self.mr_question = MrQuestion.objects.filter(id=self.kwargs.get("pk")).last()

        if not self.mr_question:
            return redirect("all_questions")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('mr_question_file')

        if form.is_valid():
            files_length = len(files)
            uploaded_files_length = self.mr_question.mr_question_file.all().count()
            if files_length + uploaded_files_length < 1:
                return self.form_invalid(form, 'عدد الملفات لا يجب أن تقل عن 1')
            elif files_length + uploaded_files_length > 6:
                return self.form_invalid(form, 'عدد الملفات لا يجب أن تزيد عن 6')
            for f in files:
                MrQuestionFile.objects.create(
                    student_homework=self.mr_question, mr_question_file=f)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        homework = MrQuestion.objects.get(id=self.kwargs.get("pk"))
        # homework_questions = homework.homework_file

        # student_homework = StudentHomework.objects.filter(
        #     homework__id=self.kwargs.get("homework_pk"), user=self.request.user).last()

        # ctx["homework_questions"] = homework_questions
        # ctx["homework"] = homework
        ctx["image_extensions"] = image_extensions
        ctx['object'] = MrQuestion.objects.get(id=self.kwargs.get("pk"))
        # if student_homework:
        ctx["uploaded_files"] = MrQuestion.objects.get(id=self.kwargs.get("pk")).mr_question_file.all()

        return ctx



# def direct_upload_s3(request):

#     lowercase_str = uuid.uuid4().hex
#     S3_BUCKET = 'mr-sayedabdelhamed2'
#     file_name = request.GET.get('file_name')
#     file_type = request.GET.get('file_type')
#     homework_id = request.GET.get('homework_id')

#     file_only_name, file_extension = os.path.splitext(file_name)
#     image_name = "images/homework/" + file_only_name + \
#         request.user.username + "-" + lowercase_str[:6] + str(file_extension)

#     # if file_name:
#     s3 = boto3.client('s3')
#     presigned_post = s3.generate_presigned_post(
#         Bucket=S3_BUCKET,
#         Key="static/" + image_name,
#         Fields={"acl": "public-read", "Content-Type": file_type},
#         Conditions=[
#             {"acl": "public-read"},
#             {"Content-Type": file_type}
#         ],
#         ExpiresIn=3600
#     )
#     data = {
#         'data': presigned_post,
#         'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
#     }
#     return HttpResponse(json.dumps(data), content_type="application/json")


def delete_image_answer(request, pk):
    mrquestion = MrQuestion.objects.get(id=pk)
    mrquestion.image_answer = None
    mrquestion.save()
    return redirect(reverse_lazy("answer_question", kwargs={"pk": pk}))
