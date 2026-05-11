from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from products.models import Product
from registrations.models import ProductRegistration
from participants.models import Participant
from payments.models import RegistrationPayment, PaymentInstallment
from .models import PublicViewConfig

class PublicProductListView(ListView):
    model = Product
    template_name = 'public_views/product_list.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def dispatch(self, request, *args, **kwargs):
        self.config = PublicViewConfig.objects.first()
        if not self.config or not self.config.is_public_enabled:
            messages.warning(request, 'La vista pública no está habilitada actualmente')
            return redirect('home')
        
        # Check privacy mode
        if self.config.visibility_mode == 'PRIVATE':
            if not request.session.get('has_access'):
                return redirect('public_views:verify_access')
        elif self.config.visibility_mode == 'PROTECTED':
            if not request.session.get('has_access'):
                return redirect('public_views:verify_access')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = Product.objects.filter(status__in=['APPROVED', 'REGISTERED'])
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query and self.config.allow_product_search:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(version__icontains=search_query)
            )
        
        # Filter by category
        category = self.request.GET.get('category', '')
        if category:
            queryset = queryset.filter(category__name=category)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['config'] = self.config
        
        # Get participant info if provided
        participant_id = self.request.GET.get('participant_id')
        if participant_id and self.config.show_participant_info:
            try:
                participant = Participant.objects.get(id=participant_id)
                context['participant'] = participant
                context['participant_products'] = ProductRegistration.objects.filter(
                    participant=participant
                ).select_related('product')
            except Participant.DoesNotExist:
                pass
                
        return context

class PublicProductDetailView(DetailView):
    model = Product
    template_name = 'public_views/product_detail.html'
    context_object_name = 'product'
    
    def dispatch(self, request, *args, **kwargs):
        self.config = PublicViewConfig.objects.first()
        if not self.config or not self.config.is_public_enabled:
            messages.warning(request, 'La vista pública no está habilitada actualmente')
            return redirect('home')
        
        # Check privacy mode
        if self.config.visibility_mode == 'PRIVATE':
            if not request.session.get('has_access'):
                return redirect('public_views:verify_access')
        elif self.config.visibility_mode == 'PROTECTED':
            if not request.session.get('has_access'):
                return redirect('public_views:verify_access')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['config'] = self.config
        
        # Get registrations for this product
        registrations = ProductRegistration.objects.filter(
            product=self.object
        ).select_related('participant')
        
        if self.config.show_participant_info:
            context['registrations'] = registrations
            
            # Get payment info if enabled
            if self.config.show_payment_info:
                payments_info = []
                for reg in registrations:
                    payment = RegistrationPayment.objects.filter(registration=reg).first()
                    if payment:
                        payments_info.append({
                            'participant': reg.participant,
                            'payment': payment,
                            'installments': PaymentInstallment.objects.filter(payment=payment)
                        })
                context['payments_info'] = payments_info
        
        return context

class VerifyAccessView(View):
    template_name = 'public_views/verify_access.html'
    
    def get(self, request):
        config = PublicViewConfig.objects.first()
        context = {'config': config}
        return render(request, self.template_name, context)
    
    def post(self, request):
        config = PublicViewConfig.objects.first()
        
        if config.visibility_mode == 'PROTECTED':
            access_code = request.POST.get('access_code')
            if access_code == config.access_code:
                request.session['has_access'] = True
                messages.success(request, 'Acceso concedido correctamente')
                
                # Redirect to original page
                next_page = request.GET.get('next', 'public_views:product_list')
                return redirect(next_page)
            else:
                messages.error(request, 'Código de acceso incorrecto')
                return render(request, self.template_name, {'config': config})
        
        # For PRIVATE mode, just grant access
        request.session['has_access'] = True
        messages.success(request, 'Acceso concedido')
        return redirect('public_views:product_list')

class ParticipantPortalView(ListView):
    model = ProductRegistration
    template_name = 'public_views/participant_portal.html'
    context_object_name = 'registrations'
    
    def dispatch(self, request, *args, **kwargs):
        participant_id = self.kwargs.get('participant_id')
        try:
            self.participant = Participant.objects.get(id=participant_id)
        except Participant.DoesNotExist:
            messages.error(request, 'Participante no encontrado')
            return redirect('public_views:product_list')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return ProductRegistration.objects.filter(
            participant=self.participant
        ).select_related('product')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['participant'] = self.participant
        
        # Get payment information for each registration
        payments_data = []
        for registration in context['registrations']:
            payment = RegistrationPayment.objects.filter(registration=registration).first()
            if payment:
                installments = PaymentInstallment.objects.filter(payment=payment)
                payments_data.append({
                    'registration': registration,
                    'payment': payment,
                    'installments': installments,
                    'total_paid': sum(i.installment_amount for i in installments if i.is_paid)
                })
            else:
                payments_data.append({
                    'registration': registration,
                    'payment': None,
                    'installments': []
                })
        context['payments_data'] = payments_data
        
        return context