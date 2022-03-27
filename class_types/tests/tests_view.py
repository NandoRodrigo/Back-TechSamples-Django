from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from classes.models import Class
from users.models import User
from class_types.models import Type

class TypeViewTest(APITestCase):
  def setUp(self) -> None:
    self.user_admin = User.objects.create_user(
        email='admin@gmail.com',
        password='1234',
        first_name='Alex',
        last_name='Silva',
        is_admin=True
    )
    
    self.new_class = Class.objects.create(
      name='class_test',
      admin= self.user_admin
    )
    
  def test_create_new_type(self):
    self.new_type = {
      "name": 'type_test',
      "class_type": self.new_class
    }
    
    token = Token.objects.create(user=self.user_admin)

    self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    
    response = self.client.post(f'/api/classes/{self.new_class.uuid}/types/', self.new_type)
    
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json()['class_type'], self.new_class.name)
    
  def test_update_type_name(self):
    self.new_type = Type.objects.create(
      name='type_test',
      class_type = self.new_class
    )
    
    self.toUpdate = {
      "name": 'updated'
    }
    
    token = Token.objects.create(user=self.user_admin)

    self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    
    response = self.client.patch(f'/api/classes/types/{self.new_type.uuid}/', self.toUpdate)
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['name'], self.toUpdate['name'])
    