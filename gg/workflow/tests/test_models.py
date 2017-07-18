from test_plus.test import TestCase
from .factories import ProposalFactory
from ..models import Proposal


class TestProposal(TestCase):

    def setUp(self):
        self.proposal = ProposalFactory()

    def test__str__(self):
        self.assertEqual(
            self.proposal.__str__(),
            self.proposal.slug
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.proposal.get_absolute_url(),
            '/en/workflow/{}/'.format(self.proposal.slug)
        )
