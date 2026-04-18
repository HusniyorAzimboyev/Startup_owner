from django.db import models
from django.conf import settings
from datetime import date


class ProgressMetric(models.Model):
    """Progress tracking metrics"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progress_metrics'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    target_value = models.DecimalField(max_digits=15, decimal_places=2)
    current_value = models.DecimalField(max_digits=15, decimal_places=2, db_default=0)
    unit = models.CharField(max_length=50, blank=True)
    metric_type = models.CharField(
        max_length=50,
        choices=[
            ('revenue', 'Revenue'),
            ('users', 'Users'),
            ('engagement', 'Engagement'),
            ('custom', 'Custom'),
        ],
        db_default='custom'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def progress_percentage(self):
        """Calculate progress percentage"""
        if self.target_value == 0:
            return 0
        return (self.current_value / self.target_value) * 100


class Milestone(models.Model):
    """Startup milestone tracking"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='milestones'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    target_date = models.DateField()
    achieved_date = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('planned', 'Planned'),
            ('in_progress', 'In Progress'),
            ('achieved', 'Achieved'),
            ('delayed', 'Delayed'),
        ],
        default='planned'
    )
    importance = models.CharField(
        max_length=10,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        default='medium'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-target_date']

    def __str__(self):
        return self.title


class DailyProgress(models.Model):
    """Daily progress tracking"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='daily_progress'
    )
    date = models.DateField(db_default=date.today)
    tasks_completed = models.IntegerField(db_default=0)
    tasks_total = models.IntegerField(db_default=0)
    note = models.TextField(blank=True, help_text="Daily note")

    class Meta:
        unique_together = [['user', 'date']]
        ordering = ['-date']

    @property
    def completion_rate(self):
        """Calculate task completion percentage"""
        if self.tasks_total == 0:
            return 0
        return round((self.tasks_completed / self.tasks_total) * 100)

    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.completion_rate}%"
