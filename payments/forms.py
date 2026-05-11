from django import forms
from .models import RegistrationPayment, PaymentPlan, PaymentInstallment

class PaymentPlanForm(forms.ModelForm):
    class Meta:
        model = PaymentPlan
        fields = ['name', 'installments_number', 'interest_rate', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'installments_number': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm', 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'})
        }
        labels = {
            'name': 'Nombre del Plan',
            'installments_number': 'Número de Cuotas',
            'interest_rate': 'Tasa de Interés (%)',
            'is_active': 'Activo'
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = RegistrationPayment
        fields = ['payment_plan']
        widgets = {
            'payment_plan': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'})
        }
        labels = {
            'payment_plan': 'Plan de Pago'
        }

class InstallmentPaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentInstallment
        fields = ['payment_date', 'receipt', 'is_paid']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'receipt': forms.FileInput(attrs={'class': 'mt-1 block w-full'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'})
        }
        labels = {
            'payment_date': 'Fecha de Pago',
            'receipt': 'Comprobante',
            'is_paid': 'Pagado'
        }