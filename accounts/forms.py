from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
     #  fields = UserCreationForm.Meta.fields +("school", "parentPhoneNumber", "phoneNumber", "profile_pic")
        # fields = UserCreationForm.Meta.fields
        fields = ('username', 'email', 'school', "parentPhoneNumber", "phoneNumber", "profile_pic" ) # new
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

        fields = ('username', 'email', 'school', "parentPhoneNumber", "phoneNumber", "profile_pic" ) # new
