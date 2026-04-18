from django import forms
from .models import MentorFeedback


class MentorFeedbackForm(forms.ModelForm):
    """Form for creating/editing mentor feedback"""
    
    class Meta:
        model = MentorFeedback
        fields = ['mentor_name', 'session_date', 'comment', 'recommendation', 'next_step']
        widgets = {
            'mentor_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500',
                'placeholder': 'Mentor\'s name',
            }),
            'session_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500',
                'type': 'date',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 h-32 resize-none',
                'placeholder': 'What was discussed in this session?',
                'rows': 4,
            }),
            'recommendation': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 h-24 resize-none',
                'placeholder': 'Mentor\'s recommendation (optional)',
                'rows': 3,
            }),
            'next_step': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 h-24 resize-none',
                'placeholder': 'What\'s the next action item? (optional)',
                'rows': 3,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mentor_name'].label = 'Mentor Name'
        self.fields['session_date'].label = 'Session Date'
        self.fields['comment'].label = 'What was discussed?'
        self.fields['recommendation'].label = 'Recommendation'
        self.fields['next_step'].label = 'Next Step'
