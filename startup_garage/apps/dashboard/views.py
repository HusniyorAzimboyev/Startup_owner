from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import StartupProfile
from .forms import StartupProfileForm
from apps.tasks.models import Task
from apps.mentor.models import MentorFeedback
from apps.progress.models import Milestone
from apps.progress.utils import calculate_streak, sync_daily_progress

import logging

logger = logging.getLogger(__name__)

# Stage-based focus tips
STAGE_TIPS = {
    "idea": "🎯 Validate your idea — interview 10 potential users this week",
    "mvp": "💰 Get your first paying customer — launch a pilot offer",
    "growth": "📈 Double down on what's working — optimize your top channel",
}


class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard view with KPIs and tasks"""
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Sync today's progress first
        try:
            sync_daily_progress(user)
        except Exception as e:
            logger.exception(f'Error syncing daily progress for user {user.id}: {e}')

        # Optimized query: Get startup profile
        try:
            startup = StartupProfile.objects.select_related('user').only(
                'id', 'user_id', 'name', 'stage', 'kpi_users', 'kpi_revenue',
                'kpi_traction', 'created_at'
            ).get(user=user)
        except StartupProfile.DoesNotExist:
            try:
                startup = StartupProfile.objects.create(
                    user=user,
                    name=f"{user.username}'s Startup"
                )
            except Exception as e:
                logger.exception(f'Error creating startup profile for user {user.id}: {e}')
                raise

        # Get task counts by status
        tasks = Task.objects.filter(user=user)
        context["todo_count"] = tasks.filter(status="todo").count()
        context["in_progress_count"] = tasks.filter(status="in_progress").count()
        context["done_count"] = tasks.filter(status="done").count()
        context["total_tasks"] = tasks.count()

        # Get latest incomplete mentor feedback with next step
        latest_step = MentorFeedback.objects.filter(
            user=user,
            is_completed=False,
            next_step__gt=""  # Excludes empty next_step
        ).order_by("-session_date").first()

        context["latest_mentor_step"] = latest_step

        # Get stage-based focus tip
        stage_tip = STAGE_TIPS.get(startup.stage, STAGE_TIPS["idea"])

        # Calculate streak from DailyProgress entries
        try:
            streak = calculate_streak(user)
        except Exception as e:
            logger.exception(f'Error calculating streak for user {user.id}: {e}')
            streak = 0

        # Get top 3 tasks for the day
        top_tasks = Task.objects.filter(
            user=user
        ).order_by('-priority', 'due_date')[:3]

        context.update({
            'startup': startup,
            'stage_tip': stage_tip,
            'streak': streak,
            'top_tasks': top_tasks,
            'stage_progress': startup.stage_progress(),
        })

        return context


class StartupProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Update startup profile"""
    model = StartupProfile
    form_class = StartupProfileForm
    template_name = 'dashboard/profile_update.html'
    success_url = reverse_lazy('dashboard:index')

    def get_object(self, queryset=None):
        """Get the startup profile for the current user"""
        return StartupProfile.objects.select_related('user').get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['startup'] = self.object
        return context

