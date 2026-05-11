from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('participants:list')),
    path('participants/', include('participants.urls')),
    path('products/', include('products.urls')),
    path('registrations/', include('registrations.urls')),
    path('payments/', include('payments.urls')),
    path('public/', include('public_views.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
