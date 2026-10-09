from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from .models import Category, Product


class JWTTests(APITestCase):
    def setUp(self):
        get_user_model().objects.create_user('jwt_test', password='Test-jwt-2026!')
        self.category = Category.objects.create(name='Prueba')
        Product.objects.create(name='Producto', category=self.category, description='Prueba', price=10)

    def test_login_access_filter_and_refresh(self):
        for route in ['/api/products/', '/api/categories/', '/api/v1/products/']:
            self.assertEqual(self.client.get(route).status_code, 401)
        response = self.client.post('/api/token/', {'username':'jwt_test', 'password':'Test-jwt-2026!'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+response.data['access'])
        result = self.client.get('/api/products/', {'category':self.category.pk})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data[0]['category'], 'Prueba')
        self.assertEqual(self.client.get('/api/categories/').status_code, 200)
        self.client.credentials()
        refreshed = self.client.post('/api/token/refresh/', {'refresh':response.data['refresh']}, format='json')
        self.assertEqual(refreshed.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+refreshed.data['access'])
        self.assertEqual(self.client.get('/api/products/').status_code, 200)

    def test_invalid_credentials_and_token(self):
        response = self.client.post('/api/token/', {'username':'jwt_test', 'password':'incorrecta'}, format='json')
        self.assertEqual(response.status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer token-invalido')
        self.assertEqual(self.client.get('/api/products/').status_code, 401)
