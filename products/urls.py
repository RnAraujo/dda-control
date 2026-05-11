from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Product URLs
    path('', views.ProductListView.as_view(), name='list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
    path('create/', views.ProductCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.ProductUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete'),
    path('<int:product_pk>/history/create/', views.ProductHistoryCreateView.as_view(), name='create_history'),
    
    # Category URLs
    path('categories/', views.ProductCategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.ProductCategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', views.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.ProductCategoryDeleteView.as_view(), name='category_delete'),
]