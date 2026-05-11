from django.shortcuts import render
from django.shortcuts import redirect

def handler404(request, exception):
    """Custom 404 error handler"""
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    """Custom 500 error handler"""
    return render(request, 'errors/500.html', status=500)

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('accounts:login')