from django.core.urlresolvers import reverse, resolve
from test_plus.test import TestCase
from .factories import ProposalFactory
from ..models import Proposal
from django.utils.translation import activate


class TestUserURLs(TestCase):
	"""Test URL patterns for users app."""

	def setUp(self):
		self.proposal = ProposalFactory


	def test_detail_reverse(self):
		activate('en')
		"""workflow:assignment_detail should reverse to /workflow/proposal/slug-0/."""
		self.assertEqual(reverse('workflow:proposal_detail', kwargs={'slug': 'slug-0'}), '/en/workflow/slug-0/')

	def test_detail_resolve(self):
		activate('en')
		"""/workflow/slug-0/ should resolve to workflow:assignment_detail."""
		self.assertEqual(resolve('/en/workflow/slug-0/').view_name, 'workflow:proposal_detail')


	def test_create_resolve(self):
		activate('en')
		"""workflow:create should reverse to /workflow/~create/."""
		self.assertEqual(reverse('workflow:proposal_create'), '/en/workflow/~create/')

	def test_detail_resolve(self):
		activate('en')
		"""/workflow/~create/ sould reverse to workflow:create."""
		self.assertEqual(resolve('/en/workflow/~create/').view_name, 'workflow:proposal_create')


	def test_list_resolve(self):
		activate('en')
		"""workflow:list should reverse to /workflow/."""
		self.assertEqual(reverse('workflow:proposal_list'), '/en/workflow/')

	def test_list_resolve(self):
		activate('en')
		"""/workflow/ sould reverse to workflow:list."""
		self.assertEqual(resolve('/en/workflow/').view_name, 'workflow:proposal_list')