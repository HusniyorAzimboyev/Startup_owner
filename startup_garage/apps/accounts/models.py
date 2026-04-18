from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Value


class User(AbstractUser):
    """Custom user model for startup_garage"""
    bio = models.TextField(blank=True, null=True)
    startup_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default=""
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_mentor = models.BooleanField(default=False)
    is_investor = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
