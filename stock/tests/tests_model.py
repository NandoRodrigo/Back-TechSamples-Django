from django.test import TestCase

from users.models import User
from stock.models import Stock

class StockTestModel(TestCase):

  @classmethod
  def setUpTestData(cls) -> None:

    cls.admin = User.objects.create_user(
      email='email@email.com',
      password='1234',
      is_admin=True
    )

    cls.name = 'test_name'
    cls.category = 'test_category'

    cls.stock = Stock.objects.create(
      name=cls.name,
      category=cls.category,
      admin=cls.admin
    )
    
  def test_stock_fields(self):
    self.assertIsInstance(self.stock.name, str)
    self.assertIsInstance(self.stock.category, str)
    
    self.assertEqual(self.stock.name, self.name)
    self.assertEqual(self.stock.admin.is_admin, True)
    self.assertEqual(self.stock.admin, self.admin)
