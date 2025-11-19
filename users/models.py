from django.db import models
from django.conf import settings
from .utils import user_audio

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, blank=True)
    audio = models.FileField(upload_to=user_audio, null=True, blank=True)
    audio_uploaded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Profile: {self.user.username}"

class AudioVersion(models.Model):
    profile = models.ForeignKey(UserProfile, related_name='versions', on_delete=models.CASCADE)
    file = models.FileField(upload_to='audio/versions/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    original_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"AudioVersion {self.profile.user.username} @ {self.uploaded_at}"

