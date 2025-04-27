from django.contrib.auth.hashers import check_password, make_password

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed, APIException

from twitter.accounts.serializers import UserSerializer
from twitter.accounts.models import User

import re

class Signin(APIView):
    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        user_exist = User.objects.filter(email=email).exists()

        if not user_exist:
            raise AuthenticationFailed(
                f'Email ({email}) incorreto ou não existente')

        user = User.objects.filter(email=email).first()

        if not check_password(password, user.password):
            raise AuthenticationFailed(
                f'Senha errada para o email {email}')


        token = RefreshToken.for_user(user)

        serializer = UserSerializer(user)

        return Response({
            'user': serializer.data,
            'refresh': str(token),
            'access': str(token.access_token)
        })
    

class Signup(APIView):

    def post(self,request):
        name = request.data.get('name')
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        if not name or name == "":
            raise APIException('O nome não deve ser nulo')
        if not email or email == "":
            raise APIException('O email não deve ser nulo')
        if not "@" in email or len(email) < 8:
            raise APIException('O email é inválido ou muito curto')

        if not password or password == "":
            raise APIException('O password não deve ser nulo')

        
        if User.objects.filter(email=email).exists():
            raise APIException('O email já existe')

        password_hashed = make_password(password)

        created_user = User.objects.create(
            name=name,
            email=email,
            username=username,
            password=password_hashed,
        )

        serializer = UserSerializer(created_user)

        return Response({
            'user':serializer.data,
            'criado em': created_user.create_account
        })