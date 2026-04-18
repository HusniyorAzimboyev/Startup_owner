from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView, CreateView, UpdateView, DeleteView, ListView
)
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from .models import Investor, Investment, PitchDeck, InvestorMeeting
from .forms import InvestorMeetingForm, PitchDeckForm


@login_required
def investor_list(request):
    """List all investors"""
    investors = Investor.objects.filter(verified=True)
    context = {
        'investors': investors,
    }
    return render(request, 'investor/investor_list.html', context)


@login_required
def investor_detail(request, pk):
    """Investor detail view"""
    investor = Investor.objects.get(pk=pk)
    context = {
        'investor': investor,
    }
    return render(request, 'investor/investor_detail.html', context)


class InvestorDashboardView(LoginRequiredMixin, TemplateView):
    """Main investor dashboard showing pitch deck status and meetings"""
    template_name = 'investor/investor_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or create pitch deck
        pitch_deck, created = PitchDeck.objects.get_or_create(
            user=self.request.user
        )
        
        # Get all meetings for the user
        all_meetings = InvestorMeeting.objects.filter(user=self.request.user)
        
        # Separate upcoming and past meetings
        now = timezone.now()
        upcoming_meetings = all_meetings.filter(meeting_date__gt=now).order_by('meeting_date')
        past_meetings = all_meetings.filter(meeting_date__lte=now).order_by('-meeting_date')
        
        # Calculate overall readiness score
        pitch_score = pitch_deck.readiness_score()
        meeting_score = min(len(all_meetings) * 10, 50)  # Max 50 points from meetings
        overall_readiness = min(pitch_score + meeting_score, 100)
        
        context.update({
            'pitch_deck': pitch_deck,
            'upcoming_meetings': upcoming_meetings,
            'past_meetings': past_meetings,
            'overall_readiness': overall_readiness,
            'pitch_score': pitch_score,
            'meeting_count': all_meetings.count(),
            'upcoming_count': upcoming_meetings.count(),
        })
        
        return context


class MeetingCreateView(LoginRequiredMixin, CreateView):
    """Create a new investor meeting"""
    model = InvestorMeeting
    form_class = InvestorMeetingForm
    template_name = 'investor/meeting_form.html'
    success_url = reverse_lazy('investor:dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MeetingUpdateView(LoginRequiredMixin, UpdateView):
    """Update an investor meeting"""
    model = InvestorMeeting
    form_class = InvestorMeetingForm
    template_name = 'investor/meeting_form.html'
    success_url = reverse_lazy('investor:dashboard')

    def get_queryset(self):
        return InvestorMeeting.objects.filter(user=self.request.user)


class MeetingDeleteView(LoginRequiredMixin, DeleteView):
    """Delete an investor meeting"""
    model = InvestorMeeting
    template_name = 'investor/meeting_confirm_delete.html'
    success_url = reverse_lazy('investor:dashboard')

    def get_queryset(self):
        return InvestorMeeting.objects.filter(user=self.request.user)


class PitchDeckUpdateView(LoginRequiredMixin, UpdateView):
    """Update pitch deck information"""
    model = PitchDeck
    form_class = PitchDeckForm
    template_name = 'investor/pitchdeck_form.html'
    success_url = reverse_lazy('investor:dashboard')

    def get_object(self):
        obj, created = PitchDeck.objects.get_or_create(user=self.request.user)
        return obj
