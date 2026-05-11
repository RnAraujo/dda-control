from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Product, ProductCategory, ProductHistory
from participants.models import Participant
from .forms import ProductForm, ProductCategoryForm, ProductHistoryForm

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.GET.get('status')
        category_filter = self.request.GET.get('category')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if category_filter:
            queryset = queryset.filter(category__id=category_filter)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        context['status_choices'] = Product.STATUS_CHOICES
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['history'] = self.object.history.all().order_by('-change_date')
        context['registrations'] = self.object.productregistration_set.all()
        return context

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/form.html'
    
    def form_valid(self, form):
        form.instance.created_by = Participant.objects.first()  # You should get from session
        messages.success(self.request, 'Producto registrado exitosamente')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('products:detail', kwargs={'pk': self.object.pk})

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/form.html'
    
    def form_valid(self, form):
        old_status = self.get_object().status
        new_status = form.cleaned_data.get('status')
        
        response = super().form_valid(form)
        
        if old_status != new_status:
            ProductHistory.objects.create(
                product=self.object,
                previous_status=old_status,
                new_status=new_status,
                performed_by=form.instance.created_by
            )
            messages.success(self.request, f'Estado actualizado de {old_status} a {new_status}')
        
        messages.success(self.request, 'Producto actualizado exitosamente')
        return response
    
    def get_success_url(self):
        return reverse_lazy('products:detail', kwargs={'pk': self.object.pk})

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/confirm_delete.html'
    success_url = reverse_lazy('products:list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Producto eliminado exitosamente')
        return super().delete(request, *args, **kwargs)

class ProductHistoryCreateView(CreateView):
    model = ProductHistory
    form_class = ProductHistoryForm
    template_name = 'products/history_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=kwargs['product_pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.product = self.product
        form.instance.previous_status = self.product.status
        form.instance.new_status = self.product.status
        form.instance.performed_by = Participant.objects.first()  # You should get from session
        messages.success(self.request, 'Historial registrado exitosamente')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('products:detail', kwargs={'pk': self.product.pk})

class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'products/category_list.html'
    context_object_name = 'categories'

class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    form_class = ProductCategoryForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('products:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoría creada exitosamente')
        return super().form_valid(form)

class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'products/category_list.html'
    context_object_name = 'categories'
    ordering = ['name']

class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    form_class = ProductCategoryForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('products:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoría creada exitosamente')
        return super().form_valid(form)

class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    form_class = ProductCategoryForm
    template_name = 'products/category_form.html'
    success_url = reverse_lazy('products:category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoría actualizada exitosamente')
        return super().form_valid(form)

class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'products/category_confirm_delete.html'
    success_url = reverse_lazy('products:category_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Categoría eliminada exitosamente')
        return super().delete(request, *args, **kwargs)