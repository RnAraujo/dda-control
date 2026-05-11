from django.db import models
from django.contrib.auth.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Borrador'),
        ('REGISTERED', 'Registrado'),
        ('UNDER_REVIEW', 'En Revisión'),
        ('OBSERVED', 'Observado'),
        ('APPROVED', 'Aprobado'),
        ('REJECTED', 'Rechazado'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    version = models.CharField(max_length=20)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
    created_by = models.ForeignKey('participants.Participant', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} v{self.version}"

class ProductHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='history')
    previous_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    observations = models.TextField()
    resolution = models.FileField(upload_to='documents/resolutions/', blank=True, null=True)
    final_document = models.FileField(upload_to='documents/final/', blank=True, null=True)
    change_date = models.DateTimeField(auto_now_add=True)
    performed_by = models.ForeignKey('participants.Participant', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.change_date}"