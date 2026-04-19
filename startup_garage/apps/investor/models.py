from django.db import models
from django.conf import settings
from django.utils import timezone


class Investor(models.Model):
    """Investor profile model"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='investor_profile'
    )
    investment_range = models.CharField(
        max_length=50,
        choices=[
            ('seed', 'Seed Stage'),
            ('series_a', 'Series A'),
            ('series_b', 'Series B'),
            ('growth', 'Growth Stage'),
        ],
        blank=True
    )
    industries = models.TextField(help_text="Interest in industries")
    portfolio_link = models.URLField(blank=True, null=True)
    verified = models.BooleanField(db_default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Investor: {self.user.get_full_name()}"


class Investment(models.Model):
    """Investment record"""
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name='investments')
    startup_founder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_investments'
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, db_default=0)
    date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('interested', 'Interested'),
            ('negotiating', 'Negotiating'),
            ('completed', 'Completed'),
            ('declined', 'Declined'),
        ],
        db_default='interested'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Investment: ${self.amount}"


class PitchDeck(models.Model):
    """Pitch deck model for investor presentations"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pitch_deck'
    )
    version = models.CharField(max_length=20, db_default="v1.0")
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('review', 'In Review'),
            ('ready', 'Ready'),
        ],
        db_default='draft'
    )
    notes = models.TextField(
        blank=True,
        help_text="Internal notes about the pitch deck"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pitch Deck'
        verbose_name_plural = 'Pitch Decks'

    def __str__(self):
        return f"Pitch Deck ({self.version}) - {self.user.username}"

    def readiness_score(self):
        """Calculate readiness score based on status"""
        scores = {
            'draft': 25,
            'review': 60,
            'ready': 100,
        }
        return scores.get(self.status, 0)


class InvestorMeeting(models.Model):
    """Investor meeting records and tracking"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='investor_meetings'
    )
    investor_name = models.CharField(max_length=100)
    company = models.CharField(
        max_length=100,
        blank=True,
        help_text="Investor's company name"
    )
    meeting_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('followup', 'Follow-up'),
            ('passed', 'Passed'),
        ],
        db_default='scheduled'
    )
    notes = models.TextField(
        blank=True,
        help_text="Meeting notes and outcomes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['meeting_date']

    def __str__(self):
        return f"Meeting with {self.investor_name} - {self.meeting_date.strftime('%Y-%m-%d')}"

    def is_upcoming(self):
        """Check if meeting is in the future"""
        from django.utils import timezone
        return self.meeting_date > timezone.now()


class InvestorMessage(models.Model):
    """Messages between founders and investors"""
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_investor_messages'
    )
    investor = models.ForeignKey(
        Investor,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(db_default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message to {self.investor.user.get_full_name()} from {self.sender.get_full_name()}"
