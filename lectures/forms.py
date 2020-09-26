from django import forms
from .models import Lecture


class LectureCreateForm(forms.ModelForm):
    # question = forms.CharField(label="السؤال", required=False)
    # image_question = forms.ImageField(label="صورة سؤال", required=False)
    # grade = forms.IntegerField(label="الدرجة")
    # lecture_manual_allow
    class Meta:
        model = Lecture
        fields = ("name", "lecture_allowed_time")
