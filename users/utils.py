import uuid
from django.utils import timezone

def user_audio(instance, filename):
    ext = filename.split('.')[-1] if '.' in filename else 'bin'
    uid = uuid.uuid4().hex
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    return f'audio/user_{instance.user.id}/{timestamp}_{uid}.{ext}'