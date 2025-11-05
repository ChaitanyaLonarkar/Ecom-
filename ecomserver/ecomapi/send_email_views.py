from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from ecomapi.serializers import PasswordResetConfirmSerializer, PasswordResetEmailSerializer

User = get_user_model()

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # For security, avoid revealing if an email exists or not
            return Response({'detail': 'Password reset email sent if account exists.'}, status=status.HTTP_200_OK)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Construct the reset link (replace with your frontend URL)
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        # Render email content from a template
        email_html_message = render_to_string('password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })

        send_mail(
            'Password Reset Request',
            email_html_message,  # Use html_message for HTML content
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
            html_message=email_html_message,
        )

        return Response({'detail': 'Password reset email sent if account exists.'}, status=status.HTTP_200_OK)



class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            uid_decoded = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid_decoded)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Invalid or expired reset link.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password reset successfully.'}, status=status.HTTP_200_OK)








# from django.core.mail import send_mail
# from django.conf import settings
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth.models import User
# from rest_framework.permissions import AllowAny
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# class SendEmailView(APIView):
#     permission_classes = [AllowAny]  # Allow any user to access this view

#     def post(self, request):
#         try:
#             data = request.data
#             subject = data.get('subject')
#             to_email = data.get('to_email')
#             context = {
#                 'username': data.get('username'),
#                 'message': data.get('message'),
#             }

#             # Render HTML content
#             html_message = render_to_string('email_template.html', context)
#             plain_message = strip_tags(html_message)

#             send_mail(
#                 subject,
#                 plain_message,
#                 settings.EMAIL_HOST_USER,
#                 [to_email],
#                 html_message=html_message,
#             )
#             return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# class ForgotPasswordEmailView(APIView):
#     permission_classes = [AllowAny]  # Allow any user to access this view

#     def post(self, request):
#         try:
#             data = request.data
#             subject = "Password Reset Request"
#             to_email = data.get('to_email')
#             reset_link = data.get('reset_link')
#             context = {
#                 'reset_link': reset_link,
#             }

#             # Render HTML content
#             html_message = render_to_string('forgot_password_email.html', context)
#             plain_message = strip_tags(html_message)

#             send_mail(
#                 subject,
#                 plain_message,
#                 settings.EMAIL_HOST_USER,
#                 [to_email],
#                 html_message=html_message,
#             )
#             return Response({'message': 'Password reset email sent successfully'}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)