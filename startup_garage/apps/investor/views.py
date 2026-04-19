from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView, CreateView, UpdateView, DeleteView, ListView
)
from django.urls import reverse_lazy
from django.utils import timezone
from django.db import IntegrityError
from datetime import timedelta
import logging
from .models import Investor, Investment, PitchDeck, InvestorMeeting
from .forms import InvestorMeetingForm, PitchDeckForm

logger = logging.getLogger(__name__)


@login_required
def investor_list(request):
    """List all verified investors with optimized queries"""
    investors = Investor.objects.filter(verified=True).select_related('user')
    context = {
        'investors': investors,
    }
    return render(request, 'investor/investor_list.html', context)


@login_required
def investor_detail(request, pk):
    """Investor detail view"""
    investor = get_object_or_404(
        Investor.objects.select_related('user'),
        pk=pk
    )
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
        try:
            pitch_deck, created = PitchDeck.objects.get_or_create(
                user=self.request.user
            )
        except IntegrityError:
            logger.exception(f'IntegrityError creating pitch deck for user {self.request.user.id}')
            pitch_deck = PitchDeck.objects.get(user=self.request.user)
        
        # Get all meetings for the user with optimized queries
        all_meetings = InvestorMeeting.objects.filter(
            user=self.request.user
        ).order_by('meeting_date')
        
        # Separate upcoming and past meetings
        now = timezone.now()
        upcoming_meetings = all_meetings.filter(meeting_date__gt=now).order_by('meeting_date')
        past_meetings = all_meetings.filter(meeting_date__lte=now).order_by('-meeting_date')
        
        # Calculate overall readiness score based on pitch deck status and completed meetings
        pitch_score = pitch_deck.readiness_score()
        completed_meetings = all_meetings.filter(status='completed').count()
        completed_followups = all_meetings.filter(status='followup').count()
        meeting_bonus = min(completed_meetings * 10, 30)  # Max +30 from completed meetings
        overall_readiness = min(pitch_score + meeting_bonus, 100)
        total_meetings = all_meetings.count()
        readiness_score = overall_readiness  # Alias for template
        
        context.update({
            'pitch_deck': pitch_deck,
            'upcoming_meetings': upcoming_meetings,
            'past_meetings': past_meetings,
            'overall_readiness': overall_readiness,
            'readiness_score': readiness_score,
            'pitch_score': pitch_score,
            'meeting_count': all_meetings.count(),
            'upcoming_count': upcoming_meetings.count(),
            'completed_meetings': completed_meetings,
            'completed_followups': completed_followups,
            'total_meetings': total_meetings,
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
