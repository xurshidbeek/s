from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

from django.http import HttpResponseForbidden

from django.shortcuts import  redirect

from django.urls import  reverse_lazy
from app_users.forms import UserRegistrationForm

User = get_user_model()

class RegistrationView(CreateView):
    model = User
    template_name = 'app_users/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')


def logout_view(request):
    logout(request)
    return redirect('login')

class UserListView(PermissionRequiredMixin, ListView):
    model = User
    template_name = 'app_users/users_list.html'
    context_object_name = 'users'
    permission_required = 'auth.view_user'

    def dispatch(self, request, *args, **kwargs):
        # Faqat adminlar kirishiga ruxsat beriladi
        if not request.user.is_staff:
            return HttpResponseForbidden("<h1>Access Denied: Admins only</h1>")
        return super().dispatch(request, *args, **kwargs)

