from django import forms
from .models import (Homework, StudentHomework,
                     StudentHomeworkFile)


class StudentHomeworkFileForm(forms.ModelForm):
    class Meta:
        model = StudentHomeworkFile
        fields = ("student_homework_file",)


class StudentHomeworkMultipleFileForm(forms.Form):
    student_homework_file = forms.FileField(label=" رفع ملفات الواجب", 
        widget=forms.ClearableFileInput(attrs={'multiple': True}))


class AdminHomeworkForm(forms.ModelForm):
    notes = forms.CharField(widget=forms.Textarea,
                            label='ملاحظات', required=False)

    class Meta:
        model = StudentHomework
        fields = ("notes",)
