from django.views.generic import UpdateView, ListView
from .models import CustomUser
from .forms import StudentChangeForm, test
from classes.models import Class
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
import random
from home.permissions import AdminPermission
<<<<<<< HEAD
from lectures.models import Lecture
=======
from django.db.models import Q

>>>>>>> 88e062feb5f1667a0762165ac64d57a2c0553cfd


class AdminStudentListView(AdminPermission, ListView):
    queryset = CustomUser.objects.filter(user_type=CustomUser.STUDENT)
    template_name = "accounts/admin-students-list.html"
    paginate_by = 10

    def get_queryset(self):
        try:
            a = self.request.GET.get('account',)
        except KeyError:
            a = None

        if a:

            admin_student_list1 = Q(first_name__contains=a,user_type=CustomUser.STUDENT) 
            admin_student_list2 = Q(username__contains=a,user_type=CustomUser.STUDENT)
            admin_student_list3 = Q(student_class__name__contains=a,user_type=CustomUser.STUDENT)
            q = CustomUser.objects.filter(admin_student_list1 | admin_student_list2 | admin_student_list3)

        else:
            q = CustomUser.objects.filter(user_type=CustomUser.STUDENT)
        return q

class AdminStudentUpdateView(AdminPermission, UpdateView):
    model = CustomUser
    form_class = StudentChangeForm
    template_name = "accounts/admin-student-update.html"
    success_url = reverse_lazy("admin_student_list")

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["classes"] = Class.objects.all()
        ctx["student_user"] = CustomUser.objects.get(id=self.kwargs["pk"])
        ctx["reseted_password"] = ctx["student_user"].check_password(
            ctx["student_user"].random_password)
        ctx["lectures"] = Lecture.objects.all()
        ctx["formo"] = test
        return ctx


def reset_password(request, pk):
    user = CustomUser.objects.get(id=pk)
    user.random_password = random.randint(0, 999999)
    user.set_password(user.random_password)
    user.save()
    return HttpResponseRedirect(reverse_lazy("student_update_view", kwargs={"pk": pk}))




# def index2(request):
#     if request.method == 'POST':

#         # form = InvoiceForm(request.POST)
#         # if form.is_valid():
#         #     instance = form.save(commit=False)
#         #     instance.save()
#         #     return redirect('home2')
#     # else:
#     #     form = InvoiceForm()

#     return HttpResponseRedirect(reverse_lazy("student_update_view", kwargs={"pk": pk}))
