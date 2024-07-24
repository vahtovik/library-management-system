from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from library_manager import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls', namespace='library')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])