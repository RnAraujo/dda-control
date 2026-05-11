from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
import os

def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Solo se permiten archivos PDF')

class Participant(models.Model):
    father_lastname = models.CharField(max_length=100)
    mother_lastname = models.CharField(max_length=100)
    names = models.CharField(max_length=200)
    
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')]
    )
    email = models.EmailField(unique=True)
    dni_number = models.CharField(max_length=8, unique=True)
    orcid_number = models.CharField(max_length=19, blank=True, null=True)
    birth_date = models.DateField()
    
    address = models.TextField()
    district = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    dni_document = models.FileField(
        upload_to='documents/dni/',
        validators=[validate_pdf],
        help_text='Adjuntar PDF del DNI'
    )
    
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.father_lastname} {self.mother_lastname}, {self.names}"
    
    @property
    def full_name(self):
        return f"{self.father_lastname} {self.mother_lastname} {self.names}"
    
    class Meta:
        ordering = ['father_lastname', 'mother_lastname']