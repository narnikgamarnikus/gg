from django.test import RequestFactory
from test_plus.test import TestCase
from ..models import Service
from ..views import ServiceUpdateView, ServiceRedirectView

class BaseServiceTestCase(TestCase):

    def setUp(self):
        self.service = Service.objects.create(slug='testservice', name='testservice')
        self.factory = RequestFactory()


class TestServiceRedirectView(BaseServiceTestCase):

    def test_get_redirect_url(self):
        # Instantiate the view directly. Never do this outside a test!
        view = ServiceRedirectView()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the service to the request
        request.service = self.service
        # Attach the request to the view
        view.request = request
        # Expect: '/services/testservice/', as that is the default service slug for
        #   self.service
        self.assertEqual(
            view.get_redirect_url(),
            '/services/testservice/'
        )



class TestServiceUpdateView(BaseServiceTestCase):

    def setUp(self):
        # call BaseServiceTestCase.setUp()
        super(TestServiceUpdateView, self).setUp()
        # Instantiate the view directly. Never do this outside a test!
        self.view = ServiceUpdateView()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the service to the request
        request.service = self.service
        # Attach the request to the view
        self.view.request = request

    def test_get_success_url(self):
        # Expect: '/services/testservice/', as that is the default service slug for
        #   self.service
        self.assertEqual(
            self.view.get_success_url(),
            '/services/testservice/'
        )

    def test_get_object(self):
        # Expect: self.service, as that is the request's service object
        self.assertEqual(
            self.view.get_object(),
            self.service
        )
