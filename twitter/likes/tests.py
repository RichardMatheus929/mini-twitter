from django.test import TestCase
from django.core.cache import cache
from rest_framework.test import APIClient

from twitter.accounts.utils import create_user, authenticate_client

class LikesUnityTest(TestCase):

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

    def test_like_post(self):
        """
        Testa o sistema de likes.
        """

        # Cria um post com o primeiro usuário
        response = self.client.post('/api/v1/posts/', {
            'content': 'Post de teste'
        }, format='json')
        self.assertEqual(response.status_code, 201)
        post_id = response.data['id']

        # Cria e autentica segundo usuário
        self.second_user = create_user(
            name='Outro Usuário',
            email='outro@gmail.com',
            username='outrousername',
            password=self.password
        )
        authenticate_client(self.client, self.second_user.email, self.password) 

        # Tenta curtir sem seguir — deve falhar
        response = self.client.post(f'/api/v1/likes/', {"post_id": post_id}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Você não pode curtir este post, pois não segue o usuário.', str(response.data))

