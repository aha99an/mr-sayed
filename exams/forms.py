from django import forms
from .models import StudentChoiceAnswer, StudentEssayAnswer, Exam


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


class ExamCreateForm(forms.ModelForm):
    name = forms.CharField(label="اسم الامتحان", widget=forms.TextInput(
        attrs={"text-align": "right"}), required=True)
    is_active = forms.BooleanField()
    TRUE_FALSE_CHOICES = (
        (True, 'مفعل'),
        (False, 'غير مفعل')
    )
    is_active = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, label="التفعيل")

    class Meta:
        model = Exam
        fields = ("name", "week", "is_active", "time", "grade")
