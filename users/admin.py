from django.contrib import admin
from .models import UserProfile, AudioVersion

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'audio_uploaded_at')

@admin.register(AudioVersion)
class AudioVersionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'original_name', 'uploaded_at')
