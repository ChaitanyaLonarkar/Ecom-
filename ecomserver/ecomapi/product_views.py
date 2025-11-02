from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .permisions import IsAdminUser, IsSuperAdminUser, IsAdminOrSuperAdminUser
from .models import Product, UserProfile

from .models import Category, Brand
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer


class ProductListView(APIView):
    """View to list all products."""

    def get_permissions(self):
        if self.request.method == 'POST':
           return [IsAuthenticated() , IsAdminOrSuperAdminUser()]
        elif self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()
    

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
  "id": serializer.data.get("id"),
  "name": serializer.data.get("name"),
  "slug": serializer.data.get("slug"),
  "price":  serializer.data.get("price"),
  "stock": serializer.data.get("stock"),
  "is_active": serializer.data.get("is_active"),
}
, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
class ProductGetUpdateDeleteView(APIView):
    """View to retrieve and update a product by ID."""
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
           return [IsAuthenticated() , IsAdminOrSuperAdminUser()]
        elif self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()


    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        if product is None:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        if product is None:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)