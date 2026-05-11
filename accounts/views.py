from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from participants.models import Participant
from products.models import Product
from registrations.models import ProductRegistration
from payments.models import RegistrationPayment


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Usuario o contraseña inválidos')
        else:
            messages.error(request, 'Usuario o contraseña inválidos')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente')
    return redirect('login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido al sistema')
            return redirect('dashboard')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard_view(request):    
    context = {
        'total_participants': Participant.objects.count(),
        'total_products': Product.objects.count(),
        'total_registrations': ProductRegistration.objects.count(),
        'total_payments': RegistrationPayment.objects.filter(status='PAID').count(),
        'recent_participants': Participant.objects.order_by('-registration_date')[:5],
        'recent_products': Product.objects.order_by('-created_date')[:5],
        'recent_registrations': ProductRegistration.objects.order_by('-registration_date')[:5],
    }
    return render(request, 'accounts/dashboard.html', context)