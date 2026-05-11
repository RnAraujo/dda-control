from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import RegistrationPayment, PaymentPlan, PaymentInstallment
from registrations.models import ProductRegistration
from .forms import PaymentPlanForm, InstallmentPaymentForm

class PaymentPlanListView(ListView):
    model = PaymentPlan
    template_name = 'payments/plan_list.html'
    context_object_name = 'plans'

class PaymentPlanCreateView(CreateView):
    model = PaymentPlan
    form_class = PaymentPlanForm
    template_name = 'payments/plan_form.html'
    success_url = reverse_lazy('payments:plan_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Plan de pago creado exitosamente')
        return super().form_valid(form)

class PaymentPlanUpdateView(UpdateView):
    model = PaymentPlan
    form_class = PaymentPlanForm
    template_name = 'payments/plan_form.html'
    success_url = reverse_lazy('payments:plan_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Plan de pago actualizado exitosamente')
        return super().form_valid(form)

class PaymentPlanDeleteView(DeleteView):
    model = PaymentPlan
    template_name = 'payments/plan_confirm_delete.html'
    success_url = reverse_lazy('payments:plan_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Plan de pago eliminado exitosamente')
        return super().delete(request, *args, **kwargs)

class PaymentDetailView(DetailView):
    model = RegistrationPayment
    template_name = 'payments/detail.html'
    context_object_name = 'payment'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['installments'] = self.object.installments.all().order_by('installment_number')
        context['total_paid'] = sum(i.installment_amount for i in context['installments'] if i.is_paid)
        return context

class PaymentInstallmentUpdateView(UpdateView):
    model = PaymentInstallment
    form_class = InstallmentPaymentForm
    template_name = 'payments/installment_form.html'
    
    def form_valid(self, form):
        installment = form.save()
        
        # Update payment totals
        payment = installment.payment
        paid_installments = payment.installments.filter(is_paid=True)
        total_paid = sum(i.installment_amount for i in paid_installments)
        
        payment.paid_amount = total_paid
        payment.pending_balance = payment.total_amount - total_paid
        
        if total_paid >= payment.total_amount:
            payment.status = 'PAID'
        else:
            payment.status = 'PENDING'
        
        payment.save()
        
        messages.success(self.request, 'Pago registrado exitosamente')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('payments:detail', kwargs={'pk': self.object.payment.pk})

class PaymentHistoryView(ListView):
    model = RegistrationPayment
    template_name = 'payments/history.html'
    context_object_name = 'payments'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        participant_id = self.request.GET.get('participant')
        
        if participant_id:
            queryset = queryset.filter(registration__participant__id=participant_id)
            
        return queryset.order_by('-registration__registration_date')