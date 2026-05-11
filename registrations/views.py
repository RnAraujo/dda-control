from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import ProductRegistration
from payments.models import RegistrationPayment, PaymentPlan, PaymentInstallment
from .forms import ProductRegistrationForm, RegistrationStatusForm
from datetime import datetime, timedelta

class ProductRegistrationListView(ListView):
    model = ProductRegistration
    template_name = 'registrations/list.html'
    context_object_name = 'registrations'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.GET.get('status')
        product_filter = self.request.GET.get('product')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if product_filter:
            queryset = queryset.filter(product__id=product_filter)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = ProductRegistration.REGISTRATION_STATUS
        context['products'] = Product.objects.all()
        return context

class ProductRegistrationDetailView(DetailView):
    model = ProductRegistration
    template_name = 'registrations/detail.html'
    context_object_name = 'registration'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = self.object.payments.all()
        context['status_form'] = RegistrationStatusForm(instance=self.object)
        return context

class ProductRegistrationCreateView(CreateView):
    model = ProductRegistration
    form_class = ProductRegistrationForm
    template_name = 'registrations/form.html'
    
    def form_valid(self, form):
        registration = form.save()
        
        # If not exempt, create payment
        if not registration.is_payment_exempt:
            total_amount = self.calculate_amount(registration.product)
            payment_plan = PaymentPlan.objects.filter(is_active=True).first()
            
            if payment_plan:
                payment = RegistrationPayment.objects.create(
                    registration=registration,
                    total_amount=total_amount,
                    paid_amount=0,
                    pending_balance=total_amount,
                    payment_plan=payment_plan,
                    due_date=datetime.now().date() + timedelta(days=30),
                    status='PENDING'
                )
                
                # Create installments
                installment_amount = total_amount / payment_plan.installments_number
                for i in range(payment_plan.installments_number):
                    PaymentInstallment.objects.create(
                        payment=payment,
                        installment_number=i+1,
                        installment_amount=installment_amount,
                        due_date=datetime.now().date() + timedelta(days=30*(i+1)),
                        is_paid=False
                    )
        
        messages.success(self.request, 'Registro creado exitosamente')
        return super().form_valid(form)
    
    def calculate_amount(self, product):
        base_amount = 500
        if product.category.name.lower() == 'software empresarial':
            return base_amount * 1.5
        return base_amount
    
    def get_success_url(self):
        return reverse_lazy('registrations:detail', kwargs={'pk': self.object.pk})

class ProductRegistrationUpdateView(UpdateView):
    model = ProductRegistration
    form_class = ProductRegistrationForm
    template_name = 'registrations/form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Registro actualizado exitosamente')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('registrations:detail', kwargs={'pk': self.object.pk})

class ProductRegistrationDeleteView(DeleteView):
    model = ProductRegistration
    template_name = 'registrations/confirm_delete.html'
    success_url = reverse_lazy('registrations:list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Registro eliminado exitosamente')
        return super().delete(request, *args, **kwargs)

class UpdateRegistrationStatusView(UpdateView):
    model = ProductRegistration
    form_class = RegistrationStatusForm
    template_name = 'registrations/update_status.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Estado actualizado exitosamente')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('registrations:detail', kwargs={'pk': self.object.pk})