from django import forms
from .models import Lecture


class LectureCreateForm(forms.ModelForm):
    name = forms.CharField(label="اسم المحاضرة", required=True)
    lecture_allowed_time = forms.IntegerField(
        label="الوقت المتاح للمحاضرة بالدقايق", required=True)

    class Meta:
        model = Lecture
        fields = ("name", "lecture_allowed_time")
