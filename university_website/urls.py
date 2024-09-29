from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from student import views
from university_website import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/', include('student.urls')),
    path('', include('static_webpages.urls')),
    path('structure/', include('programs.urls')),
    path('api/', include('programs.api.urls', namespace='api-programs')),
    path('reset_password/', views.MyPasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', views.MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
