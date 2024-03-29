from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, StudentPayment
from lectures.models import Lecture, StudentLectureMakeup

# DataFlair #Custom_Validator


def check_size(value):
    if len(value) < 11 and value.isdigit():
        raise forms.ValidationError("الرقم الذي ادخلته غير صحيح")


class CustomUserCreationForm(UserCreationForm):
    username = forms.EmailField(label="الايميل")
    first_name = forms.CharField(
        validators=[check_size, ], label="الأسم ثلاثي")
    parentPhoneNumber = forms.CharField(
        validators=[check_size, ], label="رقم موبايل ولي الأمر")
    phoneNumber = forms.CharField(
        validators=[check_size, ], label=" رقم موبايل الطالب")
    school = forms.CharField(validators=[check_size, ], label="المدرسة")
    # profile_pic = forms.ImageField(validators=[check_size, ],required=False, label="صوره الطالب")
    password1 = forms.CharField(widget=forms.PasswordInput(), validators=[
                                check_size, ], label="كلمه السر")
    password2 = forms.CharField(widget=forms.PasswordInput(), validators=[
                                check_size, ], label="إعادة كلمه السر")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'school',
                  "parentPhoneNumber", "phoneNumber", 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

        fields = ('username', 'first_name', 'last_name', 'email',
                  'school', "parentPhoneNumber", "phoneNumber", "profile_pic")


class StudentChangeForm(forms.ModelForm):
    # TRUE_FALSE_CHOICES = (
    #     (True, 'مفعل'),
    #     (False, 'غير مفعل')
    # )
    # student_class = forms.CharField(label="المجموعة")
    # student_is_active = forms.ChoiceField(
    #     choices=TRUE_FALSE_CHOICES, label="التفعيل")

    class Meta:
        model = CustomUser
        fields = ('student_class', )



class test(forms.ModelForm):
    lecture = forms.ModelChoiceField(queryset=Lecture.objects.all())

    class Meta:
        model = StudentLectureMakeup
        fields = ("lecture",)


class MyProfileData(forms.ModelForm):
    username = forms.EmailField(label="الايميل")
    parentPhoneNumber = forms.CharField(
        validators=[check_size, ], label="رقم موبايل ولي الأمر")
    phoneNumber = forms.CharField(
        validators=[check_size, ], label=" رقم موبايل الطالب")
    school = forms.CharField(validators=[check_size, ], label="المدرسة")
    # profile_pic= forms.ImageField(validators=[check_size, ],required=False, label="صوره الطالب")

    class Meta:
        model = CustomUser
        fields = ('username', 'school', 'parentPhoneNumber', 'phoneNumber')


class AdminMyProfileData(forms.ModelForm):
    username = forms.EmailField(label="الايميل")
    first_name = forms.CharField(
        validators=[check_size, ], label="الأسم ثلاثي")
    parentPhoneNumber = forms.CharField(
        validators=[check_size, ], label="رقم موبايل ولي الأمر")
    phoneNumber = forms.CharField(
        validators=[check_size, ], label=" رقم موبايل الطالب")
    school = forms.CharField(validators=[check_size, ], label="المدرسة")

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'school',
                  'parentPhoneNumber', 'phoneNumber')


class AdminStudentPayment(forms.ModelForm):
    paid_at = forms.DateField(
        label="تاريخ الدفع", widget=forms.DateInput(format='%Y-%m-%d'))
    number_available_lectures = forms.IntegerField(
        label="عدد المحاضرات المتاح للطالب حضورها")
    notes = forms.CharField(widget=forms.Textarea,
                            label="الملاحظات", required=False)

    class Meta:
        model = StudentPayment
        fields = ('number_available_lectures', 'paid_at', 'notes',)


class AdminStudentPaymentUpdateForm(forms.ModelForm):
    notes = forms.CharField(widget=forms.Textarea,
                            label="الملاحظات", required=False)

    class Meta:
        model = StudentPayment
        fields = ('notes',)
