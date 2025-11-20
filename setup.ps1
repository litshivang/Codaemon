# 1. Set variables
$venvDir = "venv"
$python = "python"  # Use full path if multiple Python versions
$sampleAudioDir = ".\users\static\audio"
$users = @(
    @{username="testuser1"; email="user1@example.com"; password="Password123"; audio="1.mp3"},
    @{username="testuser2"; email="user2@example.com"; password="Password123"; audio="2.wav"},
    @{username="testuser3"; email="user3@example.com"; password="Password123"; audio=$null}
)
$superUser = @{username="admin"; email="admin@example.com"; password="Admin123"}

# 2. Create virtual environment
if (!(Test-Path $venvDir)) {
    Write-Host "Creating virtual environment..."
    & $python -m venv $venvDir
}

# 3. Activate virtual environment
Write-Host "Activating virtual environment..."
$activateScript = Join-Path $venvDir "Scripts\Activate.ps1"
. $activateScript

# 4. Upgrade pip and install requirements
Write-Host "Upgrading pip and installing packages..."
& $python -m pip install --upgrade pip
& $python -m pip install -r requirements.txt

# 5. Apply migrations
Write-Host "Running migrations..."
& $python manage.py migrate

# 6. Create superuser (non-interactive)
Write-Host "Creating superuser..."
$superuserExists = & $python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(username='$($superUser.username)').exists())"
if ($superuserExists -eq "False") {
    & $python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(username='$($superUser.username)', email='$($superUser.email)', password='$($superUser.password)')"
    Write-Host "Superuser created: $($superUser.username) / $($superUser.password)"
} else {
    Write-Host "Superuser already exists."
}

# 7. Create test users and upload sample audio
Write-Host "Creating test users and uploading sample audio..."
foreach ($u in $users) {
    & $python manage.py shell -c @"
import os
from django.core.files import File
from django.contrib.auth import get_user_model
from users.models import UserProfile, AudioVersion

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Codaemon.settings')  # ensure settings loaded

User = get_user_model()

user, created = User.objects.get_or_create(username=r'$($u.username)', defaults={'email':r'$($u.email)'})
if created:
    user.set_password(r'$($u.password)')
    user.save()

profile, _ = UserProfile.objects.get_or_create(user=user)

audio_file_name = r'$($u.audio)' if '$($u.audio)' != 'None' else None
if audio_file_name:
    sample_audio_path = os.path.join(r'$sampleAudioDir', audio_file_name)
    if os.path.exists(sample_audio_path):
        with open(sample_audio_path, 'rb') as f:
            version = AudioVersion(profile=profile, original_name=os.path.basename(sample_audio_path))
            version.file.save(os.path.basename(sample_audio_path), File(f))
            version.save()
            profile.audio = version.file
            profile.audio_uploaded_at = version.uploaded_at
            profile.save()
"@
    Write-Host "Created user: $($u.username) / $($u.password)"
}


# 8. Run server and open browser
Write-Host "Launching Django server..."
Start-Process "$python" -ArgumentList "manage.py runserver"
Start-Sleep -Seconds 3
Write-Host "Opening browser to http://127.0.0.1:8000"
Start-Process "http://127.0.0.1:8000/"

Write-Host "Setup complete! Visit the dashboard above to test users and audio."
