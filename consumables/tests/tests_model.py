from django.test import TestCase
from datetime import date

from users.models import User
from stock.models import Stock
from consumables.models import Consumable

class ConsumablesTestModel(TestCase):

  @classmethod
  def setUpTestData(cls) -> None:

    cls.admin = User.objects.create_user(
      email='email@email.com',
      password='1234',
      is_admin=True
    )

    cls.stock = Stock.objects.create(
      name='test_name',
      category='test_category',
      admin=cls.admin
    )

    cls.batch = '123456789'
    cls.expiration = date.fromisoformat("2020-04-15")
    cls.quantity = 100
    cls.unit = 'grs'

    cls.consumable = Consumable.objects.create(
      batch = cls.batch,
      expiration = cls.expiration,
      quantity = cls.quantity,
      unit = cls.unit,
      stock = cls.stock
    )
    
  def test_consumable_fields(self):
    self.assertIsInstance(self.consumable.batch, str)
    self.assertIsInstance(self.consumable.quantity, int)
    self.assertIsInstance(self.consumable.expiration, date)
    
    self.assertEqual(self.consumable.batch, self.batch)
    self.assertEqual(self.consumable.stock.admin, self.admin)
    self.assertEqual(self.consumable.stock.admin.is_admin, True)
    self.assertEqual(self.consumable.stock, self.stock)