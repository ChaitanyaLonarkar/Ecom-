from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import RegisterUserSerializer, UserProfileSerializer


class RegisterUserView(APIView):
    """Register a new user with role"""
    permission_classes = [AllowAny]

    # def post(self, request):

    #     # serialize and validate the incoming data here
    #     serializer= RegisterUserSerializer(data=request.data)
    #     if serializer.is_valid():
    #        serializer.save()
    #        return Response(serializer.data,status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        phone_number = request.data.get('phone_number', '')
        role = request.data.get('role', 'user')  # Default role is student
        
        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
        # ADMIN = "ADMIN", "Admin"
        # USER = "USER", "User"
        # Validate role
        valid_roles = ['SUPER_ADMIN', 'ADMIN', 'USER', 'user', 'admin', 'super_admin']

        if role not in valid_roles:
            return Response(
                {'error': f'Invalid role. Must be one of: {valid_roles}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create user profile with role
        UserProfile.objects.create(user=user, role=role)
        
        # refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': role
            },
            # 'tokens': {'refresh': str(refresh), 'access': str(refresh.access_token)}
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Login user and return access and refresh tokens"""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        userprofile = UserProfile.objects.get(user=user)

        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': userprofile.role
            },
            'tokens': {'refresh': str(refresh), 'access': str(refresh.access_token)}
        }, status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    """Logout user by blacklisting their refresh token"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
