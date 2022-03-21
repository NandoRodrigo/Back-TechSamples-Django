from datetime import datetime
from django.test import TestCase

from users.models import User
from analysis.models import Analysis


class AnalysisTestModel(TestCase):

  @classmethod
  def setUpTestData(cls) -> None:

    cls.analyst = User.objects.create_user(
      email='email@email.com',
      password='1234',
      is_admin=False
    )

    cls.batch = '123456789'
    cls.category = 'test'

    cls.analysis = Analysis.objects.create(
      batch=cls.batch,
      category=cls.category,
      analyst=cls.analyst
    )

  def test_analysis_fields(self):
    self.assertIsInstance(self.analysis.batch, str)
    self.assertIsInstance(self.analysis.category, str)
    self.assertIsInstance(self.analysis.is_concluded, bool)
    self.assertIsInstance(self.analysis.made, datetime)
    
    self.assertEqual(self.analysis.is_concluded, False)
    self.assertEqual(self.analysis.batch, self.batch)
    self.assertEqual(self.analysis.analyst, self.analyst)
    