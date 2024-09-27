
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from university_website import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/', include('student.urls')),
    path('', include('static_webpages.urls')),
    path('structure/', include('programs.urls')),
    path('api/', include('programs.api.urls', namespace = 'api-programs'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
