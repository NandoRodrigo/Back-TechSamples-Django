from django.test import TestCase

from users.models import User
from classes.models import Class
from class_types.models import Type


class TypeTestModel(TestCase):

  @classmethod
  def setUpTestData(cls) -> None:

    cls.admin = User.objects.create_user(
      email='email@email.com',
      password='1234',
      is_admin=True
    )
    
    cls.new_class = Class.objects.create(
      name='test_class',
      admin=cls.admin
    )
    
    cls.name = 'test_type'
    
    cls.type = Type.objects.create(
      name = cls.name,
      class_type = cls.new_class
    )

  def test_type_fields(self):
    self.assertIsInstance(self.type.name, str)

    self.assertEqual(self.type.name, self.name)
    self.assertEqual(self.type.class_type, self.new_class)
