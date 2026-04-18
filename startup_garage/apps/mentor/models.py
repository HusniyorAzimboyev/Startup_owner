from django.db import models
from django.conf import settings


class Mentor(models.Model):
    """Mentor model"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mentor_profile'
    )
    expertise = models.TextField(help_text="Areas of expertise")
    availability = models.CharField(
        max_length=50,
        choices=[
            ('available', 'Available'),
            ('limited', 'Limited Availability'),
            ('unavailable', 'Unavailable'),
        ],
        default='available'
    )
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Mentor: {self.user.get_full_name()}"


class MentorSession(models.Model):
    """Mentor session model"""
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='sessions')
    mentee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mentor_sessions'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    scheduled_at = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='scheduled'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scheduled_at']

    def __str__(self):
        return f"Session: {self.title}"


class MentorFeedback(models.Model):
    """Mentor feedback/followup model"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mentor_feedbacks'
    )
    mentor_name = models.CharField(max_length=100)
    session_date = models.DateField()
    comment = models.TextField(help_text="What was discussed in the session")
    recommendation = models.TextField(blank=True, help_text="Mentor's recommendation")
    next_step = models.TextField(blank=True, help_text="Next action item")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-session_date']

    def __str__(self):
        return f"Feedback from {self.mentor_name} - {self.session_date}"
