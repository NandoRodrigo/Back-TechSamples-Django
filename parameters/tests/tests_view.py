from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from classes.models import Class
from parameters.models import Parameter
from users.models import User
from class_types.models import Type

class FeeViewTest(APITestCase):
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

    self.new_type = Type.objects.create(
      name='type_test',
      class_type= self.new_class
    )
    
  def test_create_new_parameter(self):
    self.new_parameter = {
      "name": "teor de sódio",
		  "unit": "%",
		  "minimum": "15",
		  "maximum": "37",
      "type": self.new_type
    }
    
    token = Token.objects.create(user=self.user_admin)

    self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    
    response = self.client.post(f'/api/classes/types/{self.new_type.uuid}/parameters/', self.new_parameter)
    
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json()['type'], self.new_type.name)
    
  def test_delete_parameter(self):
    self.new_parameter = Parameter.objects.create(
      name = "teor de sódio",
		  unit = "%",
		  minimum = "15",
		  maximum = "37",
      type = self.new_type
    )
    
 
    
    token = Token.objects.create(user=self.user_admin)

    self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    
    response = self.client.delete(f'/api/classes/types/parameters/{self.new_parameter.uuid}/')
    
    self.assertEqual(response.status_code, 204)
    
    