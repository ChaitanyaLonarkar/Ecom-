from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .permisions import IsAdminUser, IsSuperAdminUser
from .models import UserProfile

from .models import Category
from .serializers import CategorySerializer

class CategoryListView(APIView):
    """View to list all categories."""
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method == 'POST':
           return [IsAuthenticated() , IsAdminUser(), IsSuperAdminUser()]
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
    

class CategoryDetailUpdateView(APIView):

    """View to retrieve and update a category by ID."""
    permission_classes = [AllowAny]

    # def get_object(self, pk):
    #     try:
    #         return Category.objects.get(pk=pk)
    #     except Category.DoesNotExist:
    #         return None

    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        if category is None:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        category = Category.objects.get(pk=pk)
        if category is None:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)