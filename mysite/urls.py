from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

# Custom login view import (if you have custom login)
from accounts.views import login_view, logout_view, register_view, dashboard_view

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # Root URL - redirect to dashboard or login
    path('', lambda request: redirect('dashboard' if request.user.is_authenticated else 'accounts:login')),
    
    # Accounts / Authentication URLs
    path('accounts/', include('apps.accounts.urls')),
    # Alternative direct URLs for accounts
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # App URLs
    path('participants/', include('apps.participants.urls')),
    path('products/', include('apps.products.urls')),
    path('registrations/', include('apps.registrations.urls')),
    path('payments/', include('apps.payments.urls')),
    path('public/', include('apps.public_views.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Optional: Add Django debug toolbar if installed
    # if 'debug_toolbar' in settings.INSTALLED_APPS:
    #     import debug_toolbar
    #     urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns

# Custom error handlers (optional)
handler404 = 'apps.core.views.handler404'
handler500 = 'apps.core.views.handler500'