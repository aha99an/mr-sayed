from django import forms
from .models import (Homework, HomeworkFile, HomeworkAnswerFile, StudentHomework,
                     StudentHomeworkFile)


class StudentHomeworkFileForm(forms.ModelForm):
    class Meta:
        model = StudentHomeworkFile
        fields = ("student_homework_file",)


class StudentHomeworkMultipleFileForm(forms.Form):
    student_homework_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
