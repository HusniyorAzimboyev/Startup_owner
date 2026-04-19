from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta, time
import logging
from .models import Mentor, MentorSession, MentorFeedback
from .forms import MentorFeedbackForm

logger = logging.getLogger(__name__)


@login_required
def session_planner(request, mentor_id=None):
    """Session planner with calendar view - shows available time slots"""
    selected_mentor = None
    
    if mentor_id:
        selected_mentor = get_object_or_404(
            Mentor.objects.select_related('user'),
            pk=mentor_id,
            verified=True
        )
        mentors = [selected_mentor]
    else:
        mentors = Mentor.objects.filter(verified=True).select_related('user')
    
    # Generate next 7 days of available slots (optimized for performance)
    available_slots = []
    start_date = datetime.now().date()
    mentor_ids = [m.id for m in mentors]
    
    # Get all booked sessions for next 30 days in one query
    booked_sessions = MentorSession.objects.filter(
        mentor_id__in=mentor_ids,
        scheduled_at__gte=datetime.now(),
        scheduled_at__lt=datetime.combine(start_date + timedelta(days=7), time(23, 59)),
        status__in=['scheduled', 'completed']
    ).values_list('mentor_id', 'scheduled_at__date', 'scheduled_at__hour')
    
    booked_set = set(booked_sessions)
    
    for mentor_obj in mentors:
        for i in range(7):  # Only next 7 days for faster loading
            current_date = start_date + timedelta(days=i)
            
            # Skip weekends
            if current_date.weekday() >= 5:
                continue
            
            # Generate 1-hour slots from 9 AM to 6 PM
            for hour in range(9, 18):
                slot_time = datetime.combine(current_date, time(hour, 0))
                
                # Check if slot is in the future
                if slot_time > datetime.now():
                    # Check if already booked using the set
                    is_booked = (mentor_obj.id, current_date, hour) in booked_set
                    
                    if not is_booked:
                        available_slots.append({
                            'mentor': mentor_obj,
                            'datetime': slot_time,
                            'date_str': current_date.strftime('%A, %B %d'),
                            'time_str': f"{hour}:00",
                            'hour': hour,
                        })
    
    context = {
        'mentors': mentors,
        'available_slots': available_slots,
        'selected_mentor': selected_mentor,
    }
    return render(request, 'mentor/session_planner.html', context)


@login_required
@require_http_methods(["POST"])
def book_session(request):
    """Book a mentor session"""
    try:
        mentor_id = request.POST.get('mentor_id')
        session_datetime_str = request.POST.get('datetime')
        title = request.POST.get('title', 'Mentoring Session')
        description = request.POST.get('description', '')
        
        mentor = get_object_or_404(Mentor, pk=mentor_id, verified=True)
        session_datetime = datetime.fromisoformat(session_datetime_str)
        
        # Check if slot is available
        existing = MentorSession.objects.filter(
            mentor=mentor,
            scheduled_at=session_datetime,
            status__in=['scheduled', 'completed']
        ).exists()
        
        if existing:
            return JsonResponse({
                'success': False,
                'error': 'This time slot is no longer available'
            }, status=400)
        
        # Create session
        session = MentorSession.objects.create(
            mentor=mentor,
            mentee=request.user,
            title=title,
            description=description,
            scheduled_at=session_datetime,
            duration_minutes=60,
            status='scheduled'
        )
        
        return JsonResponse({
            'success': True,
            'session_id': session.id,
            'message': f'Session booked with {mentor.user.get_full_name()} on {session_datetime.strftime("%A, %B %d at %I:%M %p")}'
        })
    except Exception as e:
        logger.exception(f'Error booking session for user {request.user.id}: {e}')
        return JsonResponse({
            'success': False,
            'error': 'Failed to book session'
        }, status=500)


@login_required
def mentor_list(request):
    """List all verified mentors with optimized queries"""
    mentors = Mentor.objects.filter(verified=True).select_related('user')
    context = {
        'mentors': mentors,
    }
    return render(request, 'mentor/mentor_list.html', context)


@login_required
def mentor_detail(request, pk):
    """Mentor detail view"""
    mentor = get_object_or_404(
        Mentor.objects.select_related('user'),
        pk=pk
    )
    context = {
        'mentor': mentor,
    }
    return render(request, 'mentor/mentor_detail.html', context)


class FeedbackListView(LoginRequiredMixin, ListView):
    """List all feedback for the current user"""
    model = MentorFeedback
    template_name = 'mentor/feedback_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 20
    max_paginate_by = 100  # Prevent DoS with excessive page sizes

    def get_queryset(self):
        return MentorFeedback.objects.filter(
            user=self.request.user
        ).select_related('mentor', 'mentor__user').order_by('-session_date')


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    """Create new feedback entry"""
    model = MentorFeedback
    form_class = MentorFeedbackForm
    template_name = 'mentor/feedback_form.html'
    success_url = reverse_lazy('mentor:feedback-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FeedbackDetailView(LoginRequiredMixin, DetailView):
    """View feedback details"""
    model = MentorFeedback
    template_name = 'mentor/feedback_detail.html'
    context_object_name = 'feedback'

    def get_queryset(self):
        return MentorFeedback.objects.filter(
            user=self.request.user
        ).select_related('mentor', 'mentor__user')


class FeedbackUpdateView(LoginRequiredMixin, UpdateView):
    """Update feedback entry"""
    model = MentorFeedback
    form_class = MentorFeedbackForm
    template_name = 'mentor/feedback_form.html'
    success_url = reverse_lazy('mentor:feedback-list')

    def get_queryset(self):
        return MentorFeedback.objects.filter(user=self.request.user)


@login_required
@require_http_methods(["POST"])
def complete_next_step(request, pk):
    """Toggle is_completed status for feedback"""
    try:
        feedback = get_object_or_404(MentorFeedback, pk=pk, user=request.user)
        feedback.is_completed = not feedback.is_completed
        feedback.save(update_fields=['is_completed'])
        return JsonResponse({
            'success': True,
            'is_completed': feedback.is_completed,
        })
    except Exception as e:
        logger.exception(f'Error completing mentor step {pk} for user {request.user.id}: {e}')
        return JsonResponse({
            'success': False,
            'error': 'Failed to update step status'
        }, status=500)
