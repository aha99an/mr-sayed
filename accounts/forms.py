from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

# DataFlair #Custom_Validator


def check_size(value):
    if len(value) < 11 and value.isdigit():
        raise forms.ValidationError("please enter a valid phone number")


class CustomUserCreationForm(UserCreationForm):
    parentPhoneNumber = forms.CharField(
        validators=[check_size, ], label="Parent mobile")
    phoneNumber = forms.CharField(
        validators=[check_size, ], label="Your mobile")
    username = forms.EmailField(label="email")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = CustomUser
     #  fields = UserCreationForm.Meta.fields +("school", "parentPhoneNumber", "phoneNumber", "profile_pic")
        # fields = UserCreationForm.Meta.fields
        fields = ('username', 'first_name', 'last_name', 'school',
                  "parentPhoneNumber", "phoneNumber", "profile_pic")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

        fields = ('username', 'first_name', 'last_name', 'email',
                  'school', "parentPhoneNumber", "phoneNumber", "profile_pic")


class StudentChangeForm(forms.ModelForm):
    TRUE_FALSE_CHOICES = (
        (True, 'مفعل'),
        (False, 'غير مفعل')
    )
    # student_class = forms.CharField(label="المجموعة")
    is_active = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, label="التفعيل")

    class Meta:
        model = CustomUser
        fields = ('student_class', 'is_active',)
