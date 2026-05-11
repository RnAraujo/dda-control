from django.db import models
from registrations.models import ProductRegistration

class PaymentPlan(models.Model):
    name = models.CharField(max_length=100)
    installments_number = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.installments_number} cuotas"

class RegistrationPayment(models.Model):
    PAYMENT_STATUS = [
        ('PENDING', 'Pendiente'),
        ('PAID', 'Pagado'),
        ('EXPIRED', 'Vencido'),
        ('CANCELLED', 'Anulado'),
    ]
    
    registration = models.ForeignKey(ProductRegistration, on_delete=models.CASCADE, related_name='payments')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pending_balance = models.DecimalField(max_digits=10, decimal_places=2)
    payment_plan = models.ForeignKey(PaymentPlan, on_delete=models.SET_NULL, null=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    
    def save(self, *args, **kwargs):
        self.pending_balance = self.total_amount - self.paid_amount
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Payment {self.registration.id} - {self.status}"

class PaymentInstallment(models.Model):
    payment = models.ForeignKey(RegistrationPayment, on_delete=models.CASCADE, related_name='installments')
    installment_number = models.IntegerField()
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    receipt = models.FileField(upload_to='receipts/', blank=True, null=True)
    
    def __str__(self):
        return f"Installment {self.installment_number} - {self.payment.registration.product.name}"