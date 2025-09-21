from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import uuid
from django.utils import timezone
import os

def user_profile_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/<id>/<filename>
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('users', str(instance.id), 'profile', filename)

class CustomUser(AbstractUser):
    """Custom user model that extends the default User model with additional fields."""
    profile_image = models.ImageField(
        _('profile image'),
        upload_to=user_profile_image_path,
        null=True,
        blank=True,
        help_text=_('User profile image')
    )
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'  # Keep using the same table name
        
    def __str__(self):
        return self.username

class EmailVerification(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        expiration = self.created_at + timezone.timedelta(hours=24)
        return timezone.now() > expiration