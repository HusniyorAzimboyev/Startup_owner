from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator


class User(AbstractUser):
    """Custom user model for startup_garage"""
    bio = models.TextField(blank=True, db_default="")
    startup_name = models.CharField(
        max_length=100,
        blank=True,
        db_default=""
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        db_default="",
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'gif'],
                message='Only JPG, PNG, and GIF image files are allowed'
            )
        ],
        help_text='Maximum file size: 5MB. Formats: JPG, PNG, GIF'
    )
    is_mentor = models.BooleanField(db_default=False)
    is_investor = models.BooleanField(db_default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
