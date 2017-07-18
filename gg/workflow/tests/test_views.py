'''
from django.test import RequestFactory
from test_plus.test import TestCase
from .factories import AssignmentFactory
from ..views import (
    AssignmentRedirectView,
    AssignmentUpdateView
)


class BaseAssignmentTestCase(TestCase):

    def setUp(self):
        self.user = self.AssignmentFactory()
        self.factory = RequestFactory()


class TestAssignmentRedirectView(BaseAssignmentTestCase):

    def test_get_redirect_url(self):
        # Instantiate the view directly. Never do this outside a test!
        view = AssignmentRedirectView()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user
        # Attach the request to the view
        view.request = request
        # Expect: '/workflow/slug-0/', as that is the default slug from factory
        self.assertEqual(
            view.get_redirect_url(),
            '/workflow/slug-0/'
        )
'''