from django import forms
from .models import Product, ProductCategory, ProductHistory


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            })
        }
        labels = {
            'name': 'Nombre de la Categoría',
            'description': 'Descripción'
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'version', 'category', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'version': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'category': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'status': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'})
        }
        labels = {
            'name': 'Nombre del Producto',
            'description': 'Descripción',
            'version': 'Versión',
            'category': 'Categoría',
            'status': 'Estado'
        }

class ProductHistoryForm(forms.ModelForm):
    class Meta:
        model = ProductHistory
        fields = ['observations', 'resolution', 'final_document']
        widgets = {
            'observations': forms.Textarea(attrs={'rows': 4, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}),
            'resolution': forms.FileInput(attrs={'class': 'mt-1 block w-full'}),
            'final_document': forms.FileInput(attrs={'class': 'mt-1 block w-full'})
        }
        labels = {
            'observations': 'Observaciones',
            'resolution': 'Resolución',
            'final_document': 'Documento Final'
        }