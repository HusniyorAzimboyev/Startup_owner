from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class RegisterForm(UserCreationForm):
    """Registration form extending UserCreationForm"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-900 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500',
            'placeholder': 'Email address'
        })
    )
    startup_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-900 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500',
            'placeholder': 'Startup name (optional)'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'startup_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-900 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500',
            'placeholder': 'Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-900 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-900 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500',
            'placeholder': 'Confirm password'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.startup_name = self.cleaned_data.get('startup_name', '')
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile"""
    class Meta:
        model = User
        fields = ('bio', 'startup_name', 'avatar')
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-900 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500',
                'placeholder': 'Tell us about yourself...',
                'rows': 4
            }),
            'startup_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-900 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500',
                'placeholder': 'Startup name'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-900 text-white focus:outline-none focus:border-blue-500',
                'accept': 'image/*'
            }),
        }
