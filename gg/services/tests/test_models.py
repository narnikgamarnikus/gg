from test_plus.test import TestCase
from gg.services.models import Service
from .factories import PriceListFactory, ServiceFactory, ProposalFactory, ServiceUserFactory
from django.utils.translation import activate
from django.core.urlresolvers import reverse,

class TestService(TestCase):

    def setUp(self):
        self.service = ServiceFactory.create()

    def test__str__(self):
        self.assertEqual(
            self.service.__str__(),
            self.service.title
        )
    
    def test_get_absolute_url(self):
        activate('en')
        self.assertEqual(
            self.service.get_absolute_url(),
            '/en/services/service/{}/'.format(self.service.slug)
        )
        self.assertEqual(
            self.service.get_absolute_url(),
            reverse('services:service_detail', 
                kwrags={'slug': self.service.slug}
                )
            )
    
    
class TestServiceUser(TestCase):

    def setUp(self):
        self.service_user = ServiceUserFactory.create()

    def test__str__(self):
        self.assertEqual(
            self.service_user.__str__(),
            self.service.username
        )
    
    def test_get_absolute_url(self):
        activate('en')
        self.assertEqual(
            self.service.get_absolute_url(),
            '/en/users/{}/'.format(self.service_user.user.username)
        )
        self.assertEqual(
            self.service.get_absolute_url(),
            reverse('users:detail', 
                kwrags={'username': self.service_user.user.username}
                )
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