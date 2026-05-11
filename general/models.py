from django.db import models
from products.models import Product

class PublicViewConfig(models.Model):
    VISIBILITY_CHOICES = [
        ('PUBLIC', 'Público - Cualquier persona puede ver'),
        ('PRIVATE', 'Privado - Solo participantes registrados'),
        ('PROTECTED', 'Protegido - Requiere código de acceso'),
    ]
    
    is_public_enabled = models.BooleanField(default=True)
    visibility_mode = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='PUBLIC')
    access_code = models.CharField(max_length=20, blank=True, null=True)
    show_participant_info = models.BooleanField(default=True)
    show_payment_info = models.BooleanField(default=False)
    allow_product_search = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Public View Config - {self.visibility_mode}"
    
    class Meta:
        verbose_name = "Configuración de Vista Pública"
        verbose_name_plural = "Configuraciones de Vista Pública"