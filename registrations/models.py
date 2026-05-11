from django.db import models
from products.models import Product
from participants.models import Participant

class ProductRegistration(models.Model):
    REGISTRATION_STATUS = [
        ('PENDING', 'Pendiente'),
        ('REGISTERED', 'Registrado'),
        ('OBSERVED', 'Observado'),
        ('IN_PROCESS', 'En Proceso'),
        ('COMPLETED', 'Finalizado'),
        ('REJECTED', 'Rechazado'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=REGISTRATION_STATUS, default='PENDING')
    observations = models.TextField(blank=True, null=True)
    
    # For exempt participants
    is_payment_exempt = models.BooleanField(default=False)
    exemption_reason = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.participant.full_name}"
    
    class Meta:
        unique_together = ['product', 'participant']