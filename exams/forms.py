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


class StudentEssayGradingForm(forms.ModelForm):
    grade = forms.FloatField(
        label="الدرجة", widget=forms.NumberInput(attrs={'color': "black", 'step': "0.01"}))

    class Meta:
        model = StudentEssayAnswer
        fields = ("grade",)
