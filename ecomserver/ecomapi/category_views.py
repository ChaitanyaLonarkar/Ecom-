from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .permisions import IsAdminUser, IsSuperAdminUser, IsAdminOrSuperAdminUser
from .models import UserProfile

from .models import Category, Brand
from .serializers import CategorySerializer, BrandSerializer

class CategoryListView(APIView):
    """View to list all categories."""

    def get_permissions(self):
        if self.request.method == 'POST':
           return [IsAuthenticated() , IsAdminOrSuperAdminUser()]
        elif self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()
    

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CategoryUpdateDeleteView(APIView):

    """View to retrieve and update a category by ID."""
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdminUser]

    # def get_object(self, pk):
    #     try:
    #         return Category.objects.get(pk=pk)
    #     except Category.DoesNotExist:
    #         return None

    def put(self, request, pk):
        category = Category.objects.get(pk=pk)
        if category is None:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        category = Category.objects.get(pk=pk)
        if category is None:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class BrandListView(APIView):
    """View to list all brands."""

    def get_permissions(self):
        if self.request.method == 'POST':
           return [IsAuthenticated() , IsAdminOrSuperAdminUser()]
        elif self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')
        logo = request.FILES.get('logo')
        brand = Brand(name=name, description=description, logo=logo)
        brand.save()
        serializer = BrandSerializer(brand)
        return Response(serializer.data, status=status.HTTP_201_CREATED)