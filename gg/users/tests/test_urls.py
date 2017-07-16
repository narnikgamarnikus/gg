from django.core.urlresolvers import reverse, resolve
from .factories import PriceListFactory
from test_plus.test import TestCase
from django.utils.translation import activate

class TestUserURLs(TestCase):
    """Test URL patterns for users app."""

    def setUp(self):
        self.user = self.make_user()
        self.pricelist = PriceListFactory.create()

    def test_list_reverse(self):
        activate('en')
        """users:list should reverse to /users/."""
        self.assertEqual(reverse('users:list'), '/en/users/')

    def test_list_resolve(self):
        activate('en')
        """/users/ should resolve to users:list."""
        self.assertEqual(resolve('/en/users/').view_name, 'users:list')

    def test_redirect_reverse(self):
        activate('en')
        """users:redirect should reverse to /users/~redirect/."""
        self.assertEqual(reverse('users:redirect'), '/en/users/~redirect/')

    def test_redirect_resolve(self):
        activate('en')
        """/users/~redirect/ should resolve to users:redirect."""
        self.assertEqual(
            resolve('/en/users/~redirect/').view_name,
            'users:redirect'
        )

    def test_detail_reverse(self):
        activate('en')
        """users:detail should reverse to /users/testuser/."""
        self.assertEqual(
            reverse('users:detail', kwargs={'username': 'testuser'}),
            '/en/users/testuser/'
        )

    def test_detail_resolve(self):
        activate('en')
        """/users/testuser/ should resolve to users:detail."""
        self.assertEqual(resolve('/en/users/testuser/').view_name, 'users:detail')

    def test_update_reverse(self):
        activate('en')
        """users:update should reverse to /users/~update/."""
        self.assertEqual(reverse('users:update'), '/en/users/~update/')

    def test_update_resolve(self):
        activate('en')
        """/users/~update/ should resolve to users:update."""
        self.assertEqual(
            resolve('/en/users/~update/').view_name,
            'users:update'
        )

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