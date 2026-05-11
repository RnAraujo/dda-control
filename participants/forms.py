from django import forms
from .models import Participant

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = [
            'father_lastname', 'mother_lastname', 'names', 'phone', 'email',
            'dni_number', 'orcid_number', 'birth_date', 'address',
            'district', 'province', 'department', 'country', 'dni_document'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'father_lastname': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'mother_lastname': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'names': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'phone': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'email': forms.EmailInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'dni_number': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'orcid_number': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'district': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'province': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'department': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'country': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'dni_document': forms.FileInput(attrs={'class': 'mt-1 block w-full'})
        }
        labels = {
            'father_lastname': 'Apellido Paterno',
            'mother_lastname': 'Apellido Materno',
            'names': 'Nombres',
            'phone': 'Celular',
            'email': 'Correo Electrónico',
            'dni_number': 'Número DNI',
            'orcid_number': 'Número ORCID',
            'birth_date': 'Fecha de Nacimiento',
            'address': 'Dirección',
            'district': 'Distrito',
            'province': 'Provincia',
            'department': 'Departamento',
            'country': 'País',
            'dni_document': 'Adjuntar PDF de DNI'
        }

class ParticipantSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Buscar por DNI, nombre o email',
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'
    }))