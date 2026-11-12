from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import UserSerializer

User = get_user_model()

class UserSecurityTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin_test', 'admin@example.com', 'Admin-Seguro-2026!')
        self.target = User.objects.create_user('cliente', 'cliente@example.com', 'Cliente-Seguro-2026!', telefono='6621234567')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(AccessToken.for_user(self.admin)))
        self.url = f'/api/v1/users/{self.target.pk}/'

    def test_patch_sin_password_conserva_hash_y_login(self):
        before = self.target.password
        response = self.client.patch(self.url, {'first_name': 'Nombre nuevo'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.target.refresh_from_db()
        self.assertEqual(self.target.password, before)
        self.assertNotEqual(self.target.password, self.admin.password)
        self.assertTrue(self.target.check_password('Cliente-Seguro-2026!'))
        self.assertFalse(self.target.check_password('Admin-Seguro-2026!'))
        self.assertNotIn('password', response.data)
        self.client.credentials()
        self.assertEqual(self.client.post('/api/v1/auth/token/', {'email': self.target.email, 'password': 'Cliente-Seguro-2026!'}).status_code, 200)

    def test_put_sin_password_conserva_hash(self):
        before = self.target.password
        response = self.client.put(self.url, {'username': 'cliente', 'email': self.target.email, 'telefono': '6627654321'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.target.refresh_from_db()
        self.assertEqual(self.target.password, before)
        self.assertNotIn('password', response.data)

    def test_password_nuevo_se_guarda_con_hash(self):
        response = self.client.patch(self.url, {'password': 'Nueva-Clave-2026!'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.target.refresh_from_db()
        self.assertTrue(self.target.check_password('Nueva-Clave-2026!'))
        self.assertFalse(self.target.check_password('Cliente-Seguro-2026!'))
        self.assertNotIn('password', response.data)

    def test_password_vacio_no_modifica_hash(self):
        before = self.target.password
        self.assertEqual(self.client.patch(self.url, {'password': ''}, format='json').status_code, 400)
        self.target.refresh_from_db()
        self.assertEqual(self.target.password, before)

    def test_password_nunca_en_respuestas(self):
        for url in ['/api/v1/users/', self.url, '/api/v1/auth/me/']:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            records = response.data if isinstance(response.data, list) else [response.data]
            for record in records:
                self.assertNotIn('password', record)
                self.assertNotIn(self.target.password, str(record))
        self.assertTrue(UserSerializer().fields['password'].write_only)

    def test_crear_usuario_requiere_password_y_oculta_hash(self):
        data = {'username': 'nuevo', 'email': 'nuevo@example.com', 'telefono': '6625551234'}
        self.assertEqual(self.client.post('/api/v1/users/', data).status_code, 400)
        data['password'] = 'Nuevo-Seguro-2026!'
        response = self.client.post('/api/v1/users/', data)
        self.assertEqual(response.status_code, 201)
        self.assertNotIn('password', response.data)
        self.assertEqual(response.data['telefono'], '6625551234')
        self.assertTrue(User.objects.get(email=data['email']).check_password(data['password']))

    def test_roles_y_datos_personales(self):
        self.client.credentials()
        self.assertEqual(self.client.get('/api/v1/auth/me/').status_code, 401)
        self.assertEqual(self.client.get('/api/v1/users/').status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(AccessToken.for_user(self.target)))
        self.assertEqual(self.client.get('/api/v1/users/').status_code, 403)
        response = self.client.get('/api/v1/auth/me/')
        self.assertEqual(response.data['email'], self.target.email)
        self.assertNotIn('password', response.data)

    def test_login_email_y_token_30_minutos(self):
        self.client.credentials()
        response = self.client.post('/api/v1/auth/token/', {'email': self.target.email, 'password': 'Cliente-Seguro-2026!'})
        self.assertEqual(response.status_code, 200)
        token = AccessToken(response.data['access'])
        self.assertEqual(token['exp'] - token['iat'], 1800)
        self.assertEqual(self.client.post('/api/v1/auth/token/', {'email': self.target.email, 'password': 'incorrecta'}).status_code, 401)

    def test_validacion_telefono_y_correo(self):
        self.assertEqual(self.client.patch(self.url, {'telefono': 'abc'}).status_code, 400)
        self.assertEqual(self.client.patch(self.url, {'email': 'ADMIN@example.com'}).status_code, 400)

    def test_eliminar_usuario(self):
        self.assertEqual(self.client.delete(self.url).status_code, 204)
        self.assertFalse(User.objects.filter(pk=self.target.pk).exists())

    def test_swagger_titulo_campo_extra_y_respuesta_sin_password(self):
        self.client.credentials()
        response = self.client.get('/swagger.json')
        self.assertEqual(response.status_code, 200)
        schema = response.json()
        self.assertEqual(schema['info']['title'], 'CentiStore API')
        self.assertIn('telefono', schema['definitions']['User']['properties'])
        self.assertNotIn('password', schema['definitions']['UserRead']['properties'])
