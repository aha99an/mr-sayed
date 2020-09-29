from django import forms
from .models import Lecture
from classes.models import Week

class LectureCreateForm(forms.ModelForm):
    name = forms.CharField(label="اسم المحاضرة", required=True)
    week = forms.ModelChoiceField(queryset=Week.objects.all(), required=True, label="الحصة")
    lecture_allowed_time = forms.IntegerField(
        label="الوقت المتاح للمحاضرة بالدقايق", required=True)

    class Meta:
        model = Lecture
        fields = ("name", "week", "lecture_allowed_time")
