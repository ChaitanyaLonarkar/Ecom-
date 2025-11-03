from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .permisions import IsAdminUser, IsSuperAdminUser, IsAdminOrSuperAdminUser
from .models import Product, UserProfile
from .serializers import CartAddSerializer


class CartAddItemView(APIView):

    permission_classes=[IsAuthenticated,IsSuperAdminUser]

    def post(self,request):
        serializer=CartAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
