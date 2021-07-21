from django import forms



class MrQuestionMultipleFileForm(forms.Form):
    mr_question_file = forms.FileField(label=" رفع صور الاجابة", 
        widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
