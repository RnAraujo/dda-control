from django.urls import path
from . import views

app_name = 'public_views'

urlpatterns = [
    path('products/', views.PublicProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.PublicProductDetailView.as_view(), name='product_detail'),
    path('verify-access/', views.VerifyAccessView.as_view(), name='verify_access'),
    path('participant-portal/<int:participant_id>/', views.ParticipantPortalView.as_view(), name='participant_portal'),
]