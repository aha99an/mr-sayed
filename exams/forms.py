from django import forms
from .models import StudentChoiceAnswer, StudentEssayAnswer


class StudentChoiceAnswerForm(forms.ModelForm):
    class Meta:
        model = StudentChoiceAnswer
        fields = ("answer",)

class StudentEssayAnswerForm(forms.ModelForm):
    class Meta:
        model = StudentEssayAnswer
        fields = ("answer", "image_answer")
