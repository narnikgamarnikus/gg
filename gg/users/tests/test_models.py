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
            '/en/users/testuser/'
        )


class TestPriceList(TestCase):

    def setUp(self):
        self.pricelist = PriceListFactory.create()

    def test__str__(self):
        self.assertEqual(
            self.pricelist.__str__(),
            'Service: {}'.format(self.pricelist.service.name)
            )
