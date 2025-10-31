from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .permisions import IsAdminUser, IsSuperAdminUser
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
        
class UserProfileView(APIView):
    """Get user profile information"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        userprofile = UserProfile.objects.get(user=user)

        serialzer=UserProfileSerializer(userprofile)

        return Response(serialzer.data,status=status.HTTP_200_OK)

        # return Response({
        #     'user': {
        #         'id': user.id,
        #         'username': user.username,
        #         'email': user.email,
        #         'first_name': user.first_name,
        #         'last_name': user.last_name,
        #         'role': userprofile.role,
        #         'bio': userprofile.bio,
        #         'profile_picture': userprofile.profile_picture.url if userprofile.profile_picture else None
        #     }
        # }, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        userprofile = UserProfile.objects.get(user=user)

        # serializer = UserProfileSerializer(data=request.data, instance=userprofile, partial=True)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.email = request.data.get('email', user.email)
        userprofile.phone_number = request.data.get('phone_number', userprofile.phone_number)
        userprofile.date_of_birth = request.data.get('date_of_birth', userprofile.date_of_birth)
        userprofile.gender = request.data.get('gender', userprofile.gender)

        if 'profile_picture' in request.FILES:
            userprofile.profile_picture = request.FILES['profile_picture']

        user.save()
        userprofile.save()

        return Response({'message': 'Profile updated successfully', 'user': {'id': user.id, 'username': user.username, 'email': user.email}, 'profile': {'phone_number': userprofile.phone_number, 'gender': userprofile.gender, 'role': userprofile.role}}, status=status.HTTP_200_OK)
    

class CreateAdminView(APIView):
    permission_classes = [IsAuthenticated & IsSuperAdminUser]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        role = request.data.get('role', 'admin')  # Default role is admin

        if role != 'admin' and role != 'ADMIN':
            return Response(
                {'error': 'Only admin role can be created via this endpoint'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not username or not password or not email:
            return Response(
                {'error': 'Username and password and email are required'},
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
    
        
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create user profile with role
        userprofile = UserProfile.objects.create(user=user, role=role)
        
        # refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Admin created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': userprofile.role
            },
            # 'tokens': {'refresh': str(refresh), 'access': str(refresh.access_token)}
        }, status=status.HTTP_201_CREATED)