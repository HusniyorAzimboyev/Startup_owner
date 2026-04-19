from django import forms
from .models import StartupProfile


class StartupProfileForm(forms.ModelForm):
    """Form for updating startup profile"""
    
    class Meta:
        model = StartupProfile
        fields = ['name', 'stage', 'kpi_users', 'kpi_revenue', 'kpi_traction']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-900 text-white',
                'placeholder': 'Startup name'
            }),
            'stage': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-900 text-white',
            }),
            'kpi_users': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-900 text-white',
                'placeholder': 'Number of users'
            }),
            'kpi_revenue': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-900 text-white',
                'placeholder': 'Revenue ($)'
            }),
            'kpi_traction': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-900 text-white',
                'placeholder': 'Traction details',
                'rows': 4
            }),
        }
