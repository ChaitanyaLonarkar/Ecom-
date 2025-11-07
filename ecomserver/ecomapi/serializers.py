
from .models import Cart, CartItem, Product, ProductVariant, UserProfile, User
from rest_framework import serializers
from .models import Category, Brand,ProductImage



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

        # read_only_fields = ['id', 'user']
        # depth = 1
class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    # profile = UserProfileSerializer(read_only=True)
    # class Meta:
    #     model = User
    #     fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'profile']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'profile']

# category serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductVarientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'sku', 'name', 'price', 'stock']

class ProductImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        field=['id', 'image_url']

class CartAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [ 'cart', 'product_variant', 'quantity','subtotal']

class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = "__all__"

class CartSerializer(serializers.ModelSerializer):
    cartitem=CartItemSerializer(read_only=True,many=True)
    
    class Meta:
        model = Cart
        fields = [ 'id', 'user', 'cartitem',  'created_at']



class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True)