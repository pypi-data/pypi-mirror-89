from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token as Rest_Token, Token
from unchained_auth.serializers.main import UserSerializer


class RegisterAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                new_user = get_user_model()(
                    email=request.data['email'],
                    first_name=request.data['first_name'],
                    last_name=request.data['last_name'],
                )
                new_user.set_password(request.data['password'])
                new_user.save()
                token, _ = Token.objects.get_or_create(user=new_user)
                return Response({
                    'token': token.key,
                    'code': token.user.code,
                },
                    status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'User already exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(LoginView, self).post(request, *args, **kwargs)
        token = Rest_Token.objects.get(key=response.data['token'])

        # related_values = {}
        # for f in request.user._meta.get_fields():
        #     if f.auto_created and not f.concrete and hasattr(f.related_model, 'include_profile') and f.related_model.include_profile:
        #         values = f.related_model.objects.filter(**{f.field.name: request.user})
        #         if values:
        #             related_values[f.related_model._meta.model_name] = list(values.values_list('pk', flat=True))
        # print(related_values)
        #
        return Response({
            'token': token.key,
            'user_id': token.user_id,
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
