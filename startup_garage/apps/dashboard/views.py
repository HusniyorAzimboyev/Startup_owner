from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import StartupProfile
from apps.tasks.models import Task
from apps.mentor.models import MentorSession
from apps.progress.models import Milestone

import logging

logger = logging.getLogger(__name__)

# Stage-based focus tips
STAGE_TIPS = {
    'idea': 'Focus on validating your idea with potential users. Get feedback before building.',
    'mvp': 'Build the minimum viable product. Ship something to test your assumptions.',
    'growth': 'Scale up your traction. Focus on user acquisition and retention.',
}


class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard view with KPIs and tasks"""
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Optimized query: Get startup profile
        try:
            startup = StartupProfile.objects.select_related('user').only(
                'id', 'user_id', 'name', 'stage', 'kpi_users', 'kpi_revenue',
                'kpi_traction', 'created_at'
            ).get(user=user)
        except StartupProfile.DoesNotExist:
            startup = StartupProfile.objects.create(
                user=user,
                name=f"{user.username}'s Startup"
            )

        # Get today's tasks grouped by status
        today = timezone.now().date()
        tasks = Task.objects.filter(user=user).values('status').annotate(count=Count('id'))
        tasks_by_status = {task['status']: task['count'] for task in tasks}

        # Get latest incomplete mentor session
        mentor_tip = None
        try:
            recent_mentor = MentorSession.objects.filter(
                mentee=user,
                status='scheduled'
            ).select_related('mentor', 'mentor__user').only(
                'title', 'scheduled_at', 'mentor__user__username'
            ).first()
            if recent_mentor:
                mentor_tip = {
                    'title': recent_mentor.title,
                    'mentor': recent_mentor.mentor.user.username,
                    'date': recent_mentor.scheduled_at
                }
        except Exception as e:
            logger.warning(f"Error fetching mentor session: {e}")

        # Get stage-based focus tip
        stage_tip = STAGE_TIPS.get(startup.stage, 'Keep building and learning!')

        # Calculate streak count from milestones (recent achieved)
        streak = Milestone.objects.filter(
            user=user,
            status='achieved',
            achieved_date__gte=today - timedelta(days=30)
        ).count()

        # Get top 3 tasks for the day
        top_tasks = Task.objects.filter(
            user=user
        ).order_by('-priority', 'due_date')[:3]

        context.update({
            'startup': startup,
            'tasks_by_status': tasks_by_status,
            'mentor_tip': mentor_tip,
            'stage_tip': stage_tip,
            'streak': streak,
            'top_tasks': top_tasks,
            'stage_progress': startup.stage_progress(),
        })

        return context


class StartupProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Update startup profile"""
    model = StartupProfile
    fields = ['name', 'stage', 'kpi_users', 'kpi_revenue', 'kpi_traction']
    template_name = 'dashboard/profile_update.html'
    success_url = reverse_lazy('dashboard:index')

    def get_object(self, queryset=None):
        """Get the startup profile for the current user"""
        return StartupProfile.objects.select_related('user').get(user=self.request.user)

    def get_form_class(self):
        """Return the form class"""
        from django.forms import ModelForm
        from .models import StartupProfile

        class StartupProfileForm(ModelForm):
            class Meta:
                model = StartupProfile
                fields = ['name', 'stage', 'kpi_users', 'kpi_revenue', 'kpi_traction']
                widgets = {
                    'name': __import__('django.forms', fromlist=['TextInput']).TextInput(attrs={
                        'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-900 text-white',
                        'placeholder': 'Startup name'
                    }),
                    'stage': __import__('django.forms', fromlist=['Select']).Select(attrs={
                        'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-900 text-white',
                    }),
                    'kpi_users': __import__('django.forms', fromlist=['NumberInput']).NumberInput(attrs={
                        'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-900 text-white',
                        'placeholder': 'Number of users'
                    }),
                    'kpi_revenue': __import__('django.forms', fromlist=['NumberInput']).NumberInput(attrs={
                        'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-900 text-white',
                        'placeholder': 'Revenue ($)'
                    }),
                    'kpi_traction': __import__('django.forms', fromlist=['Textarea']).Textarea(attrs={
                        'class': 'w-full px-4 py-2 border border-gray-700 rounded-lg bg-gray-900 text-white',
                        'placeholder': 'Traction details',
                        'rows': 4
                    }),
                }

        return StartupProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['startup'] = self.object
        return context

