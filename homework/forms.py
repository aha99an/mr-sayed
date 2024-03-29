from django import forms
from .models import (Homework, StudentHomework,
                     StudentHomeworkFile)


class StudentHomeworkFileForm(forms.ModelForm):
    class Meta:
        model = StudentHomeworkFile
        fields = ("student_homework_file",)


class StudentHomeworkMultipleFileForm(forms.Form):
    student_homework_file = forms.FileField(label=" رفع ملفات الواجب", 
        widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)


class AdminHomeworkForm(forms.ModelForm):
    notes = forms.CharField(widget=forms.Textarea,
                            label='ملاحظات', required=False)

    notes_file = forms.FileField(
                            label=' ملاحظات كصوره أو ملف', required=False)
    class Meta:
        model = StudentHomework
        fields = ("notes","notes_file")
