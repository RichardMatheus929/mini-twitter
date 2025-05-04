from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.core.cache import cache
from rest_framework.test import APIClient

from twitter.accounts.utils import create_user, authenticate_client

class PotsUnityTest(TestCase):
    """
    Testa o sistema de posts.
    """

    def setUp(self):
        cache.clear()

        self.client = APIClient()
        self.password = 'senha123'

        self.user = create_user(
            name='Usuário Teste',
            email='teste@example.com',
            username='testuser',
            password=self.password
        )

        authenticate_client(self.client, self.user.email, self.password)

   
    def test_create_post(self):
        """
        Testa a criação de posts.
        """

        # Cria um post
        response = self.client.post('/api/v1/posts/', {
            'content': 'Post de teste'
        }, format='json')
        self.assertEqual(response.status_code, 201)

        # Verifica se o post foi criado corretamente
        response = self.client.get(f'/api/v1/posts/{response.data["id"]}/', format='json')
        self.assertEqual(response.data["user"], self.user.username)

        
