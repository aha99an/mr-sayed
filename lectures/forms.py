from django import forms
from .models import Lecture
from classes.models import Week

class LectureCreateForm(forms.ModelForm):
    name = forms.CharField(label="اسم المحاضرة", required=True)
    week = forms.ModelChoiceField(queryset=Week.objects.all(), required=True, label="الأسبوع")
    lecture_allowed_time = forms.IntegerField(
        label="الوقت المتاح للمحاضرة بالدقايق", required=True)
    homeworkAnswerFile = forms.FileField(label=" نموذج اجابة الواجب السابق ")
    examAnswerFile = forms.FileField(label="نموذج اجابة الامتحان السابق ")

    class Meta:
        model = Lecture
        fields = ("name", "week","homeworkAnswerFile","examAnswerFile", "lecture_allowed_time")
