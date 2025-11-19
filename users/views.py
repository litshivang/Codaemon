# 1. library
import os
import mimetypes

# 2. Third-party
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from mutagen import File as MutagenFile
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

# 3. app
from .models import UserProfile, AudioVersion
from .serializers import UserProfileSerializer


MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_MIME = ['audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/x-wav', 'audio/x-m4a']

User = get_user_model()


# UserProfile
class UserProfileViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser,)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        serializer = UserProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='audio', parser_classes=[MultiPartParser, FormParser])
    def upload_audio(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        profile, _ = UserProfile.objects.get_or_create(user=user)

        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'detail': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        if file_obj.size > MAX_UPLOAD_SIZE:
            return Response({'detail': f'File too large. Max size is {MAX_UPLOAD_SIZE} bytes.'}, status=status.HTTP_400_BAD_REQUEST)

        mime_type, _ = mimetypes.guess_type(file_obj.name)
        if mime_type not in ALLOWED_MIME:
            # Try reading file header via mutagen
            try:
                mf = MutagenFile(file_obj)
                if not mf:
                    return Response({'detail': 'Unsupported audio format.'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response({'detail': 'Unsupported audio format.'}, status=status.HTTP_400_BAD_REQUEST)

        # Save version
        original_name = file_obj.name
        version = AudioVersion(profile=profile, original_name=original_name)
        version.file.save(file_obj.name, file_obj)
        version.save()

        # Remove previous main audio if exists (we keep versions)
        if profile.audio:
            try:
                old = profile.audio.path
                # don't delete versions
                # os.remove(old)  # keeping old file as part of versions
            except Exception:
                pass

        # Set profile audio to new file (copy version to profile.audio)
        profile.audio = version.file
        profile.audio_uploaded_at = version.uploaded_at
        profile.save()

        serializer = UserProfileSerializer(profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='audio')
    def delete_audio(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(UserProfile, user=user)
        # Archive current audio as a version if any (already stored in versions)
        if profile.audio:
            try:
                profile.audio.delete(save=False)
            except Exception:
                pass
        profile.audio = None
        profile.audio_uploaded_at = None
        profile.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='audio/restore/(?P<version_id>[^/.]+)')
    def restore_audio_version(self, request, pk=None, version_id=None):
        """
        Restore a previous audio version as the current profile audio.
        """
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(UserProfile, user=user)

        version = get_object_or_404(AudioVersion, pk=version_id, profile=profile)

        # Set profile.audio to the version file
        profile.audio = version.file
        profile.audio_uploaded_at = version.uploaded_at
        profile.save()

        serializer = UserProfileSerializer(profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# Dashboard
def dashboard_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return render(request, 'users/user_dashboard.html', {'profile': profile}) 

# Landing Page
def landing_page(request):
    users = User.objects.all()
    return render(request, 'users/landing.html', {'users': users})

