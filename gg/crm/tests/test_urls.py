from django.core.urlresolvers import reverse, resolve
from test_plus.test import TestCase
from .factories import AssignmentFactory
from ..models import Assignment

class TestUserURLs(TestCase):
	"""Test URL patterns for users app."""

	def setUp(self):
		self.assignment = AssignmentFactory


	def test_detail_reverse(self):
		"""crm:assignment_detail should reverse to /crm/assignment/slug-0/."""
		self.assertEqual(reverse('crm:assignment_detail', kwargs={'slug': 'slug-0'}), '/crm/slug-0/')

	def test_detail_resolve(self):
		"""/crm/slug-0/ should resolve to crm:assignment_detail."""
		self.assertEqual(resolve('/crm/slug-0/').view_name, 'crm:assignment_detail')


	def test_create_resolve(self):
		"""crm:create should reverse to /crm/~create/."""
		self.assertEqual(reverse('crm:assignment_create'), '/crm/~create/')

	def test_detail_resolve(self):
		"""/crm/~create/ sould reverse to crm:create."""
		self.assertEqual(resolve('/crm/~create/').view_name, 'crm:assignment_create')


	def test_list_resolve(self):
		"""crm:list should reverse to /crm/."""
		self.assertEqual(reverse('crm:assignment_list'), '/crm/')

	def test_list_resolve(self):
		"""/crm/ sould reverse to crm:list."""
		self.assertEqual(resolve('/crm/').view_name, 'crm:assignment_list')