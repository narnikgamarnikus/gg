from test_plus.test import TestCase
from gg.services.models import Service

class TestService(TestCase):

    def setUp(self):
        self.service = Service.objects.create(name="testservice")

    def test__str__(self):
        self.assertEqual(
            self.service.__str__(),
            'testservice'  # This is the default username for self.make_user()
        )
    
    def test_get_absolute_url(self):
        self.assertEqual(
            self.service.get_absolute_url(),
            '/ru-ru/services/testservice/'
        )
    