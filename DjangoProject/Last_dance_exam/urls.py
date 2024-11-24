from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import (PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)


urlpatterns = [
path('password-reset/', PasswordResetView.as_view(template_name='app_users/password-reset.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='app_users/password-reset-done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='app_users/password-reset-confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='app_users/password-reset-complete.html'), name='password_reset_complete'),

    path('social-auth/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    path('user/', include('app_users.urls')),
    path('', include('app_main.urls')),

]


if settings.DEBUG:
    urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)
