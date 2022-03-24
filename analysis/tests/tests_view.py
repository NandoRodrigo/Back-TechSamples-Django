import json
from django.http import JsonResponse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users.models import User
from analysis.models import Analysis
from classes.models import Class

class AnalysisViewTest(APITestCase):
  def setUp(self) -> None:
    self.user_admin = User.objects.create_user(
        email='admin@gmail.com',
        password='1234',
        first_name='Alex',
        last_name='Silva',
        is_admin=True
    )
    
    self.user_analyst = User.objects.create_user(
        email='analyst2@analyst.com',
        password='1234',
        first_name='Alex',
        last_name='Silva',
        is_admin=False
    )
    
    self.new_class = Class.objects.create(
      name='class_test',
      admin= self.user_admin
    )
  def test_analyst_create_new_analysis(self):
    
    self.new_analysis = {
      "batch": "15sd82135f8",
      "category": "test_category",
      "analyst": self.user_analyst,
      "class_id": self.new_class.uuid,
    }
    
    token = Token.objects.create(user=self.user_analyst)

    self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    
    response = self.client.post('/api/analysis/', self.new_analysis)
    print(response.json())
    
    self.assertEqual(response.status_code, 201)
