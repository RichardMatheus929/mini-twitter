from twitter.accounts.models import User
from rest_framework.test import APIClient

"""
Funções utilitárias para criar usuários e autenticar clientes para testes.
"""

def create_user(name="Usuário Teste", email="teste@example.com", username="testuser", password="senha123"):
    return User.objects.create_user(
        name=name,
        email=email,
        username=username,
        password=password
    )

def authenticate_client(client, email, password):
    response = client.post('/api/v1/accounts/signin', {
        'email': email,
        'password': password
    }, format='json')
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return token
