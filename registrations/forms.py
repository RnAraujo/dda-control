from django import forms
from .models import ProductRegistration
from products.models import Product
from participants.models import Participant

class ProductRegistrationForm(forms.ModelForm):
    class Meta:
        model = ProductRegistration
        fields = ['product', 'participant', 'status', 'is_payment_exempt', 'exemption_reason', 'observations']
        widgets = {
            'product': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'participant': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'status': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'is_payment_exempt': forms.CheckboxInput(attrs={'class': 'mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'}),
            'exemption_reason': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'observations': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'})
        }
        labels = {
            'product': 'Producto',
            'participant': 'Participante',
            'status': 'Estado',
            'is_payment_exempt': 'Exonerado de Pago',
            'exemption_reason': 'Motivo de Exoneración',
            'observations': 'Observaciones'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(status__in=['REGISTERED', 'APPROVED'])
        self.fields['participant'].queryset = Participant.objects.filter(is_active=True)

class RegistrationStatusForm(forms.ModelForm):
    class Meta:
        model = ProductRegistration
        fields = ['status', 'observations']
        widgets = {
            'status': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'observations': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'})
        }
        labels = {
            'status': 'Estado',
            'observations': 'Observaciones'
        }