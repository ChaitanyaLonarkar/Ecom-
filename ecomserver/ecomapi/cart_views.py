from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .permisions import IsAdminUser, IsSuperAdminUser, IsAdminOrSuperAdminUser
from .models import Cart, CartItem, Product, UserProfile
from .serializers import CartAddSerializer, CartItemSerializer, CartSerializer


class CartAddItemView(APIView):

    permission_classes=[IsAuthenticated,IsSuperAdminUser]

  
    def post(self,request):
        cart = request.user.cart
        print (cart,"dfasdf")
        # serializer=CartAddSerializer(cart, data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data,status=status.HTTP_201_CREATED)
        product_variant=request.data.get('product_variant')
        quantity=request.data.get('quantity')

        serializer=CartAddSerializer(data={'cart':cart.id,'product_variant':product_variant,'quantity':quantity})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CartView(APIView):
    permission_classes=[IsAuthenticated,IsSuperAdminUser]
    def get(self,request):
        user= request.user
        carts= Cart.objects.get(user=user)

        # print(user,"dfasdf")
        # print("cartid", carts.id)
        cart = CartItem.objects.all().filter(cart=carts.id)
        
        serializer=CartSerializer(carts)

        print(serializer.data,"dfasdf")

        total=0
        for item in cart:
            total += item.subtotal
        # print("total", total)
        return Response({
                "user": request.user.username,
                # "items":[{
                # # "id": cart.id,
                # # "product_variant": cart.product_variant,
                # # "quantity": cart.quantity,
                # }],
                # "total":cart.subtotal
                "items":cart.values(),
                # "cart":serializer.data,
                "total":total

            },status=status.HTTP_200_OK)
        # return Response(serializer.data,status=status.HTTP_200_OK)
        # except :
        #     return Response({"error":"Cart not found"},status=status.HTTP_404_NOT_FOUND)