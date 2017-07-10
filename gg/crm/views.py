from django.views.generic import DetailView, CreateView, ListView, View
from django.views.generic.edit import BaseCreateView
from .models import Assignment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from gg.services.models import Service
import ujson as json
from .forms import AssignmentForm
from django.core.urlresolvers import reverse
from dal import autocomplete


class AssignmentCreateView(CreateView):
	model = Assignment
	form_class = AssignmentForm

class AssignmentDetailView(LoginRequiredMixin, DetailView):
    # These next one line tell the view to index lookups by slug
    model = Assignment

    def get_context_data(self, **kwargs):
    	context = super(AssignmentDetailView, self).get_context_data(**kwargs)
    	return context


class AssignmentListView(LoginRequiredMixin, ListView):
    # These next one line tell the view to index lookups by slug
    model = Assignment






class ServicesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Service.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs