from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class StartupProfile(models.Model):
    """Startup profile model with KPIs"""
    STAGE_CHOICES = [
        ('idea', 'Idea'),
        ('mvp', 'MVP'),
        ('growth', 'Growth'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='startup_profile'
    )
    name = models.CharField(max_length=200)
    stage = models.CharField(
        max_length=20,
        choices=STAGE_CHOICES,
        db_default='idea'
    )
    kpi_users = models.IntegerField(db_default=0)
    kpi_revenue = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        db_default=0
    )
    kpi_traction = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Startup Profile'
        verbose_name_plural = 'Startup Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Startup: {self.name}"

    def stage_progress(self):
        """Calculate stage progress percentage"""
        return {
            'idea': 33,
            'mvp': 66,
            'growth': 100,
        }.get(self.stage, 0)

    def stage_label(self):
        """Get human-readable stage label"""
        return dict(self.STAGE_CHOICES).get(self.stage, 'Unknown')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_startup_profile(sender, instance, created, **kwargs):
    """Auto-create StartupProfile when user is created"""
    if created:
        StartupProfile.objects.get_or_create(
            user=instance,
            defaults={
                'name': f"{instance.username}'s Startup",
            }
        )

