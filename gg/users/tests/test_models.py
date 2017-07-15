from test_plus.test import TestCase
from .factories import PriceListFactory

class TestUser(TestCase):

    def setUp(self):
        self.user = self.make_user()

    def test__str__(self):
        self.assertEqual(
            self.user.__str__(),
            'testuser'  # This is the default username for self.make_user()
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.user.get_absolute_url(),
            '/users/testuser/'
        )


class TestPriceList(TestCase):

    def setUp(self):
        self.service = PriceListFactory.create()

    def test__str__(self):
        self.assertEqual(
            self.service.__str__(),
            'Service: {}'.format(self.service.pk)
            )
