from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import urls as users_urls
from users.views import landing_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include((users_urls))),
    path('', landing_page, name='landing'),  


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
