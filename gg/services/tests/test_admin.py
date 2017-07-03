from test_plus.test import TestCase
from ..models import Service

class TestServiceAdmin(TestCase):

    def setUp(self):
        self.service = Service.objects.create(slug='testservice', name='testservice')