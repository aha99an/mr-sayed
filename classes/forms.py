from django import forms
from .models import Class


class ClassForm(forms.ModelForm):
    name = forms.CharField(label="اسم الحصة", widget=forms.TextInput(
        attrs={"text-align": "right"}), required=True)
    week_day = forms.ChoiceField(
        choices=Class.DAYS_OF_WEEK, label="يوم الحصة", widget=forms.Select(attrs={"text-align": "right"}))
    start = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    end = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

    class Meta:
        model = Class
        fields = ("name", "week_day", "start", "end")
