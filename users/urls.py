from django.urls import path, re_path
from .views import UserProfileViewSet, dashboard_view

urlpatterns = [
    path('<int:pk>/', UserProfileViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
    path('<int:pk>/audio/', UserProfileViewSet.as_view({'post': 'upload_audio', 'delete': 'delete_audio'}), name='user-audio'),
    re_path(r'^(?P<pk>\d+)/audio/restore/(?P<version_id>\d+)/$', 
            UserProfileViewSet.as_view({'post': 'restore_audio_version'}), 
            name='restore-audio'),
    path('<int:pk>/dashboard/', dashboard_view, name='user-dashboard'),
]
