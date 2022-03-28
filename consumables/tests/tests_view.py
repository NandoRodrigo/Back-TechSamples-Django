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

        self.stock_1 = Stock.objects.create(
            name='iode',
            category='example',
            admin=self.user_admin
        )

        self.stock_2 = Stock.objects.create(
            name='alcohol',
            category='example',
            admin=self.user_admin
        )

        self.consumable_1 = {
            'batch': '85575844',
            'expiration': '2022-04-11',
            'quantity': 10000,
            'unit': 'ml'
        }

        self.consumable_2 = {
            'batch': '85575844',
            'expiration': '2022-04-11',
            'quantity': 5000,
            'unit': 'ml'
        }

        self.consumable_3 = {
            'batch': '85575845',
            'expiration': '2022-04-11',
            'quantity': 2000,
            'unit': 'ml'
        }

        self.consumable_4 = {
            'batch': '85575844',
            'expiration': '2022-04-11',
            'quantity': 8000,
            'unit': 'ml'
        }

    def test_create_new_consumable(self):

        token = Token.objects.create(user=self.user_admin)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        parameter = str(self.stock_1.uuid)

        response = self.client.post(
            f'/api/stock/{parameter}/consumables/', self.consumable_1)

        self.assertEqual(response.status_code, 201)

    def test_if_add_items_with_same_batch(self):

        token = Token.objects.create(user=self.user_admin)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        parameter = str(self.stock_1.uuid)

        self.client.post(
            f'/api/stock/{parameter}/consumables/', self.consumable_1)

        self.client.post(
            f'/api/stock/{parameter}/consumables/', self.consumable_2)

        response = self.client.get(f'/api/stock/{parameter}/consumables/')

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['quantity'], 15000)

    def test_if_analyst_cannot_create_a_consumable_item(self):
        token = Token.objects.create(user=self.user_analyst)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        parameter = str(self.stock_1.uuid)

        response = self.client.post(
            f'/api/stock/{parameter}/consumables/', self.consumable_1)

        self.assertEqual(response.status_code, 403)

    def test_if_consumables_are_created_in_correct_stock(self):
        token = Token.objects.create(user=self.user_admin)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        parameter_1 = str(self.stock_1.uuid)
        parameter_2 = str(self.stock_2.uuid)

        self.client.post(
            f'/api/stock/{parameter_1}/consumables/', self.consumable_1)
        self.client.post(
            f'/api/stock/{parameter_1}/consumables/', self.consumable_2)
        self.client.post(
            f'/api/stock/{parameter_1}/consumables/', self.consumable_3)
        self.client.post(
            f'/api/stock/{parameter_2}/consumables/', self.consumable_4)

        response_1 = self.client.get(f'/api/stock/{parameter_1}/consumables/')
        response_2 = self.client.get(f'/api/stock/{parameter_2}/consumables/')

        self.assertEqual(len(response_1.data), 2)
        self.assertEqual(response_1.data[0]['quantity'], 15000)
        self.assertEqual(response_1.data[1]['quantity'], 2000)

        self.assertEqual(len(response_2.data), 1)
        self.assertEqual(response_2.data[0]['quantity'], 8000)
