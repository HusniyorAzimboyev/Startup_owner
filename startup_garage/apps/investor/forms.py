from django import forms
from .models import InvestorMeeting, PitchDeck


class InvestorMeetingForm(forms.ModelForm):
    """Form for creating/editing investor meetings"""
    
    class Meta:
        model = InvestorMeeting
        fields = ['investor_name', 'company', 'meeting_date', 'status', 'notes']
        widgets = {
            'investor_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500',
                'placeholder': 'Investor name',
            }),
            'company': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500',
                'placeholder': 'Company (optional)',
            }),
            'meeting_date': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500',
                'type': 'datetime-local',
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 h-32 resize-none',
                'placeholder': 'Meeting notes and outcomes',
                'rows': 4,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['investor_name'].label = 'Investor Name'
        self.fields['company'].label = 'Company'
        self.fields['meeting_date'].label = 'Meeting Date & Time'
        self.fields['status'].label = 'Status'
        self.fields['notes'].label = 'Notes'


class PitchDeckForm(forms.ModelForm):
    """Form for updating pitch deck"""
    
    class Meta:
        model = PitchDeck
        fields = ['version', 'status', 'notes']
        widgets = {
            'version': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500',
                'placeholder': 'e.g., v1.0, v2.1',
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 h-24 resize-none',
                'placeholder': 'Internal notes about the pitch deck',
                'rows': 3,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['version'].label = 'Pitch Deck Version'
        self.fields['status'].label = 'Status'
        self.fields['notes'].label = 'Internal Notes'
