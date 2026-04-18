from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Sum
from django.core.serializers.json import DjangoJSONEncoder
from datetime import timedelta, date
from django.http import JsonResponse
import json
import logging
from .models import ProgressMetric, Milestone, DailyProgress
from .utils import calculate_streak, sync_daily_progress

logger = logging.getLogger(__name__)


@login_required
def progress_dashboard(request):
    """Progress dashboard view"""
    try:
        metrics = ProgressMetric.objects.filter(user=request.user)
        milestones = Milestone.objects.filter(user=request.user)
        context = {
            'metrics': metrics,
            'milestones': milestones,
        }
        return render(request, 'progress/dashboard.html', context)
    except Exception as e:
        logger.exception(f'Error loading progress dashboard for user {request.user.id}: {e}')
        return render(request, 'progress/dashboard.html', {
            'metrics': [],
            'milestones': [],
            'error': 'Failed to load progress data'
        })


@login_required
def metrics_detail(request):
    """Detailed metrics view"""
    try:
        metrics = ProgressMetric.objects.filter(user=request.user)
        context = {
            'metrics': metrics,
        }
        return render(request, 'progress/metrics_detail.html', context)
    except Exception as e:
        logger.exception(f'Error loading metrics for user {request.user.id}: {e}')
        return render(request, 'progress/metrics_detail.html', {
            'metrics': [],
            'error': 'Failed to load metrics'
        })


class ProgressOverviewView(LoginRequiredMixin, TemplateView):
    """Main progress overview with daily tracking and streak"""
    template_name = 'progress/progress.html'

    def get_weekly_data(self, user):
        """Generate 7-day weekly data for chart"""
        try:
            today = date.today()
            result = []
            for i in range(6, -1, -1):
                day = today - timedelta(days=i)
                try:
                    entry = DailyProgress.objects.get(user=user, date=day)
                    rate = entry.completion_rate
                except DailyProgress.DoesNotExist:
                    rate = 0
                result.append({
                    "date": day.strftime("%b %d"),
                    "rate": rate
                })
            return json.dumps(result, cls=DjangoJSONEncoder)
        except Exception as e:
            logger.exception(f'Error generating weekly data for user {user.id}: {e}')
            return json.dumps([])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            # Sync today's progress
            today_progress = sync_daily_progress(self.request.user)
            if today_progress is None:
                # Fallback if sync fails
                today = timezone.now().date()
                today_progress, _ = DailyProgress.objects.get_or_create(
                    user=self.request.user,
                    date=today
                )
            
            # Get last 7 days of progress
            today = timezone.now().date()
            week_ago = today - timedelta(days=6)
            last_7_days = DailyProgress.objects.filter(
                user=self.request.user,
                date__gte=week_ago,
                date__lte=today
            ).order_by('date')
            
            # Calculate streak
            streak = calculate_streak(self.request.user)
            
            # Calculate all-time completed tasks (safe aggregation)
            all_time_data = DailyProgress.objects.filter(
                user=self.request.user
            ).aggregate(total=Sum('tasks_completed'))
            all_time_completed = all_time_data.get('total') or 0
            
            # Calculate this week's average completion rate (safe)
            week_data = list(last_7_days.values_list('completion_rate', flat=True))
            weekly_avg = round(sum(week_data) / len(week_data)) if week_data else 0
            
            # Clamp values to 0-100 range
            weekly_avg = min(max(weekly_avg, 0), 100)
            
            context.update({
                'today_progress': today_progress,
                'last_7_days': last_7_days.order_by('-date'),
                'streak': streak,
                'all_time_completed': all_time_completed,
                'weekly_avg': weekly_avg,
                'weekly_data': self.get_weekly_data(self.request.user),
            })
        except Exception as e:
            logger.exception(f'Error getting progress overview for user {self.request.user.id}: {e}')
            context.update({
                'today_progress': None,
                'last_7_days': [],
                'streak': 0,
                'all_time_completed': 0,
                'weekly_avg': 0,
                'weekly_data': '[]',
                'error': 'Failed to load progress data'
            })
        
        return context
