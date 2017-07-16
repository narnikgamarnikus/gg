from test_plus.test import TestCase
from .factories import AssignmentFactory
from ..models import Assignment


class TestAssignment(TestCase):

    def setUp(self):
        self.assignment = AssignmentFactory()

    def test__str__(self):
        self.assertEqual(
            self.assignment.__str__(),
            self.assignment.slug
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.assignment.get_absolute_url(),
            '/ru-ru/crm/{}/'.format(self.assignment.slug)
        )
