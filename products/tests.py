from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from .models import Category, Product
from rest_framework_simplejwt.tokens import RefreshToken


class ApiTests(APITestCase):
    def test_precio_final_autenticado(self):
        user = get_user_model().objects.get(username='prueba')
        self.client.force_authenticate(user=None)
        token = str(RefreshToken.for_user(user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        ropa = Category.objects.create(name='Ropa')
        camisa = Product.objects.create(
            name='Camisa', category=ropa, description='Algodon', price='500.00')
        for producto, esperado in [(self.product, '13500.00'), (camisa, '400.00')]:
            response = self.client.get(
                f'/api/v1/products/{producto.pk}/precio-final/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['precio_final'], esperado)
            self.assertEqual(response.data['categoria'], producto.category.name)

    def test_precio_final_sin_autenticar(self):
        self.client.force_authenticate(user=None)
        self.client.credentials()
        response = self.client.get(
            f'/api/v1/products/{self.product.pk}/precio-final/')
        self.assertEqual(response.status_code, 401)

    def setUp(self):
        user = get_user_model().objects.create_user('prueba', password='Prueba-2026!')
        self.client.force_authenticate(user=user)
        self.category = Category.objects.create(name='Electronica')
        self.product = Product.objects.create(
            name='Laptop', category=self.category,
            description='Laptop HP', price='15000.00')

    def test_create_category(self):
        response = self.client.post('/api/categories/', {'name': 'Ropa'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.get(pk=response.data['id']).name, 'Ropa')

    def test_list_categories(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{'id': self.category.pk, 'name': 'Electronica'}])

    def test_create_product(self):
        response = self.client.post('/api/products/', {
            'name': 'Mouse', 'category_id': self.category.pk,
            'description': 'Mouse inalambrico', 'price': '500.00'}, format='json')
        self.assertEqual(response.status_code, 201)
        product = Product.objects.get(pk=response.data['id'])
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual((product.name, product.category_id), ('Mouse', self.category.pk))
        self.assertEqual(product.price, Decimal('500.00'))
        self.assertEqual(response.data['category'], 'Electronica')

    def test_list_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.product.pk)
        self.assertEqual(response.data[0]['category'], 'Electronica')

    def test_update_product(self):
        category = Category.objects.create(name='Computadoras')
        response = self.client.put(f'/api/products/{self.product.pk}/', {
            'name': 'Laptop Pro', 'category_id': category.pk,
            'description': 'Laptop actualizada', 'price': '18000.00'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Laptop Pro')
        self.assertEqual(self.product.description, 'Laptop actualizada')
        self.assertEqual(self.product.price, Decimal('18000.00'))
        self.assertEqual(self.product.category_id, category.pk)

    def test_delete_product(self):
        url = f'/api/products/{self.product.pk}/'
        self.assertEqual(self.client.delete(url).status_code, 204)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertTrue(Category.objects.filter(pk=self.category.pk).exists())
