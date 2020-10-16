from django import forms
from .models import Lecture
from classes.models import Week


def check_allowed_time(value):
    if value <= 0:
        raise forms.ValidationError(
            "الوقت المتاح للمحاضرة يجب ان يزيد عن الصفر")


class LectureCreateForm(forms.ModelForm):
    TRUE_FALSE_CHOICES = (
        (True, 'مثبتة'),
        (False, 'غير مثبتة')
    )
    name = forms.CharField(label="اسم المحاضرة", required=True)
    week = forms.ModelChoiceField(
        queryset=Week.objects.all(), required=False, label="الأسبوع")
    lecture_allowed_time = forms.IntegerField(validators=[check_allowed_time, ],
                                              label="الوقت المتاح للمحاضرة بالدقايق", required=False)
    is_permanent = forms.ChoiceField(choices=TRUE_FALSE_CHOICES,
                                     label="محاضرة مثبتة", initial=False, required=False)

    class Meta:
        model = Lecture
        fields = ("name", "week", "lecture_allowed_time", "is_permanent")

    def clean(self):
        data = self.cleaned_data
        if data.get('is_permanent', None) == "False" and not(data.get('week', None)):
            self.add_error('week', "الرجاء اختيار حصة للمحاضرة")
        if data.get('is_permanent', None) == "False" and not(data.get('lecture_allowed_time', None)):
            self.add_error('lecture_allowed_time',
                           "الرجاء ادخال الوقت المتاح للمحاضرة")
        else:
            return data
