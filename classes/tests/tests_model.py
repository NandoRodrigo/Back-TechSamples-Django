from django.test import TestCase

from users.models import User
from stock.models import Stock
from classes.models import Class


class ClassTestModel(TestCase):

  @classmethod
  def setUpTestData(cls) -> None:

    cls.admin = User.objects.create_user(
      email='email@email.com',
      password='1234',
      is_admin=True
    )

    cls.name = 'test_class'

    cls.new_class = Class.objects.create(
      name=cls.name,
      admin=cls.admin
    )

  def test_class_fields(self):
    self.assertIsInstance(self.new_class.name, str)

    self.assertEqual(self.new_class.name, self.name)
    self.assertEqual(self.new_class.admin, self.admin)
    self.assertEqual(self.new_class.admin.is_admin, True)

  def test_relationship_class_stock(self):

    stock1 = Stock.objects.create(
      name='test_name1',
      category='test_category',
      admin=self.admin
    )

    stock2 = Stock.objects.create(
      name='test_name2',
      category='test_category',
      admin=self.admin
    )

    stock3 = Stock.objects.create(
      name='test_name3',
      category='test_category',
      admin=self.admin
    )

    stock_list = [
      stock1, stock2, stock3
    ]

    for stock in stock_list:
      self.new_class.stock.add(stock)

    self.assertEqual(len(stock_list), self.new_class.stock.count())
