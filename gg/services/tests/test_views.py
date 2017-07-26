from django.test import RequestFactory
from test_plus.test import TestCase
from .factories import PriceListFactory, ServiceFactory, ServiceUserFactory, UserFactory
from ..models import Service
from ..views import (
    ServiceUpdateView,
    PriceListUpdateView,
    ServiceUserDetailView
    )





class BaseServiceTestCase(TestCase):

    def setUp(self):
        self.service_user = ServiceFactory.create()
        self.factory = RequestFactory()

'''
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
'''


class TestServiceUpdateView(BaseServiceTestCase):

    def setUp(self):
        self.service = ServiceFactory.create()
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
    
    def test_get_absolute_url(self):
        # Expect: '/services/testservice/', as that is the default service slug for
        #   self.service
        self.assertEqual(
            self.view.model.get_absolute_url(self.service),
            '/en/services/service/{}/'.format(self.service.slug)
        )



class TestPriceListUpdateView(BaseServiceTestCase):

    def setUp(self):
        # call BaseServiceTestCase.setUp()
        super(TestPriceListUpdateView, self).setUp()
        # Instantiate the view directly. Never do this outside a test!
        self.view = PriceListUpdateView()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user
        # Attach the request to the view
        self.view.request = request

'''
class TestPricelistRedirectView(BaseServiceTestCase):

    def test_get_redirect_url(self):
        # Instantiate the view directly. Never do this outside a test!
        view = PriceListRedirectView()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user
        # Attach the request to the view
        view.request = request
        # Expect: '/users/testuser/', as that is the default username for
        #   self.make_user()
        self.assertEqual(
            view.get_redirect_url(),
            '/en/users/pricelist/1/'
        )
'''



'''
class TestPriceList(TestCase):

    def setUp(self):
        self.pricelist = PriceListFactory.create()

    def test__str__(self):
        self.assertEqual(
            self.pricelist.__str__(),
            'Service: {}'.format(self.pricelist.service.name)
            )
'''


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