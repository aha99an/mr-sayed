from django import forms



class MrQuestionMultipleFileForm(forms.Form):
    mr_question_file = forms.FileField(label=" رفع صور الاجابة", 
        widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    # TRUE_FALSE_CHOICES = (
    #     (True, 'مفعل'),
    #     (False, 'غير مفعل')
    # )
    # is_active = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, label="التفعيل")