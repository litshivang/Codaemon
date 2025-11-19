from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile, AudioVersion
from django.conf import settings

User = get_user_model()

class AudioVersionSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = AudioVersion
        fields = ['id', 'file_url', 'uploaded_at', 'original_name']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    audio_url = serializers.SerializerMethodField()
    versions = AudioVersionSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'full_name', 'audio_url', 'audio_uploaded_at', 'versions']

    def get_audio_url(self, obj):
        request = self.context.get('request')
        if obj.audio:
            if request:
                return request.build_absolute_uri(obj.audio.url)
            return obj.audio.url
        return None
