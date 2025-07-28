from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from decimal import Decimal
from .models import Gestao, Analise
from .serializers import GestaoSerializer, AnaliseSerializer

class BaseTestCase(APITestCase):
    """Classe base para testes com configuração comum"""
    pass


class GestaoModelTest(TestCase):
    """Testes para o modelo Gestao"""
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_gestao_creation(self):
        gestao = Gestao.objects.create(
            usuario=self.user,
            aparelho='Geladeira',
            consumo='150',
            tempo='24',
            dias_de_uso=30
        )
        self.assertEqual(gestao.aparelho, 'Geladeira')
        self.assertEqual(gestao.consumo, '150')
        self.assertEqual(gestao.tempo, '24')
        self.assertEqual(gestao.dias_de_uso, 30)
        self.assertEqual(str(gestao), 'Geladeira')
        
    def test_gestao_without_user(self):
        gestao = Gestao.objects.create(
            aparelho='TV',
            consumo='100',
            tempo='8',
            dias_de_uso=30
        )
        self.assertIsNone(gestao.usuario)


class AnaliseModelTest(TestCase):
    """Testes para o modelo Analise"""
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.gestao = Gestao.objects.create(
            usuario=self.user,
            aparelho='Ar Condicionado',
            consumo='1500',
            tempo='8',
            dias_de_uso=30
        )
        
    def test_analise_auto_creation(self):
        # Analise deve ser criada automaticamente via signal
        self.assertTrue(hasattr(self.gestao, 'analise'))
        
    def test_analise_calculation(self):
        analise = self.gestao.analise
        # 1500W * 8h * 30 dias = 360 kWh
        expected_kwh = Decimal('360.00')
        # 360 kWh * R$ 0.92 = R$ 331.20
        expected_cost = Decimal('331.20')
        
        self.assertEqual(analise.consumo_mensal_kwh, expected_kwh)
        self.assertEqual(analise.custo_mensal_reais, expected_cost)
        
    def test_analise_str_method(self):
        analise = self.gestao.analise
        self.assertEqual(str(analise), 'Análise de Ar Condicionado')
        
    def test_analise_recalculation_on_update(self):
        # Atualiza dados da gestão
        self.gestao.consumo = '2000'
        self.gestao.tempo = '10'
        self.gestao.save()
        
        # Recarrega a análise
        analise = Analise.objects.get(gestao=self.gestao)
        # 2000W * 10h * 30 dias = 600 kWh
        expected_kwh = Decimal('600.00')
        self.assertEqual(analise.consumo_mensal_kwh, expected_kwh)


class GestaoSerializerTest(TestCase):
    """Testes para o serializer de Gestao"""
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_gestao_serializer_valid_data(self):
        data = {
            'aparelho': 'Microondas',
            'consumo': '800',
            'tempo': '1',
            'dias_de_uso': 30,
            'usuario': self.user.id
        }
        serializer = GestaoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
    def test_gestao_serializer_invalid_data(self):
        data = {
            'aparelho': '',  # Campo obrigatório vazio
            'consumo': '800',
            'tempo': '1',
            'dias_de_uso': 30
        }
        serializer = GestaoSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class GestaoAPITest(BaseTestCase):
    """Testes para a API de Gestao"""
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@test.com'
        )
        self.token = Token.objects.create(user=self.user)
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.client = APIClient()
        
        self.gestao_data = {
            'aparelho': 'Notebook',
            'consumo': '65',
            'tempo': '8',
            'dias_de_uso': 22
        }
        
    def test_create_gestao_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post('/api/gestao/aparelhos/', self.gestao_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['aparelho'], 'Notebook')
        
    def test_create_gestao_unauthenticated(self):
        response = self.client.post('/api/gestao/aparelhos/', self.gestao_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_list_gestao_user_only_sees_own(self):
        # Cria aparelhos para diferentes usuários
        Gestao.objects.create(usuario=self.user, aparelho='TV User', consumo='100', tempo='4', dias_de_uso=30)
        Gestao.objects.create(usuario=self.admin_user, aparelho='TV Admin', consumo='100', tempo='4', dias_de_uso=30)
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/gestao/aparelhos/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['aparelho'], 'TV User')
        
    def test_list_gestao_admin_sees_all(self):
        Gestao.objects.create(usuario=self.user, aparelho='TV User', consumo='100', tempo='4', dias_de_uso=30)
        Gestao.objects.create(usuario=self.admin_user, aparelho='TV Admin', consumo='100', tempo='4', dias_de_uso=30)
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get('/api/gestao/aparelhos/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_update_gestao(self):
        gestao = Gestao.objects.create(
            usuario=self.user,
            aparelho='Ventilador',
            consumo='60',
            tempo='12',
            dias_de_uso=30
        )
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        updated_data = {
            'aparelho': 'Ventilador Atualizado',
            'consumo': '80',
            'tempo': '10',
            'dias_de_uso': 25
        }
        response = self.client.put(f'/api/gestao/aparelhos/{gestao.id}/', updated_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['aparelho'], 'Ventilador Atualizado')
        
    def test_delete_gestao_own_device(self):
        gestao = Gestao.objects.create(
            usuario=self.user,
            aparelho='Impressora',
            consumo='30',
            tempo='2',
            dias_de_uso=20
        )
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(f'/api/gestao/aparelhos/{gestao.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Gestao.objects.filter(id=gestao.id).exists())
        
    def test_delete_gestao_other_user_device(self):
        gestao = Gestao.objects.create(
            usuario=self.admin_user,
            aparelho='Roteador',
            consumo='15',
            tempo='24',
            dias_de_uso=30
        )
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(f'/api/gestao/aparelhos/{gestao.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AnaliseAPITest(BaseTestCase):
    """Testes para a API de Analise"""
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        
        self.gestao = Gestao.objects.create(
            usuario=self.user,
            aparelho='Chuveiro Elétrico',
            consumo='5500',
            tempo='1',
            dias_de_uso=30
        )
        
    def test_list_analises(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/gestao/analises/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['gestao']['aparelho'], 'Chuveiro Elétrico')
        
    def test_analise_readonly(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post('/api/gestao/analises/', {})
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class AuthenticationTest(BaseTestCase):
    """Testes de autenticação integrados"""
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        
    def test_login_valid_credentials(self):
        response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn('token', response_data)
        self.assertEqual(response_data['username'], 'testuser')
        
    def test_login_invalid_credentials(self):
        response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_logout(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        response = self.client.post('/api/usuarios/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Token deve ter sido deletado
        self.assertFalse(Token.objects.filter(key=token.key).exists())
