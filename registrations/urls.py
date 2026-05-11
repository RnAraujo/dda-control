from django.urls import path
from . import views

app_name = 'registrations'

urlpatterns = [
    path('', views.ProductRegistrationListView.as_view(), name='list'),
    path('<int:pk>/', views.ProductRegistrationDetailView.as_view(), name='detail'),
    path('create/', views.ProductRegistrationCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.ProductRegistrationUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ProductRegistrationDeleteView.as_view(), name='delete'),
    path('<int:pk>/update-status/', views.UpdateRegistrationStatusView.as_view(), name='update_status'),
]