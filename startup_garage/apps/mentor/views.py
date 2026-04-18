from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
import logging
from .models import Mentor, MentorSession, MentorFeedback
from .forms import MentorFeedbackForm

logger = logging.getLogger(__name__)


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
