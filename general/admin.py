from django.contrib import admin
from .models import PublicViewConfig

@admin.register(PublicViewConfig)
class PublicViewConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Configuración General', {
            'fields': ('is_public_enabled', 'visibility_mode')
        }),
        ('Acceso Protegido', {
            'fields': ('access_code',),
            'classes': ('collapse',),
            'description': 'Configuración solo para modo protegido'
        }),
        ('Visibilidad de Información', {
            'fields': ('show_participant_info', 'show_payment_info', 'allow_product_search')
        })
    )
    
    def has_add_permission(self, request):
        # Allow only one configuration instance
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)