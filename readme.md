# Django Audio Dashboard

## Overview
This is a full-stack Django application for managing user profiles and audio uploads. Users can upload audio files, view current and previous versions, restore older versions, and visualize audio waveforms. The app features a modern, neon-themed, light/dark toggling UI.

## Features
- REST API for user profiles.
- Audio file upload, playback, and version history.
- Waveform visualization using Wavesurfer.js.
- Light/Dark mode toggle.
- Drag-and-drop audio upload.
- Fully responsive and interactive frontend.

## Future Enhancements
- AI/ML-based audio analysis (speech-to-text, emotion detection, audio quality analysis).
- Auto-recommendations for audio editing.
- User analytics dashboard.
- Voice-based commands to control the app.
- Advanced audio filters and processing.

## Project Structure
```
project_root/
│   manage.py
│   requirements.txt
│   .gitignore
│   setup.ps1
│
├── audioapp/     # Django project settings
├── users/                # Django app for user profiles and audio
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── templates/users/user_dashboard.html
└── static/audio/         # Sample audio files for testing
```

## Setup Instructions (Manual Steps)

### 1. Clone Repository
```bash
git clone <repository-url>
cd project_root
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
- **Windows:** `.env\Scripts\Activate.ps1`
- **Linux/macOS:** `source venv/bin/activate`

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Apply Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (optional)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```
Access the app at `http://127.0.0.1:8000/`.

## Automated Test Setup (Windows)

To make testing easy for recruiters, a **PowerShell automation script** is provided: `setup.ps1`. It performs the following tasks:

1. Creates and activates a virtual environment.
2. Installs required packages from `requirements.txt`.
3. Runs Django migrations.
4. Creates a superuser (`admin/Admin123`).
5. Creates 3 test users with usernames `testuser1`, `testuser2`, `testuser3`.
6. Uploads sample audio files from `static/audio/` for each test user.

### Running the Automation Script
1. Open PowerShell in the project root.
2. Execute:
```powershell
.\setup.ps1
```
3. After completion, the server can be run with:
```powershell
python manage.py runserver
```
4. Access dashboards:
   - `http://127.0.0.1:8000/users/1/dashboard/`
   - `http://127.0.0.1:8000/users/2/dashboard/`
   - `http://127.0.0.1:8000/users/3/dashboard/`

## Testing the App
- Upload audio by drag-and-drop or file selector.
- Observe waveform visualization.
- Test restoring previous audio versions.
- Toggle between Light/Dark mode.
- Ensure everything works without backend errors.

## Requirements
- Python 3.11+
- Django 5.0+
- Django REST Framework
- Wavesurfer.js (frontend included via CDN)
- Mutagen (for audio validation)

## .gitignore
```
# Python
__pycache__/
*.pyc
*.pyo
*.pyd

# Virtual Environment
venv/

# Django
*.sqlite3
/static/audio/*
/media/

# IDEs
.vscode/
.idea/
```

## requirements.txt
```
django>=5.0.0
djangorestframework
mutagen
```

---

This README provides **all steps** for setup, testing, and running the project. Recruiters can run the automation script to quickly have a ready-to-test environment.