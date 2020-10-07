from django import forms
from .models import Class,Week


class ClassForm(forms.ModelForm):
    name = forms.CharField(label="اسم المجموعة", widget=forms.TextInput(
        attrs={"text-align": "right"}), required=True)
    week_day = forms.ChoiceField(
        choices=Class.DAYS_OF_WEEK, label="يوم المجموعة", widget=forms.Select(attrs={"text-align": "right"}))
    start = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    end = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

    class Meta:
        model = Class
        fields = ("name", "week_day", "start", "end")



class WeekForm(forms.ModelForm):
    name = forms.CharField(label="اسم الأسبوع", widget=forms.TextInput(
        attrs={"text-align": "right"}), required=True)
    start = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y'))
    end =  forms.DateField(widget=forms.DateInput(format='%d-%m-%Y'))

    class Meta: 
        model = Week
        fields = ("name", "start", "end")
