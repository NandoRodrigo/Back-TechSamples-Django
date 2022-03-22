from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from users.models import User


class StockItemCreateTestView(APITestCase):
    def setUp(self):
        self.user_admin = User.objects.create(
            first_name='Adm',
            last_name='In',
            email='admin@mail.com',
            password='1234',
            is_admin=True
        )

        self.user_analyst = User.objects.create(
            first_name='Ana',
            last_name='Lyst',
            email='analyst@mail.com',
            password='1234',
            is_admin=False
        )

    def test_create_new_stock_item(self):
        self.new_stock = {
            'name': 'iodo',
            'category': 'example',
        }

        token = Token.objects.create(user=self.user_admin)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        response = self.client.post(
            '/api/stock/', self.new_stock)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get(
            'admin'), str(self.user_admin.uuid))

    def test_if_analyst_can_not_create_an_item_in_stock(self):
        self.new_stock = {
            'name': 'iodo',
            'category': 'example',
        }

        token = Token.objects.create(user=self.user_analyst)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        response = self.client.post(
            '/api/stock/', self.new_stock)

        self.assertEqual(response.status_code, 403)
