from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from classes.models import Class
from users.models import User


class ClassViewTest(APITestCase):
  def setUp(self) -> None:
    self.user_admin = User.objects.create_user(
        email='admin@gmail.com',
        password='1234',
        first_name='Alex',
        last_name='Silva',
        is_admin=True
    )
    
    self.user_analyst = User.objects.create_user(
        email='notadmin@gmail.com',
        password='1234',
        first_name='Alex',
        last_name='Silva',
        is_admin=False
    )
    
  def test_admin_create_new_class(self):
    self.new_class = {
      "name": "refrigerante",
      "admin": self.user_admin
    }
    
    token = Token.objects.create(user=self.user_admin)

    self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    
    response = self.client.post('/api/classes/', self.new_class)
    
    self.assertEqual(response.status_code, 201)
    
  def test_analyst_cannot_create_new_class(self):
    self.new_class = {
      "name": "refrigerante",
      "admin": self.user_analyst
    }
    
    token = Token.objects.create(user=self.user_analyst)

    self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    
    response = self.client.post('/api/classes/', self.new_class)
    
    self.assertEqual(response.status_code, 403)
    
  def test_list_all_classes(self):
    self.new_class1 = Class.objects.create(
      name='class_1',
      admin=self.user_admin
    )
    
    self.new_class2 = Class.objects.create(
      name='class_2',
      admin=self.user_admin
    )
    
    self.new_class3 = Class.objects.create(
      name='class_3',
      admin=self.user_admin
    )

    token = Token.objects.create(user=self.user_analyst)

    self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    
    response = self.client.get('/api/classes/')
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.json()), 3)
    self.assertIsInstance(response.json(), list)