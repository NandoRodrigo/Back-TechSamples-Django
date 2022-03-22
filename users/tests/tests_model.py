from django.test import TestCase

from users.models import User

class UserModelTest(TestCase):
  @classmethod
  def setUpTestData(cls) -> None:
    cls.first_name = 'alex'
    cls.last_name = 'silva'
    cls.email = 'email@email.com'
    cls.password = '1234'
    cls.is_admin = True

    cls.user = User.objects.create_user(
      first_name = cls.first_name,
      last_name = cls.last_name,
      email=cls.email,
      password=cls.password,
      is_admin=cls.is_admin
    )

  def test_user_fields(self):
    self.assertIsInstance(self.user.email, str)
    self.assertEqual(self.user.email, self.email)
    self.assertEqual(self.user.first_name, self.first_name)
    self.assertIsInstance(self.is_admin, bool)
    self.assertEqual(self.user.is_admin, True)
    self.assertNotEqual(self.password, self.user.password)
    self.assertIsInstance(self.user.password, str)
