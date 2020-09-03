from django import forms
from .models import StudentChoiceAnswer


class StudentChoiceAnswerForm(forms.ModelForm):
    class Meta:
        model = StudentChoiceAnswer
        fields = ("answer",)
