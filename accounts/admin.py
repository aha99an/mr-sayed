from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, StudentPayment


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
    (None, {'fields': ('examStudentGrade', 'homeWorkAnswerd', 'examGrade', 'user_type', 'student_class', 'student_is_active')}),)
    list_display = ("id", 'username', "first_name", "school",
                    "parentPhoneNumber", "phoneNumber", "student_class")
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentPayment)
