import django_filters
from .models import Proposal

class ProposalFilter(django_filters.FilterSet):
    #type = django_filters.CharFilter(name='type', lookup_expr='iexact')

    class Meta:
        model = Proposal
        fields = ['type']
