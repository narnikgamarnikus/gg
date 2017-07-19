from django.core.urlresolvers import reverse, resolve
from test_plus.test import TestCase
from .factories import PriceListFactory, ServiceFactory, ProposalFactory
from django.utils.translation import activate


class TestServiceURLs(TestCase):
    """Test URL patterns for users app."""

    def setUp(self):
        self.service = ServiceFactory.create()
        self.proposal = ProposalFactory.create()

    def test_service_list_reverse(self):
        activate('en')
        """services:list should reverse to /services/service/."""
        self.assertEqual(reverse('services:service_list'), '/en/services/service/')

    def test_service_list_resolve(self):
        activate('en')
        """/services/service/ should resolve to services:list."""
        self.assertEqual(resolve('/en/services/service/').view_name, 'services:service_list')

    def test_service_detail_reverse(self):
        activate('en')
        """services:detail should reverse to /services/service/testservice/."""
        self.assertEqual(
            reverse('services:service_detail', kwargs={'slug': 'testservice'}),
            '/en/services/service/testservice/'
        )

    def test_service_detail_resolve(self):
        activate('en')
        """/services/service/testservice/ should resolve to services:detail."""
        self.assertEqual(resolve('/en/services/service/testservice/').view_name, 'services:service_detail')        

    '''
    def test_redirect_reverse(self):
        activate('en')
        """services:redirect should reverse to /services/~redirect/."""
        self.assertEqual(reverse('services:redirect'), '/en/services/~redirect/')

    def test_redirect_resolve(self):
        activate('en')
        """/services/~redirect/ should resolve to services:redirect."""
        self.assertEqual(
            resolve('/en/services/~redirect/').view_name,
            'services:redirect'
        )
    ''' 

    def test_service_update_reverse(self):
        activate('en')
        """services:update should reverse to /services/service/~update/."""
        self.assertEqual(
            reverse('services:service_update', kwargs={'slug': 'testservice'}),
            '/en/services/service/~update/testservice/'
        )

    def test_update_resolve(self):
        activate('en')
        """/services/service/~update/ should resolve to services:update."""
        self.assertEqual(
            resolve('/en/services/service/~update/testservice/').view_name,
            'services:service_update'
        )

    '''
    def test_detail_reverse(self):
        activate('en')
        """services:assignment_detail should reverse to /services/proposal/slug-0/."""
        self.assertEqual(reverse('services:proposal_detail', kwargs={'slug': 'slug-0'}), '/en/services/service/slug-0/')

    def test_detail_resolve(self):
        activate('en')
        """/services/slug-0/ should resolve to services:assignment_detail."""
        self.assertEqual(resolve('/en/services/service/slug-0/').view_name, 'services:proposal_detail')


    def test_create_resolve(self):
        activate('en')
        """services:create should reverse to /services/~create/."""
        self.assertEqual(reverse('services:proposal_create'), '/en/services/service/~create/')

    def test_detail_resolve(self):
        activate('en')
        """/services/~create/ sould reverse to services:create."""
        self.assertEqual(resolve('/en/services/service/~create/').view_name, 'services:proposal_create')


    def test_list_resolve(self):
        activate('en')
        """services:list should reverse to /services/."""
        self.assertEqual(reverse('services:proposal_list'), '/en/services/service/')

    def test_list_resolve(self):
        activate('en')
        """/services/ sould reverse to services:list."""
        self.assertEqual(resolve('/en/services/service/').view_name, 'services:proposal_list')



    def test_pricelist_update_reverse(self):
        activate('en')
        """users:pricelist should reverse to /users/~update/."""
        self.assertEqual(reverse('users:pricelist_update'), '/en/users/profile/~pricelist/')

    def test_pricelist_update_resolve(self):
        activate('en')
        """/users/~update/ should resolve to users:pricelist."""
        self.assertEqual(
            resolve('/en/users/profile/~pricelist/').view_name,
            'users:pricelist_update'
        )

    
    def test_detail_pricelist_reverse(self):
        activate('en')
        """users:detail should reverse to /users/testuser/."""
        self.assertEqual(
            reverse('users:pricelist_detail', kwargs={'pk': self.pricelist.pk}),
            '/en/users/profile/pricelist/{}/'.format(self.pricelist.pk)
        )

    def test_detail_pricelist_resolve(self):
        activate('en')
        """/users/pricelist/1/ should resolve to users:detail_pricelist."""
        self.assertEqual(resolve('/en/users/profile/pricelist/{}/'.format(self.pricelist.pk)).view_name,
         'users:pricelist_detail')
    

    def test_list_pricelist_reverse(self):
        activate('en')
        """users:pricelistlist should reverse to /users/pricelist/."""
        self.assertEqual(reverse('users:pricelist_list'), '/en/users/profile/pricelist/')

    def test_list_pricelist_resolve(self):
        activate('en')
        """/users/pricelist/ should resolve to users:pricelist."""
        self.assertEqual(resolve('/en/users/profile/pricelist/').view_name, 'users:pricelist_list')
    '''