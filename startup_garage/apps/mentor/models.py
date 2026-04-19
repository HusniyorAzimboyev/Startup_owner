from django.db import models
from django.conf import settings
from django.utils import timezone


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
        db_default='available'
    )
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    verified = models.BooleanField(db_default=False)
    created_at = models.DateTimeField(default=timezone.now)
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
    duration_minutes = models.IntegerField(db_default=60)
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        db_default='scheduled'
    )
    created_at = models.DateTimeField(default=timezone.now)

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
    mentor = models.ForeignKey(
        Mentor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='feedbacks_given'
    )
    mentor_name = models.CharField(max_length=100, blank=True)  # Fallback if mentor deleted
    session_date = models.DateField()
    comment = models.TextField(help_text="What was discussed in the session")
    recommendation = models.TextField(blank=True, help_text="Mentor's recommendation")
    next_step = models.TextField(blank=True, help_text="Next action item")
    is_completed = models.BooleanField(db_default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-session_date']

    def __str__(self):
        mentor = self.mentor.user.get_full_name() if self.mentor else self.mentor_name
        return f"Feedback from {mentor} - {self.session_date}"
