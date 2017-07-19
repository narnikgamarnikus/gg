from test_plus.test import TestCase
from gg.services.models import Service
from .factories import PriceListFactory, ServiceFactory, ProposalFactory

class TestService(TestCase):

    def setUp(self):
        self.service = ServiceFactory.create()

    def test__str__(self):
        self.assertEqual(
            self.service.__str__(),
            '{}'.format(self.service.title)  # This is the default username for self.make_user()
        )
    
    def test_get_absolute_url(self):
        self.assertEqual(
            self.service.get_absolute_url(),
            '/ru-ru/services/service/{}/'.format(self.service.slug)
        )
    



'''
class TestProposal(TestCase):

    def setUp(self):
        self.proposal = ProposalFactory.create()

    def test__str__(self):
        self.assertEqual(
            self.proposal.__str__(),
            self.proposal.slug
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.proposal.get_absolute_url(),
            '/en/services/service/{}/'.format(self.proposal.slug)
        )



class TestPriceList(TestCase):

    def setUp(self):
        self.pricelist = PriceListFactory.create()

    def test__str__(self):
        self.assertEqual(
            self.pricelist.__str__(),
            'Service: {}'.format(self.pricelist.service.name)
            )
'''