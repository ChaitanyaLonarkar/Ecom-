
from .models import Product, UserProfile, User
from rest_framework import serializers
from .models import Category, Brand



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