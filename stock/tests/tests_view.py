from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from users.models import User
from stock.models import Stock


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

        self.new_stock = {
            'name': 'iode',
            'category': 'example',
        }

        self.consumable_1 = {
            'batch': '85575845',
            'expiration': '2023-04-11',
            'quantity': 10000,
            'unit': 'ml'
        }

        self.consumable_2 = {
            'batch': '85575840',
            'expiration': '2022-04-11',
            'quantity': 5000,
            'unit': 'ml'
        }

    def test_create_new_stock_item(self):
        token = Token.objects.create(user=self.user_admin)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        response = self.client.post('/api/stock/', self.new_stock)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get(
            'admin'), str(self.user_admin.uuid))

    def test_if_analyst_cannot_create_an_item_in_stock(self):
        token = Token.objects.create(user=self.user_analyst)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        response = self.client.post('/api/stock/', self.new_stock)

        self.assertEqual(response.status_code, 403)

    def test_if_reduce_quantity_from_the_older_consumable(self):

        token = Token.objects.create(user=self.user_admin)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        response = self.client.post('/api/stock/', self.new_stock)

        parameter = str(response.data['uuid'])

        self.client.post(
            f'/api/stock/{parameter}/consumables/', self.consumable_1)
        self.client.post(
            f'/api/stock/{parameter}/consumables/', self.consumable_2)

        stock = Stock.objects.get(uuid=parameter)
        subtract = stock.subtract(3000)

        response = self.client.get(f'/api/stock/{parameter}/consumables/')
        ref = {}
        for item in response.data:
            if item['expiration'] == '2022-04-11':
                ref = item

        self.assertEqual(ref['quantity'], 2000)
        self.assertEqual(subtract['total_transfered'], 3000)

    def test_if_dont_transpass_the_maximum_value_in_database(self):
        token = Token.objects.create(user=self.user_admin)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        response = self.client.post('/api/stock/', self.new_stock)

        parameter = str(response.data['uuid'])

        self.client.post(
            f'/api/stock/{parameter}/consumables/', self.consumable_1)
        self.client.post(
            f'/api/stock/{parameter}/consumables/', self.consumable_2)

        stock = Stock.objects.get(uuid=parameter)
        subtract = stock.subtract(30000)

        response = self.client.get(f'/api/stock/{parameter}/consumables/')

        self.assertEqual(response.data[0]['quantity'], 0)
        self.assertEqual(response.data[0]['batch'],
                         subtract['consumables'][1]['batch'])

        self.assertEqual(response.data[1]['quantity'], 0)
        self.assertEqual(response.data[1]['batch'],
                         subtract['consumables'][0]['batch'])

        self.assertEqual(subtract['total_transfered'], 15000)
