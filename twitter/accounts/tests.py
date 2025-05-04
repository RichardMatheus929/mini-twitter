from django.test import TestCase

from twitter.accounts.models import User

from rest_framework.test import APIClient
# Create your tests here.
class UserLoginUnityTest(TestCase):
    """
    Testa o login do usuário.
    """

    def setUp(self):

        self.client = APIClient()

        self.user = User.objects.create_user(
            name='Test User',
            email='emailteste@gmail.com',
            username='testuser',
            password='testpassword'
        )

    def test_login(self):
        response = self.client.post('/api/v1/accounts/signin', {
            'email': 'emailteste@gmail.com',
            'password': 'testpassword'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post('/api/v1/accounts/signin', {
            'email': '',
            'password': 'wrongpassword'
        })

        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)
        self.assertNotIn('access', response.data)
