

from django.urls import path

from .auth_views import *
from .category_views import *
from .product_views import *


urlpatterns = [
    path('auth/register', RegisterUserView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('auth/profile', UserProfileView.as_view(), name='profile'),
    path('auth/create-admin', CreateAdminView.as_view(), name='create-admin'),

     # category urls
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryUpdateDeleteView.as_view(), name='category-detail-update'),
    # path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    # path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    # path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    #Brand urls
    path('brands/', BrandListView.as_view(), name='brand-list'),

    #product urls
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductGetUpdateDeleteView.as_view(), name='product-detail-update'),
    # path('products/create/', ProductCreateView.as_view(), name='product-create'),
    # path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    # path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),

   
]
