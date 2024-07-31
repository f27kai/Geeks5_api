from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth.models import User
from .serializers import UserCreateSerializer, UserLoginSerializer, SMScodeSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
from .models import SmsCode
from rest_framework.views import APIView




class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            email=serializer.validated_data['email'],
            is_active=False
        )

        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        SmsCode.objects.create(code=code, user=user)

        send_mail(
            'Your Verification Code',
            f'Your verification code is: {code}',
            'your-email@example.com',
            [user.email],
            fail_silently=False
        )

        return Response(data={'user_id': user.id}, status=status.HTTP_201_CREATED)

class SMSConfirmationAPIView(generics.CreateAPIView):
    serializer_class = SMScodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['SMS']

        try:
            sms = SmsCode.objects.get(code=code)
        except SmsCode.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid code'})

        user = sms.user
        if user.is_active:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'User is already active'})

        user.is_active = True
        user.save()
        sms.delete()

        return Response(data={'active': True}, status=status.HTTP_200_OK)


class UserLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if user:
            if user.is_active:
                token, _ = Token.objects.get_or_create(user=user)
                return Response(data={'key': token.key})
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'error': 'Account is not active'})
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'error': 'Invalid username or password'})






# @api_view(['POST'])
# def registration_api_view(request):
#     serializer = UserCreateSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#
#
#     user = User.objects.create_user(
#         username=serializer.validated_data['username'],
#         password=serializer.validated_data['password'],
#         email=serializer.validated_data['email'],
#         is_active=False
#     )
#
#
#     code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
#     SmsCode.objects.create(code=code, user=user)
#
#     send_mail(
#         'Your Verification Code',
#         f'Your verification code is: {code}',
#         'your-email@example.com',
#         [user.email],
#         fail_silently=False
#     )
#
#     return Response(data={'user_id': user.id}, status=status.HTTP_201_CREATED)
#
#
# @api_view(['POST'])
# def login_api_view(request):
#     serializer = UserLoginSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#
#     user = authenticate(**serializer.validated_data)
#     if user:
#         if user.is_active:
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response(data={'key': token.key})
#         return Response(status=status.HTTP_401_UNAUTHORIZED, data={'error': 'Account is not active'})
#     return Response(status=status.HTTP_401_UNAUTHORIZED, data={'error': 'Invalid username or password'})
#
#
# @api_view(['POST'])
# def confirm_sms_api_view(request):
#     serializer = SMScodeSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     code = serializer.validated_data['SMS']
#
#     try:
#         sms = SmsCode.objects.get(code=code)
#     except SmsCode.DoesNotExist:
#         return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid code'})
#
#
#     user = sms.user
#     if user.is_active:
#         return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'User is already active'})
#
#     user.is_active = True
#     user.save()
#     sms.delete()
#
#     return Response(data={'active': True}, status=status.HTTP_200_OK)
