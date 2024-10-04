from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from student import views
from university_website import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/', include('student.urls')),
    path('', include('static_webpages.urls')),
    path('structure/', include('programs.urls')),
    path('api/programs/', include('programs.api.urls', namespace='api-programs')),
    path('api/student/', include('student.api.urls', namespace='api-student')),

    path('reset_password/', views.MyPasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', views.MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

admin.site.site_header = "Blank University Administration"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls')), ]
