from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from users.models import User
from stock.models import Stock


class ConsumableCreateTestView(APITestCase):
    def setUp(self) -> None:
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

        self.stock = Stock.objects.create(
            name='iodo',
            category='example',
            admin=self.user_admin
        )

    def test_create_new_consumable(self):
        self.consumable = {
            'batch': '85575844',
            'expiration': '2022-04-11',
            'quantity': 10000,
            'unit': 'ml',
            'stock': self.stock
        }

        token = Token.objects.create(user=self.user_admin)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        parameter = str(self.stock.uuid)

        response = self.client.post(
            f'/api/stock/{parameter}/consumables/', self.consumable)

        self.assertEqual(response.status_code, 201)
