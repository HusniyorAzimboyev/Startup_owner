from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import User
from .forms import RegisterForm, ProfileUpdateForm


@login_not_required
def register_view(request):
    """Legacy register view - replaced by RegisterView"""
    pass


class RegisterView(CreateView):
    """User registration view"""
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard:index')

    def dispatch(self, request, *args, **kwargs):
        """Redirect authenticated users to dashboard"""
        if request.user.is_authenticated:
            return redirect('dashboard:index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Auto-login user after successful registration"""
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs


class ProfileView(LoginRequiredMixin, UpdateView):
    """User profile update view"""
    model = User
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        """Return the current user"""
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

