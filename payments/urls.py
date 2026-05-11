from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('plans/', views.PaymentPlanListView.as_view(), name='plan_list'),
    path('plans/create/', views.PaymentPlanCreateView.as_view(), name='plan_create'),
    path('plans/<int:pk>/update/', views.PaymentPlanUpdateView.as_view(), name='plan_update'),
    path('plans/<int:pk>/delete/', views.PaymentPlanDeleteView.as_view(), name='plan_delete'),
    path('<int:pk>/', views.PaymentDetailView.as_view(), name='detail'),
    path('installment/<int:pk>/pay/', views.PaymentInstallmentUpdateView.as_view(), name='pay_installment'),
    path('history/', views.PaymentHistoryView.as_view(), name='history'),
]