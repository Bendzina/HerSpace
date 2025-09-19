# No custom user model. Using Django's default User model.
# users/models.py
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone

class EmailVerification(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        expiration = self.created_at + timezone.timedelta(hours=24)
        return timezone.now() > expiration