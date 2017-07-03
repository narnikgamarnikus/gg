from django.core.urlresolvers import reverse, resolve
from test_plus.test import TestCase
from ..models import Service


class TestUserURLs(TestCase):
    """Test URL patterns for users app."""

    def setUp(self):
        self.service = Service.objects.create(slug='testservice', name='testservice')

    def test_list_reverse(self):
        """services:list should reverse to /services/."""
        self.assertEqual(reverse('services:list'), '/services/')

    def test_list_resolve(self):
        """/services/ should resolve to services:list."""
        self.assertEqual(resolve('/services/').view_name, 'services:list')

    def test_detail_reverse(self):
        """services:detail should reverse to /services/testservice/."""
        self.assertEqual(
            reverse('services:detail', kwargs={'service': 'testservice'}),
            '/services/testservice/'
        )

    def test_detail_resolve(self):
        """/services/testservice/ should resolve to services:detail."""
        self.assertEqual(resolve('/services/testservice/').view_name, 'services:detail')        

    def test_redirect_reverse(self):
        """services:redirect should reverse to /services/~redirect/."""
        self.assertEqual(reverse('services:redirect'), '/services/~redirect/')

    def test_redirect_resolve(self):
        """/services/~redirect/ should resolve to services:redirect."""
        self.assertEqual(
            resolve('/services/~redirect/').view_name,
            'services:redirect'
        )

    def test_update_reverse(self):
        """services:update should reverse to /services/~update/."""
        self.assertEqual(reverse('users:update'), '/users/~update/')

    def test_update_resolve(self):
        """/services/~update/ should resolve to services:update."""
        self.assertEqual(
            resolve('/services/~update/').view_name,
            'services:update'
        )
