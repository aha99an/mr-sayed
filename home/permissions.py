from django.shortcuts import redirect
from accounts.models import CustomUser


class StudentPermission(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if self.request.user.user_type == CustomUser.STUDENT and self.request.user.student_is_active is True:
                return super().dispatch(request, *args, **kwargs)
            return redirect("account_not_active")
        return redirect('login')


class AdminPermission(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if self.request.user.user_type == CustomUser.ADMIN:
                return super().dispatch(request, *args, **kwargs)
        return redirect('login')

class AuthenticatedPermission(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect('login')
