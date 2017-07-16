from django.core.urlresolvers import reverse, resolve
from test_plus.test import TestCase
from ..models import Service
from django.utils.translation import activate

class TestUserURLs(TestCase):
    """Test URL patterns for users app."""

    def setUp(self):
        self.service = Service.objects.create(slug='testservice', name='testservice')

    def test_list_reverse(self):
        activate('en')
        """services:list should reverse to /services/."""
        self.assertEqual(reverse('services:list'), '/en/services/')

    def test_list_resolve(self):
        activate('en')
        """/services/ should resolve to services:list."""
        self.assertEqual(resolve('/en/services/').view_name, 'services:list')

    def test_detail_reverse(self):
        activate('en')
        """services:detail should reverse to /services/testservice/."""
        self.assertEqual(
            reverse('services:detail', kwargs={'slug': 'testservice'}),
            '/en/services/testservice/'
        )

    def test_detail_resolve(self):
        activate('en')
        """/services/testservice/ should resolve to services:detail."""
        self.assertEqual(resolve('/en/services/testservice/').view_name, 'services:detail')        

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

    def test_update_reverse(self):
        activate('en')
        """services:update should reverse to /services/~update/."""
        self.assertEqual(
            reverse('services:update', kwargs={'slug': 'testservice'}),
            '/en/services/~update/testservice/'
        )

    def test_update_resolve(self):
        activate('en')
        """/services/~update/ should resolve to services:update."""
        self.assertEqual(
            resolve('/en/services/~update/testservice/').view_name,
            'services:update'
        )
