

from django.urls import path

from ecomapi.send_email_views import PasswordResetConfirmView, PasswordResetRequestView

from .stripe_views import PaymentAPI, StripeWebhookAPIView

from .auth_views import *
from .category_views import *
from .product_views import *
from .cart_views import *



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
    path('products/<int:pk>/variants/', ProductVarientCreateView.as_view(), name='product-create-varient'),
    # path('product/<id:pk>/images/', ProductImageCreateView.as_view(), name='product-image-create'),
   

   # cart apis
    path('cart/add/', CartAddItemView.as_view(), name='cart-add-item'),
    path('cart/', CartView.as_view(), name='cart-view'),
  
    path('cart/<int:pk>/update/', CartUpdateDeleteView.as_view(), name='cart-update'),
    path('cart/<int:pk>/delete/', CartUpdateDeleteView.as_view(), name='cart-delete'),

    

    path('make_payment/', PaymentAPI.as_view(), name='make_payment'),
    # path('suce')
    path('webhook/' , StripeWebhookAPIView.as_view(), name='stripe-webhook'),


    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

   
]
