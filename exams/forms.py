from django import forms
from .models import StudentChoiceAnswer, StudentEssayAnswer, Exam, ChoiceQuestion, EssayQuestion


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
    answer = forms.FileField(label="نموذج الاجابة")

    class Meta:
        model = Exam
        fields = ("name", "week", "is_active", "time", "grade", "answer")


class ChoiceQuestionCreateForm(forms.ModelForm):
    question = forms.CharField(label="السؤال", required=False)
    image_question = forms.ImageField(label="صورة سؤال", required=False)
    option1 = forms.CharField(label="الاختيار الاول")
    option2 = forms.CharField(label="الاختيار الثاني")
    option3 = forms.CharField(label="الاختيار الثالث")
    option4 = forms.CharField(label="الاختيار الرابع")
    right_answer_choice = forms.ChoiceField(
        choices=ChoiceQuestion.QUESTION_ANSWER_CHOICES, label="اختار الاجابة الصحيحة ")
    grade = forms.IntegerField(label="الدرجة")

    class Meta:
        model = ChoiceQuestion
        fields = ("question", "image_question", "option1", "option2",
                  "option3", "option4", "right_answer_choice", "grade")


class EssayQuestionCreateForm(forms.ModelForm):
    question = forms.CharField(label="السؤال", required=False)
    image_question = forms.ImageField(label="صورة سؤال", required=False)
    grade = forms.IntegerField(label="الدرجة")

    class Meta:
        model = EssayQuestion
        fields = ("question", "image_question", "grade")
