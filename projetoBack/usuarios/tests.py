from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from .auth_views import CustomAuthToken

class BaseTestCase(APITestCase):
    """Classe base para testes com configuração comum"""
    pass


class CustomAuthTokenTest(BaseTestCase):
    """Testes para autenticação customizada com tokens"""
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@test.com'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@test.com'
        )
        self.client = APIClient()
        
    def test_login_success_regular_user(self):
        response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn('token', response_data)
        self.assertEqual(response_data['username'], 'testuser')
        self.assertEqual(response_data['user_id'], self.user.id)
        self.assertFalse(response_data['is_staff'])
        
    def test_login_success_admin_user(self):
        response = self.client.post('/api/login/', {
            'username': 'admin',
            'password': 'admin123'
        }, format='json')
        

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn('token', response_data)
        self.assertEqual(response_data['username'], 'admin')
        self.assertTrue(response_data['is_staff'])
        
    def test_login_invalid_credentials(self):
        response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_login_missing_username(self):
        response = self.client.post('/api/login/', {
            'password': 'testpass123'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_login_missing_password(self):
        response = self.client.post('/api/login/', {
            'username': 'testuser'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_token_creation_and_reuse(self):
        # Primeiro login
        response1 = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        response1_data = response1.json()
        self.assertIn('token', response1_data)
        token1 = response1_data['token']
        
        # Segundo login - deve retornar o mesmo token
        response2 = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        response2_data = response2.json()
        self.assertIn('token', response2_data)
        token2 = response2_data['token']
        
        self.assertEqual(token1, token2)


class LogoutTest(BaseTestCase):
    """Testes para funcionalidade de logout"""
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        
    def test_logout_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post('/api/usuarios/logout/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Logout realizado')
        
        # Token deve ter sido deletado
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())
        
    def test_logout_unauthenticated(self):
        response = self.client.post('/api/usuarios/logout/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_logout_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token invalidtoken123')
        response = self.client.post('/api/usuarios/logout/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RevokeTokensTest(BaseTestCase):
    """Testes para revogação de tokens"""
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        
    def test_revoke_current_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        # Não passa all_tokens ou passa como False explicitamente
        response = self.client.post('/api/usuarios/revoke-tokens/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Token atual revogado')
        
        # Token deve ter sido deletado
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())
        
    def test_revoke_all_tokens(self):
        # Remove o token existente e cria um novo para simular múltiplas sessões
        self.token.delete()
        token1 = Token.objects.create(user=self.user)
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token1.key)
        response = self.client.post('/api/usuarios/revoke-tokens/', {
            'all_tokens': True
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Todos os tokens revogados')
        
        # Todos os tokens do usuário devem ter sido deletados
        self.assertEqual(Token.objects.filter(user=self.user).count(), 0)
        
    def test_revoke_tokens_unauthenticated(self):
        response = self.client.post('/api/usuarios/revoke-tokens/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserModelTest(TestCase):
    """Testes para o modelo de usuário"""
    def test_create_regular_user(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@test.com'
        )
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@test.com')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password('testpass123'))
        
    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@test.com'
        )
        
        self.assertEqual(admin.username, 'admin')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.check_password('admin123'))


class TokenModelTest(TestCase):
    """Testes para o modelo de token"""
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_token_creation(self):
        token = Token.objects.create(user=self.user)
        
        self.assertEqual(token.user, self.user)
        self.assertIsNotNone(token.key)
        self.assertEqual(len(token.key), 40)  # Token padrão tem 40 caracteres
        
    def test_token_uniqueness(self):
        token1 = Token.objects.create(user=self.user)
        
        # Tentar criar outro token para o mesmo usuário deve falhar
        with self.assertRaises(Exception):
            Token.objects.create(user=self.user)
            
    def test_get_or_create_token(self):
        # Primeira chamada cria o token
        token1, created1 = Token.objects.get_or_create(user=self.user)
        self.assertTrue(created1)
        
        # Segunda chamada retorna o mesmo token
        token2, created2 = Token.objects.get_or_create(user=self.user)
        self.assertFalse(created2)
        self.assertEqual(token1.key, token2.key)
