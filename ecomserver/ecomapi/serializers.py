
from .models import CartItem, Product, ProductVariant, UserProfile, User
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
        fields = ['product_variant', 'quantity']