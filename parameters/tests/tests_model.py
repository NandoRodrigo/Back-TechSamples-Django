from django.test import TestCase

from users.models import User
from classes.models import Class
from class_types.models import Type
from parameters.models import Parameter


class ParameterTestModel(TestCase):

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

    cls.type = Type.objects.create(
      name='test_type',
      class_type=cls.new_class
    )

    cls.name = 'test_parameter'
    cls.minimum = '2'
    cls.maximum = '10'
    cls.unit = '%'

    cls.parameter = Parameter.objects.create(
      name=cls.name,
      minimum=cls.minimum,
      maximum=cls.maximum,
      unit=cls.unit,
      type=cls.type
    )

  def test_parameters_field(self):
    self.assertIsInstance(self.parameter.name, str)
    self.assertIsInstance(self.parameter.unit, str)

    self.assertEqual(self.parameter.result, None)
    self.assertEqual(self.parameter.name, self.name)
    self.assertEqual(self.parameter.unit, self.unit)

    self.assertEqual(self.parameter.type, self.type)
    self.assertEqual(self.parameter.type.class_type, self.new_class)
    self.assertEqual(self.parameter.type.class_type.admin, self.admin)
