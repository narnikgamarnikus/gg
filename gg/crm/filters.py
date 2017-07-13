import django_filters
from .models import Assignment

class AssignmentFilter(django_filters.FilterSet):
    #type = django_filters.CharFilter(name='type', lookup_expr='iexact')

    class Meta:
        model = Assignment
        fields = ['type']
