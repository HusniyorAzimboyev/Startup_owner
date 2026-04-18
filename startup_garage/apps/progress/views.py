from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
import json
from .models import ProgressMetric, Milestone, DailyProgress
from .utils import calculate_streak, sync_daily_progress


@login_required
def progress_dashboard(request):
    """Progress dashboard view"""
    metrics = ProgressMetric.objects.filter(user=request.user)
    milestones = Milestone.objects.filter(user=request.user)
    context = {
        'metrics': metrics,
        'milestones': milestones,
    }
    return render(request, 'progress/dashboard.html', context)


@login_required
def metrics_detail(request):
    """Detailed metrics view"""
    metrics = ProgressMetric.objects.filter(user=request.user)
    context = {
        'metrics': metrics,
    }
    return render(request, 'progress/metrics_detail.html', context)


class ProgressOverviewView(LoginRequiredMixin, TemplateView):
    """Main progress overview with daily tracking and streak"""
    template_name = 'progress/progress.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Sync today's progress
        today_progress = sync_daily_progress(self.request.user)
        
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
        
        # Calculate all-time completed tasks
        all_time_completed = DailyProgress.objects.filter(
            user=self.request.user
        ).aggregate(total=sum('tasks_completed'))['total'] or 0
        
        # Calculate this week's average completion rate
        week_data = last_7_days.values_list('completion_rate', flat=True)
        weekly_avg = round(sum(week_data) / len(week_data)) if week_data else 0
        
        # Prepare data for Chart.js (ensure all 7 days are present)
        chart_data = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            progress = last_7_days.filter(date=date).first()
            chart_data.append({
                'date': date.strftime('%a'),  # Mon, Tue, etc
                'rate': progress.completion_rate if progress else 0,
                'completed': progress.tasks_completed if progress else 0,
                'total': progress.tasks_total if progress else 0,
            })
        
        context.update({
            'today_progress': today_progress,
            'last_7_days': last_7_days.order_by('-date'),
            'streak': streak,
            'all_time_completed': all_time_completed,
            'weekly_avg': weekly_avg,
            'chart_data': json.dumps(chart_data),
        })
        
        return context
