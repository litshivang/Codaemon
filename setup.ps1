# 1. Set variables
$venvDir = "venv"
$python = "python"  # Use full path if multiple Python versions
$sampleAudioDir = ".\static\audio"
$users = @(
    @{username="testuser1"; email="user1@example.com"; password="Password123"},
    @{username="testuser2"; email="user2@example.com"; password="Password123"},
    @{username="testuser3"; email="user3@example.com"; password="Password123"}
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
    & $python manage.py shell -c "
from django.contrib.auth import get_user_model
from users.models import UserProfile, AudioVersion
from django.core.files import File
import os

User = get_user_model()

user, created = User.objects.get_or_create(username='$($u.username)', defaults={'email':'$($u.email)'})
if created:
    user.set_password('$($u.password)')
    user.save()

profile, _ = UserProfile.objects.get_or_create(user=user)

sample_audio_path = os.path.join('$sampleAudioDir', '$($u.username).mp3')
if os.path.exists(sample_audio_path):
    with open(sample_audio_path, 'rb') as f:
        version = AudioVersion(profile=profile, original_name=os.path.basename(sample_audio_path))
        version.file.save(os.path.basename(sample_audio_path), File(f))
        version.save()
        profile.audio = version.file
        profile.audio_uploaded_at = version.uploaded_at
        profile.save()
"
    Write-Host "Created user: $($u.username) / $($u.password)"
}

Write-Host "Setup complete! You can now run the project with:"
Write-Host "`tpython manage.py runserver"
