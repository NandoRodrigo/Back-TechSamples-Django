from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users.models import User


class UserViewTest(APITestCase):

  def setUp(self) -> None:
    self.user_admin = User.objects.create_user(
      email='admin@gmail.com',
      password='1234',
      first_name='Alex',
      last_name='Silva',
      is_admin=True
    )

    self.user_analyst = User.objects.create_user(
      email='analyst@gmail.com',
      password='1234',
      first_name='Alex',
      last_name='Silva',
      is_admin=False
    )

  def test_create_new_user_success(self):
    user_data = {
      'email': 'userdata@email.com',
      'password': '1234',
      'first_name': 'Alex',
      'last_name': 'Silva',
      'is_admin': True
    }

    response = self.client.post('/api/signup/', user_data)

    self.assertEqual(response.status_code, 201)
    self.assertNotIn('password', response.json())

  def test_create_new_user_fail(self):

    user_data = {
      'password': '1234',
      'first_name': 'Alex',
      'last_name': 'Silva',
      'is_admin': True
    }

    response = self.client.post('/api/signup/', user_data)

    self.assertEqual(response.status_code, 400)

  def test_only_admin_can_read_users(self):

    token = Token.objects.create(user=self.user_admin)

    self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    response = self.client.get('/api/admin/analyst')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.json()), 2)

  def test_not_admin_cannot_read_users(self):

    token = Token.objects.create(user=self.user_analyst)

    self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    response = self.client.get('/api/admin/analyst')

    self.assertEqual(response.status_code, 403)

  def test_analyst_cannot_create_analyst(self):

    self.analyst = {
      'email': 'analyst@email.com',
      'password': '1234',
      'first_name': 'Alex',
      'last_name': 'Silva',
      'is_admin': False
    }

    token = Token.objects.create(user=self.user_analyst)

    self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    response = self.client.post('/api/admin/analyst', self.analyst)

    self.assertEqual(response.status_code, 403)


class LoginTestView(APITestCase):
  def setUp(self) -> None:
    User.objects.create_user(
      email='email@gmail.com',
      password='1234',
      first_name='Alex',
      last_name='Silva',
      is_admin=True
    )

  def test_login_success(self):
    login_data = {
      'email': 'email@gmail.com',
      'password': '1234',
    }

    response = self.client.post('/api/login/', login_data)

    self.assertEqual(response.status_code, 200)
    self.assertIn('token', response.json())

  def test_login_fail(self):
    login_data = {
      'email': 'email@gmail.com',
      'password': '124',
    }

    response = self.client.post('/api/login/', login_data)

    self.assertEqual(response.status_code, 401)
